# -*- coding: utf-8 -*-
"""
SkillInstaller + FFmpeg 修复工具

功能：
1. 选择一个 Skill Markdown 文件，自动安装到 Codex 或 Claude。
2. 检查 ffmpeg / ffprobe 是否可用。
3. 一键下载并安装 FFmpeg 到用户目录。
4. 自动把 FFmpeg 加入当前用户 PATH。

说明：
- 运行源码需要 Python。
- 打包成 exe 后，最终用户不需要 Python。
"""

from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile
import threading
import urllib.request
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox


APP_TITLE = "Codex / Claude Skill 安装器"
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
INSTALL_TARGETS = {
    "codex": {
        "label": "Codex",
        "root": Path.home() / ".codex" / "skills",
        "restart": "Codex 客户端",
    },
    "claude": {
        "label": "Claude",
        "root": Path.home() / ".claude" / "skills",
        "restart": "Claude 客户端",
    },
}


def run_command(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=False,
            timeout=10
        )
        return result.returncode == 0, (result.stdout or result.stderr or "").strip()
    except Exception as exc:
        return False, str(exc)


def command_exists(command):
    ok, _ = run_command([command, "-version"])
    return ok


def check_ffmpeg_status():
    ffmpeg_ok = command_exists("ffmpeg")
    ffprobe_ok = command_exists("ffprobe")
    return ffmpeg_ok and ffprobe_ok


def parse_frontmatter_name(md_text):
    if not md_text.lstrip().startswith("---"):
        return ""
    parts = md_text.lstrip().split("---", 2)
    if len(parts) < 3:
        return ""
    for line in parts[1].splitlines():
        line = line.strip()
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return ""


