# -*- coding: utf-8 -*-
"""
xhs_fetch.py -- 按关键词从小红书拉真实场景图，落到素材池。

走 Playwright 持久化浏览器，不是逆向签名接口：小红书搜索页是前端渲染的，
XHR 要 x-s 签名，逆向出来隔几周就失效；用真浏览器带登录态跑，接口改版也不受影响。
登录态存在本地 profile 目录，扫码一次可以反复用。

三条子命令：
  login                                  首次扫码登录，把登录态写进 profile
  fetch --topics topics.json --out 01_素材    按 topics 里每个选题的 keywords 批量拉
  fetch --keyword "工位 桌搭" --out 01_素材/01  单关键词拉
  from-urls urls.txt --out 01_素材/01      兜底：手动贴图片直链，纯下载

依赖（首次要装）：
  pip install playwright httpx
  python -m playwright install chromium

素材合规：抓下来的是他人拍摄的照片。自用测试、内部比稿没问题；
真要公开发布，请换成自有素材、授权图库或 AI 生成图——本脚本只负责取，不负责授权。
"""
import argparse
import hashlib
import io
import os
import re
import sys
import time
import urllib.parse

DEFAULT_PROFILE = os.environ.get(
    "XHS_PROFILE", os.path.join(os.path.expanduser("~"), ".xhs_profile"))
SEARCH_URL = "https://www.xiaohongshu.com/search_result?keyword={kw}"
ASSET_EXT = {".js", ".css", ".svg", ".ico", ".woff", ".woff2", ".ttf",
             ".mp4", ".gif", ".json"}
IMG_MIN_W, IMG_MIN_H = 480, 480


# ---------------------------------------------------------------- 工具

def die(msg, code=1):
    print("\n[xhs_fetch] " + msg, file=sys.stderr)
    sys.exit(code)


def need_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except ImportError:
        die("缺 Playwright。先跑：\n"
            "    pip install playwright httpx\n"
            "    python -m playwright install chromium")


def upgrade_url(u):
    """
    尽量取大图。但别指望它能提分辨率——

    实测（2026-09-10）：搜索列表页的直链形如
        .../notes_uhdr/<id>!nc_n_webp_mw_1
    尺寸由末尾 `!` 后的 **CDN 预设** 决定，`imageView2` 查询参数会被完全忽略
    （w/1280、w/1920、去掉参数，返回的都是同一张 640×853）。
    而换预设后缀会 403——路径里带时间+哈希令牌，签名和预设是绑死的。

    结论：搜索列表页就是 640 宽封顶。想要原图得逐条进笔记详情页取，本脚本不做。
    640 宽对 960×600 输出够用：文字在 1920px 画布上矢量绘制再降采样，锐度不受影响，
    背景略软反而更贴「真实手机照」的调性。

    下面的重写只对老式 imageView2 直链有效，留着当兼容。
    """
    u = u.split("&amp;")[0].replace("&amp;", "&")
    u = re.sub(r"/w/\d+", "/w/1280", u)
    u = re.sub(r"format/(webp|heic)", "format/jpg", u)
    if "imageView2" not in u and "?" not in u:
        u += "?imageView2/2/w/1280/format/jpg"
    return u


# ---------------------------------------------------------------- 浏览器

def open_context(pw, profile, headless=True):
    return pw.chromium.launch_persistent_context(
        user_data_dir=profile,
        headless=headless,
        viewport={"width": 1440, "height": 900},
        user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
        locale="zh-CN",
    )


