# -*- coding: utf-8 -*-
"""
飞书连通性 + 权限体检
用法:python 06_代码/feishu_sync/test_connect.py

检查项:
1. 凭证是否正确(能否拿到 tenant_access_token)
2. wiki 权限:列出全部知识空间(含 space_id)
3. drive 导入权限:探测 import_tasks 是否可访问
"""
import sys
from feishu_client import FeishuClient

# 让 Windows 终端尽量按 utf-8 输出
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main():
    c = FeishuClient()

    print("【1】凭证 / token ...")
    try:
        tok = c.token()
        print(f"  ✅ 鉴权成功 (app_id={c.cfg['app_id']})")
    except Exception as e:
        print(f"  ❌ 鉴权失败:{e}")
        print("     → 检查 feishu_config.json 里的 app_id / app_secret")
        return

    print("\n【2】wiki 权限 — 列出知识空间 ...")
    code, data, spaces = c.list_wiki_spaces()
    if data.get("code") != 0:
        print(f"  ❌ 失败 code={data.get('code')} msg={data.get('msg')}")
        print("     → 可能缺少 wiki 读权限(如 wiki:wiki / wiki:space:readonly)")
        print("     → 也可能应用未被加入任一知识库的协作者")
    elif not spaces:
        print("  ⚠️ 鉴权与权限正常,但没有可见的知识空间。")
        print("     → 需要在目标飞书知识库 设置-管理员 里,把这个应用(机器人)")
        print("       加为知识库管理员/可编辑成员,它才看得见空间。")
    else:
        print(f"  ✅ 可见 {len(spaces)} 个知识空间:")
        for s in spaces:
            print(f"     - space_id={s.get('space_id')}  "
                  f"名称={s.get('name')}  类型={s.get('space_type')}")
        print("  → 把目标空间的 space_id 填回 feishu_config.json 的 target_space_id")

    print("\n【3】drive 导入权限 — 探测 import_tasks ...")
    # 用一个假 ticket 探测:权限缺失会返回权限错误码;权限正常会返回"找不到"
    code, data = c.get("/drive/v1/import_tasks/__probe__")
    ecode = data.get("code")
    if ecode in (1061002, 1061004, 1064230) or "not found" in str(data.get("msg", "")).lower():
        print(f"  ✅ 有 drive 访问权限(探测返回 code={ecode}=资源不存在,符合预期)")
    elif ecode in (1254040,) or "permission" in str(data.get("msg", "")).lower() \
            or "access" in str(data.get("msg", "")).lower():
        print(f"  ❌ 缺少 drive 导入权限 code={ecode} msg={data.get('msg')}")
        print("     → 需要 drive:drive(云空间)相关权限,导入 Markdown 要用到")
    else:
        print(f"  ℹ️ 探测返回 code={ecode} msg={data.get('msg')}(人工判断:"
              f"非权限报错即视为有权限)")

    print("\n体检结束。把 space_id 填好后,我们就进 POC。")


if __name__ == "__main__":
    main()