def sanitize_skill_name(name):
    name = name.strip().lower().replace(" ", "-")
    name = re.sub(r"[^a-z0-9._-]+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name or "unnamed-skill"


def infer_skill_name(path):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")

    name = parse_frontmatter_name(text)
    if name:
        return sanitize_skill_name(name)

    stem = path.stem
    stem = re.sub(r"[_\- ]?SKILL$", "", stem, flags=re.IGNORECASE)
    return sanitize_skill_name(stem)


def validate_skill_md(path):
    if not path.exists():
        return False, "文件不存在。"
    if path.suffix.lower() != ".md":
        return False, "请选择 .md 格式的 Skill 文件。"
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
    if not text.strip():
        return False, "文件内容为空。"
    if not text.lstrip().startswith("---"):
        return False, "文件开头缺少 YAML 信息。Skill 文件通常需要以 --- 开头。"
    parts = text.lstrip().split("---", 2)
    if len(parts) < 3:
        return False, "YAML 信息格式不完整。"
    fm = parts[1]
    if "name:" not in fm:
        return False, "YAML 信息中缺少 name 字段。"
    if "description:" not in fm:
        return False, "YAML 信息中缺少 description 字段。"
    return True, ""


def get_selected_install_targets():
    choice = install_target_var.get()
    if choice == "claude":
        return ["claude"]
    if choice == "both":
        return ["codex", "claude"]
    return ["codex"]


def format_install_paths(paths):
    return "\n".join(str(p) for p in paths)


def install_skill(md_path):
    path = Path(md_path).expanduser().resolve()
    ok, msg = validate_skill_md(path)
    if not ok:
        messagebox.showerror("安装失败", msg)
        status_var.set("安装失败：" + msg)
        return

    skill_name = infer_skill_name(path)
    installed_files = []
    for target_key in get_selected_install_targets():
        target_root = INSTALL_TARGETS[target_key]["root"]
        target_dir = target_root / skill_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / "SKILL.md"
        if target_file.exists():
            target_label = INSTALL_TARGETS[target_key]["label"]
            if not messagebox.askyesno(
                "确认覆盖",
                f"{target_label} 中已存在 Skill：{skill_name}\n\n"
                f"现有文件：\n{target_file}\n\n"
                "是否覆盖？"
            ):
                continue
        shutil.copy2(path, target_file)
        installed_files.append(target_file)

    if not installed_files:
        status_var.set("安装已取消：没有覆盖任何已有 Skill。")
        return

    skill_name_var.set(skill_name)
    target_path_var.set(format_install_paths(installed_files))
    target_labels = " + ".join(INSTALL_TARGETS[k]["label"] for k in get_selected_install_targets())
    status_var.set(f"已安装到 {target_labels}：" + skill_name)
    restart_names = " / ".join(INSTALL_TARGETS[k]["restart"] for k in get_selected_install_targets())

    messagebox.showinfo(
        "安装成功",
        "Skill 已成功安装：\n\n"
        + skill_name
        + "\n\n安装位置：\n"
        + format_install_paths(installed_files)
        + "\n\n请完全退出并重启 "
        + restart_names
        + " 后使用。"
    )


def choose_file():
    file_path = filedialog.askopenfilename(
        title="选择 Skill Markdown 文件",
        filetypes=[("Markdown 文件", "*.md"), ("所有文件", "*.*")]
    )
    if file_path:
        install_skill(file_path)


def open_skills_folder():
    folders = [INSTALL_TARGETS[k]["root"] for k in get_selected_install_targets()]
    failed = []
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        try:
            os.startfile(str(folder))
        except Exception:
            failed.append(str(folder))
    if failed:
        messagebox.showinfo("Skills 目录", "\n".join(failed))


def open_ffmpeg_folder():
    folder = Path.home() / ".codex-tools" / "ffmpeg"
    folder.mkdir(parents=True, exist_ok=True)
    try:
        os.startfile(str(folder))
    except Exception:
        messagebox.showinfo("FFmpeg 安装目录", str(folder))


def copy_path():
    p = target_path_var.get().strip()
    if p and p != "-":
        root.clipboard_clear()
        root.clipboard_append(p)
        status_var.set("已复制安装路径。")


def update_ffmpeg_status_label():
    if check_ffmpeg_status():
        ffmpeg_status_var.set("FFmpeg 状态：已就绪")
    else:
        ffmpeg_status_var.set("FFmpeg 状态：未检测到")


def add_to_user_path(bin_dir):
    """
    将 bin_dir 加入当前用户 PATH。
    不需要管理员权限。
    """
    import winreg

    bin_dir = str(Path(bin_dir).resolve())

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Environment",
        0,
        winreg.KEY_READ | winreg.KEY_WRITE
    )

    try:
        current, value_type = winreg.QueryValueEx(key, "Path")
    except FileNotFoundError:
        current = ""
        value_type = winreg.REG_EXPAND_SZ

    paths = [p.strip() for p in current.split(";") if p.strip()]
    lower_paths = [p.lower() for p in paths]

    if bin_dir.lower() not in lower_paths:
        paths.append(bin_dir)
        new_value = ";".join(paths)
        winreg.SetValueEx(key, "Path", 0, value_type, new_value)

    winreg.CloseKey(key)

    # 当前程序内立即生效，便于检测。
    os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + bin_dir

    # 通知系统环境变量变化。
    try:
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_ABORTIFHUNG,
            5000,
            None
        )
    except Exception:
        pass


def find_ffmpeg_bin(root_dir):
    root_dir = Path(root_dir)
    for p in root_dir.rglob("ffmpeg.exe"):
        bin_dir = p.parent
        if (bin_dir / "ffprobe.exe").exists():
            return bin_dir
    return None


def safe_extract_zip(zip_file, destination):
    destination = Path(destination).resolve()
    for member in zip_file.infolist():
        target_path = (destination / member.filename).resolve()
        if target_path != destination and destination not in target_path.parents:
            raise RuntimeError(f"压缩包包含不安全路径：{member.filename}")
    zip_file.extractall(destination)


def download_file(url, destination, progress_callback=None):
    def reporthook(block_num, block_size, total_size):
        if progress_callback and total_size > 0:
            downloaded = block_num * block_size
            percent = min(100, int(downloaded * 100 / total_size))
            progress_callback(percent)

    urllib.request.urlretrieve(url, destination, reporthook=reporthook)


