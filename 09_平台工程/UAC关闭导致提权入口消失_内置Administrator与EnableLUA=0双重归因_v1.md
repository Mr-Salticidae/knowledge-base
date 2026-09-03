# UAC 关闭导致"以管理员身份运行"入口消失

> 一句话律：右键提权入口消失，先查账户类型和 UAC 状态，再谈修复——多数情况是"已经是最高权限"，不是"权限不够"。

## 现象

本地 PowerShell 无法选择"以管理员身份运行"：右键菜单没有该选项，或点击无效、不弹 UAC 窗口。

## 诊断路径（只读，无副作用）

1. **账户类型**：`whoami` + `net localgroup administrators`
   - 若当前用户就是内置 `Administrator`（SID 500），且是 administrators 组唯一成员 → 管理员身份确认。
2. **UAC 状态**：读注册表 `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`
   - `EnableLUA = 0` → UAC 总开关已关（根因）
   - `ConsentPromptBehaviorAdmin = 0` → 管理员提权"不提示直接提升"
   - `PromptOnSecureDesktop = 0` → 安全桌面提示已关
3. **进程完整性级别**：`whoami /groups` 看 S-1-16-12288（High）——UAC 关闭时进程直接以 High 完整性运行，无过滤令牌。

## 根因

两个条件叠加：

1. **UAC 被完全关闭（EnableLUA=0）**：过滤令牌机制失效，所有进程直接以完整管理员令牌运行，系统认为"提权没有意义"，右键"以管理员身份运行"入口被隐藏。
2. **内置 Administrator 账户**：SID 500 默认走全权限令牌模式，进一步弱化提权 UI。

## 影响

- 事实状态：已经是最高权限，直接运行即管理员，不需要提权选项。
- 代价：任何程序（含恶意软件）静默获得完整系统权限；部分 UWP/Store 应用（设置页等）在 EnableLUA=0 下异常。

## 修复

恢复 UAC（需重启生效）：

- 控制面板 → 用户账户 → 更改用户账户控制设置 → 拉回合适级别（默认第二档）；
- 或注册表：`HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System` → `EnableLUA = 1`。

重启后右键"以管理员身份运行"恢复。若只想确认当前已是管理员，无需改动。

## 教训

- "没有管理员选项" ≠ "没有管理员权限"，先验账户与 UAC，不要盲目提权或改权限。
- 关闭 UAC 换取"免弹窗"是常见的历史操作，排查系统类问题时应把 UAC 状态列为必查项。

## 关联文档

- [[09_平台工程索引]] —— 平台工程区入口
- [[炉石传说安装被拒_UBR判断假正常系统与Win10原地升级_v1]] —— 同区同类「系统状态被表象掩盖」的排障:本篇的假象是「没有提权入口=没有权限」,那篇的假象是「版本号正常=满足最低要求」;两篇都用**只读诊断(注册表/UBR)戳破表象**再谈修复