def cmd_login(args):
    need_playwright()
    from playwright.sync_api import sync_playwright
    os.makedirs(args.profile, exist_ok=True)
    with sync_playwright() as pw:
        ctx = open_context(pw, args.profile, headless=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://www.xiaohongshu.com/explore", timeout=60000)
        print("浏览器已打开。请扫码登录小红书，登录完成后回到这里按回车。")
        print("（登录态会写进 %s，之后 fetch 就能无头跑）" % args.profile)
        try:
            input()
        except EOFError:
            time.sleep(120)
        ctx.close()
    print("登录态已保存。")


def is_logged_in(page):
    """
    未登录时搜索页会盖一层 .login-container 登录遮罩，且一条笔记卡片都不渲染。
    别去匹配「扫码登录」文案——实测页面写的是「手机号登录」，按文案判会漏。
    """
    try:
        if page.locator(".login-container").count() > 0:
            return False
        if page.locator("section.note-item, div.note-item").count() > 0:
            return True
    except Exception:      # noqa: BLE001
        pass
    return True


def is_note_image(u):
    """
    只要笔记正文图。小红书页面里混着大量同域的前端静态资源
    （fe-static/fe-video 下的 .js/.css/.svg/.ico），不滤掉会全抓回来。
    """
    try:
        parts = urllib.parse.urlparse(u)
    except Exception:      # noqa: BLE001
        return False
    host, path = parts.netloc.lower(), parts.path.lower()
    if "xhscdn.com" not in host:
        return False
    if host.startswith(("fe-static", "fe-video", "fe-platform")):
        return False
    if "sns-" not in host:                       # 正文图都在 sns-webpic / sns-img
        return False
    if any(k in u for k in ("/avatar/", "/emoji/", "picasso-static", "sns-avatar")):
        return False
    if os.path.splitext(path)[1] in ASSET_EXT:
        return False
    return True


def collect_image_urls(page, scrolls, want):
    """
    滚动搜索结果页，收笔记封面直链。
    读渲染后 img 元素的 currentSrc，而不是拿正则扫 HTML——扫 HTML 会把
    内联脚本里的资源链接一并捞进来。
    """
    seen, out = set(), []
    for _ in range(scrolls + 1):
        try:
            srcs = page.eval_on_selector_all(
                "img", "els => els.map(e => e.currentSrc || e.src || '')")
        except Exception:      # noqa: BLE001
            srcs = []
        for u in srcs:
            if not u.startswith("http") or not is_note_image(u):
                continue
            key = re.sub(r"\?.*$", "", u)
            if key in seen:
                continue
            seen.add(key)
            out.append(upgrade_url(u))
        if len(out) >= want * 3:
            break
        page.mouse.wheel(0, 2400)
        page.wait_for_timeout(1500)
    return out


def fetch_keyword(page, keyword, want, scrolls):
    url = SEARCH_URL.format(kw=urllib.parse.quote(keyword))
    page.goto(url, timeout=60000, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    if not is_logged_in(page):
        die("登录态已失效（搜索页被登录遮罩挡住）。重跑一次："
            "python xhs_fetch.py login")
    urls = collect_image_urls(page, scrolls, want)
    if not urls:
        print("    ! 一张笔记图都没取到。要么关键词太偏，要么登录态刚失效。",
              file=sys.stderr)
    return urls


# ---------------------------------------------------------------- 下载

def download(urls, out_dir, want, min_ratio=0.6):
    """下图 → 过滤尺寸/比例 → 按内容去重 → 存 jpg。返回实际存下的路径。"""
    import httpx
    from PIL import Image

    os.makedirs(out_dir, exist_ok=True)
    seen_hash = set()
    for f in os.listdir(out_dir):                       # 已有文件也纳入去重
        p = os.path.join(out_dir, f)
        if os.path.isfile(p):
            seen_hash.add(hashlib.md5(open(p, "rb").read()).hexdigest())

    saved = []
    headers = {"Referer": "https://www.xiaohongshu.com/",
               "User-Agent": "Mozilla/5.0"}
    with httpx.Client(timeout=25, headers=headers, follow_redirects=True) as cli:
        for u in urls:
            if len(saved) >= want:
                break
            try:
                r = cli.get(u)
                if r.status_code != 200 or len(r.content) < 20000:
                    continue
                im = Image.open(io.BytesIO(r.content))
                if im.width < IMG_MIN_W or im.height < IMG_MIN_H:
                    continue
                if im.width / im.height < min_ratio:     # 太竖的裁到 16:10 会废
                    continue
                buf = io.BytesIO()
                im.convert("RGB").save(buf, "JPEG", quality=94)
                h = hashlib.md5(buf.getvalue()).hexdigest()
                if h in seen_hash:
                    continue
                seen_hash.add(h)
                path = os.path.join(out_dir, "%s.jpg" % h[:12])
                with open(path, "wb") as fh:
                    fh.write(buf.getvalue())
                saved.append(path)
                print("    + %s  %dx%d" % (os.path.basename(path), im.width, im.height))
            except Exception:      # noqa: BLE001
                continue
    return saved


# ---------------------------------------------------------------- 子命令

def cmd_fetch(args):
    need_playwright()
    from playwright.sync_api import sync_playwright

    jobs = []          # [(out_dir, [keyword, ...])]
    if args.topics:
        import json
        with open(args.topics, encoding="utf-8") as fh:
            cfg = json.load(fh)
        topics = cfg["topics"] if isinstance(cfg, dict) else cfg
        for n, t in enumerate(topics, 1):
            tid = str(t.get("id") or n)
            kws = t.get("keywords") or []
            if not kws:
                print("  ! 选题 %s 没写 keywords，跳过" % tid, file=sys.stderr)
                continue
            jobs.append((os.path.join(args.out, tid), kws))
    elif args.keyword:
        jobs.append((args.out, [args.keyword]))
    else:
        die("要么给 --topics，要么给 --keyword")

    if not os.path.isdir(args.profile):
        die("还没有登录态（%s 不存在）。先跑：python xhs_fetch.py login" % args.profile)

    total = 0
    with sync_playwright() as pw:
        ctx = open_context(pw, args.profile, headless=not args.headful)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for out_dir, kws in jobs:
            print("\n[%s]" % out_dir)
            got = []
            per = max(1, args.n // max(1, len(kws)))
            for kw in kws:
                print("  搜索：%s" % kw)
                try:
                    urls = fetch_keyword(page, kw, per, args.scrolls)
                except Exception as e:      # noqa: BLE001
                    print("    搜索失败：%s" % e, file=sys.stderr)
                    continue
                got += download(urls, out_dir, per + 2, args.min_ratio)
                time.sleep(args.delay)
            total += len(got)
            print("  小计 %d 张" % len(got))
        ctx.close()
    print("\n共取回 %d 张素材。" % total)


def cmd_from_urls(args):
    urls = [l.strip() for l in open(args.file, encoding="utf-8") if l.strip()]
    urls = [upgrade_url(u) for u in urls if u.startswith("http")]
    saved = download(urls, args.out, args.n, args.min_ratio)
    print("\n存下 %d 张。" % len(saved))


def main():
    ap = argparse.ArgumentParser(description="小红书场景图采集")
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="浏览器 profile 目录")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("login", help="扫码登录，保存登录态")
    p.set_defaults(func=cmd_login)

    p = sub.add_parser("fetch", help="按关键词拉图")
    p.add_argument("--topics", help="topics.json，按每个选题的 keywords 分目录拉")
    p.add_argument("--keyword", help="单个关键词")
    p.add_argument("--out", default="01_素材")
    p.add_argument("-n", type=int, default=12, help="每个选题要几张")
    p.add_argument("--scrolls", type=int, default=4, help="搜索页往下滚几屏")
    p.add_argument("--min-ratio", type=float, default=0.6, dest="min_ratio",
                   help="最小宽高比，滤掉裁到 16:10 会废的竖图")
    p.add_argument("--delay", type=float, default=2.0, help="关键词之间的间隔秒数")
    p.add_argument("--headful", action="store_true", help="显示浏览器窗口，调试用")
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("from-urls", help="从图片直链清单下载（兜底）")
    p.add_argument("file")
    p.add_argument("--out", default="01_素材")
    p.add_argument("-n", type=int, default=50)
    p.add_argument("--min-ratio", type=float, default=0.6, dest="min_ratio")
    p.set_defaults(func=cmd_from_urls)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