def install_ffmpeg_worker():
    try:
        install_ffmpeg_btn.config(state="disabled")
        status_var.set("正在检查 FFmpeg...")

        if check_ffmpeg_status():
            ffmpeg_status_var.set("FFmpeg 状态：已就绪")
            status_var.set("FFmpeg 已经安装，无需重复安装。")
            messagebox.showinfo("FFmpeg", "已检测到 ffmpeg 和 ffprobe，可以直接使用。")
            return

        install_root = Path.home() / ".codex-tools" / "ffmpeg"
        install_root.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            zip_path = tmp_dir / "ffmpeg.zip"

            status_var.set("正在下载 FFmpeg...")
            download_file(
                FFMPEG_URL,
                zip_path,
                lambda p: status_var.set(f"正在下载 FFmpeg... {p}%")
            )

            status_var.set("正在解压 FFmpeg...")
            with zipfile.ZipFile(zip_path, "r") as z:
                safe_extract_zip(z, install_root)

        bin_dir = find_ffmpeg_bin(install_root)
        if not bin_dir:
            raise RuntimeError("解压完成，但没有找到 ffmpeg.exe。")

        status_var.set("正在写入用户 PATH...")
        add_to_user_path(bin_dir)

        if check_ffmpeg_status():
            ffmpeg_status_var.set("FFmpeg 状态：已就绪")
            status_var.set("FFmpeg 安装成功。")
            messagebox.showinfo(
                "FFmpeg 安装成功",
                "FFmpeg 已安装成功。\n\n"
                f"安装位置：\n{bin_dir}\n\n"
                "请重启 Codex 客户端，以及已经打开的 PowerShell / CMD 窗口。"
            )
        else:
            ffmpeg_status_var.set("FFmpeg 状态：已安装，重启后生效")
            status_var.set("FFmpeg 已安装，可能需要重启后生效。")
            messagebox.showinfo(
                "FFmpeg 已安装",
                "FFmpeg 已下载并加入 PATH。\n\n"
                "如果当前窗口仍然检测不到，请重启 PowerShell / CMD / Codex 后再试。"
            )

    except Exception as exc:
        status_var.set("FFmpeg 安装失败。")
        messagebox.showerror(
            "FFmpeg 安装失败",
            "自动安装 FFmpeg 失败。\n\n"
            + str(exc)
            + "\n\n可能原因：网络拦截下载地址、公司电脑限制、杀毒软件拦截。\n你仍然可以手动安装 FFmpeg。"
        )
    finally:
        install_ffmpeg_btn.config(state="normal")
        update_ffmpeg_status_label()


def install_ffmpeg():
    if not messagebox.askyesno(
        "安装 / 修复 FFmpeg",
        "将自动下载 FFmpeg，并安装到：\n\n"
        "%USERPROFILE%\\.codex-tools\\ffmpeg\n\n"
        "同时会把 FFmpeg 加入当前用户 PATH。\n\n"
        "这通常不需要管理员权限。\n\n"
        "是否继续？"
    ):
        return

    t = threading.Thread(target=install_ffmpeg_worker, daemon=True)
    t.start()


def build_ui():
    root.configure(bg="#f7f7f5")

    tk.Label(
        root,
        text="Codex / Claude Skill 安装器",
        bg="#f7f7f5",
        fg="#111111",
        font=("Microsoft YaHei UI", 20, "bold")
    ).pack(pady=(22, 4))

    tk.Label(
        root,
        text="一键安装 Skill 到 Codex 或 Claude，并为视频类 Skill 准备 FFmpeg",
        bg="#f7f7f5",
        fg="#666666",
        font=("Microsoft YaHei UI", 10)
    ).pack(pady=(0, 14))

    main = tk.Frame(root, bg="#f7f7f5")
    main.pack(padx=28, fill="both")

    skill_box = tk.LabelFrame(
        main,
        text="  第一步：安装 Skill  ",
        bg="#f7f7f5",
        fg="#444444",
        font=("Microsoft YaHei UI", 9)
    )
    skill_box.pack(fill="x", pady=(0, 10))

    target_box = tk.Frame(skill_box, bg="#f7f7f5")
    target_box.pack(padx=12, pady=(12, 4), fill="x")

    tk.Label(
        target_box,
        text="安装到：",
        bg="#f7f7f5",
        fg="#555555",
        font=("Microsoft YaHei UI", 10, "bold")
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))

    tk.Radiobutton(
        target_box,
        text="Codex",
        variable=install_target_var,
        value="codex",
        bg="#f7f7f5",
        font=("Microsoft YaHei UI", 10)
    ).grid(row=0, column=1, sticky="w", padx=4)

    tk.Radiobutton(
        target_box,
        text="Claude",
        variable=install_target_var,
        value="claude",
        bg="#f7f7f5",
        font=("Microsoft YaHei UI", 10)
    ).grid(row=0, column=2, sticky="w", padx=4)

    tk.Radiobutton(
        target_box,
        text="Codex + Claude",
        variable=install_target_var,
        value="both",
        bg="#f7f7f5",
        font=("Microsoft YaHei UI", 10)
    ).grid(row=0, column=3, sticky="w", padx=4)

    tk.Button(
        skill_box,
        text="选择 Skill 的 .md 文件",
        command=choose_file,
        width=30,
        height=2,
        font=("Microsoft YaHei UI", 11, "bold")
    ).pack(pady=(8, 10))

    info = tk.Frame(skill_box, bg="#f7f7f5")
    info.pack(padx=12, pady=(0, 10), fill="x")

    tk.Label(info, text="Skill 名称：", bg="#f7f7f5", fg="#777777", font=("Microsoft YaHei UI", 9)).grid(row=0, column=0, sticky="w")
    tk.Label(info, textvariable=skill_name_var, bg="#f7f7f5", fg="#222222", font=("Consolas", 9)).grid(row=0, column=1, sticky="w")

    tk.Label(info, text="安装位置：", bg="#f7f7f5", fg="#777777", font=("Microsoft YaHei UI", 9)).grid(row=1, column=0, sticky="w", pady=(5, 0))
    tk.Label(info, textvariable=target_path_var, bg="#f7f7f5", fg="#222222", font=("Consolas", 8), wraplength=430, justify="left").grid(row=1, column=1, sticky="w", pady=(5, 0))

    skill_btns = tk.Frame(skill_box, bg="#f7f7f5")
    skill_btns.pack(pady=(0, 10))
    tk.Button(skill_btns, text="打开 Skills 目录", command=open_skills_folder, width=18).grid(row=0, column=0, padx=5)
    tk.Button(skill_btns, text="复制安装路径", command=copy_path, width=14).grid(row=0, column=1, padx=5)

    ffmpeg_box = tk.LabelFrame(
        main,
        text="  第二步：视频依赖检查  ",
        bg="#f7f7f5",
        fg="#444444",
        font=("Microsoft YaHei UI", 9)
    )
    ffmpeg_box.pack(fill="x", pady=(0, 8))

    row = tk.Frame(ffmpeg_box, bg="#f7f7f5")
    row.pack(pady=12)

    tk.Label(
        row,
        textvariable=ffmpeg_status_var,
        bg="#f7f7f5",
        fg="#222222",
        font=("Microsoft YaHei UI", 10, "bold")
    ).grid(row=0, column=0, padx=8)

    global install_ffmpeg_btn
    install_ffmpeg_btn = tk.Button(
        row,
        text="安装 / 修复 FFmpeg",
        command=install_ffmpeg,
        width=18
    )
    install_ffmpeg_btn.grid(row=0, column=1, padx=8)

    tk.Button(row, text="打开 FFmpeg 目录", command=open_ffmpeg_folder, width=18).grid(row=0, column=2, padx=8)

    tk.Label(
        root,
        textvariable=status_var,
        bg="#f7f7f5",
        fg="#666666",
        font=("Microsoft YaHei UI", 9)
    ).pack(pady=(4, 0))


root = tk.Tk()
root.title(APP_TITLE)
root.geometry("650x505")
root.resizable(False, False)

status_var = tk.StringVar(value="准备就绪。")
install_target_var = tk.StringVar(value="codex")
skill_name_var = tk.StringVar(value="-")
target_path_var = tk.StringVar(value="-")
ffmpeg_status_var = tk.StringVar(value="FFmpeg 状态：正在检查...")
install_ffmpeg_btn = None

build_ui()
update_ffmpeg_status_label()
root.mainloop()
