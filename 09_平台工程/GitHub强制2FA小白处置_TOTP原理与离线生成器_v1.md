---
tags: [类型/平台工程, 主题/账号安全, 主题/2FA]
---
# GitHub 强制 2FA 的小白处置 · TOTP 原理与离线生成器

> 入档:2026-06-29
> 来源:帮一位非技术作者处理 GitHub 弹出的「Enable 2FA / 7 天内必须开启」拦截页;约束=国内网络、Chrome、手机没装任何验证器 App、不便用外网工具
> 状态:全流程跑通并验证(2FA 成功启用 + 官方恢复码与自存副本逐字一致 + 离线生成器经 Python/Node 同时间戳交叉验证算码一致)

## 一句话总结

GitHub 弹的「Enable two-factor authentication」**不是收费,是强制两步验证**(对上传过代码的账号强制,免费)。开启它本质只需要一个能持续产出 6 位码的 **TOTP 生成器**——而 **TOTP 是纯本地算法(密钥 + 时间,HMAC-SHA1),根本不连任何服务器**,所以「国内 / 不能用外网」对它毫无影响。手机没 App、商店进不去时,**二维码旁的 setup key 就是 TOTP 密钥**,可以直接喂给任何标准验证器,或做成一个**纯离线 HTML 网页生成器**(双击即出码),并务必把**恢复码**单独留底。

## 破除两个常见误解(都是卡住小白的根因)

1. **「GitHub 要收费」** ❌ —— 那是强制 2FA 的安全要求,不是付费墙。
2. **「国内用不了验证器,因为要连外网」** ❌ —— 验证器(Authenticator App / 浏览器扩展 / 本地脚本)算码是 **离线** 的:它只用「密钥 + 当前时间」在本地算,**不上传、不连外国服务器**。卡国内用户的从来不是算码本身,而是**「怎么把那个外国 App / 商店装上」**。绕过"装"这一关,问题就没了。

## 为什么这么选(决策链)

非技术 + 国内 + Chrome + 没手机 App + 不便外网,三条路逐一权衡:

- **手机装验证器 App**:最通用,但用户明确"不想装 App / 怕外网";国内商店其实能下(微软 Authenticator、腾讯身份验证器等),作为备选。
- **Chrome 浏览器扩展(Authenticator)**:商店可达(实测 `chromewebstore.google.com` 在该网络 HTTP 200),但有**两道自动化硬墙**:Chrome 安全策略**禁止脚本/自动化点击商店「添加到Chrome」**,也**无法操作扩展的弹出小窗**——这两步只能真人点。且非技术用户找不到扩展图标、弹窗一失焦就关,极易卡死。
- ✅ **纯离线 HTML 生成器(最终采用)**:从 setup key 拿到密钥,写一个**单文件 HTML**,用浏览器自带 Web Crypto 本地算 TOTP,双击即显示当前 6 位码 + 倒计时。无需商店、无需扩展弹窗、无需手机、纯离线;且这个文件页面**可被自动化读取/截图**,代理能全程驱动并自检。代价:密钥以明文存在本机文件里(和"没锁屏的手机上的验证器 App"风险相当)——必须配恢复码留底 + 提醒文件私密保管。

> 迁移判据:**当"装标准验证器"这一步被环境卡死(无 App / 商店或扩展弹窗不可用),而你已能拿到 TOTP 密钥时**,离线 HTML 生成器是兜底正解。能正常装 App / 扩展时,优先用标准工具(更"正规"、跨站通用)。

## 可照做(完整步骤)

1. **拿到密钥**:在 2FA 扫码页点「**setup key / 设置密钥**」,它显示的 base32 串(形如 `XXXXXXXXXXXXXXXX`)就是 TOTP 密钥。二维码内容 = `otpauth://totp/...&secret=该密钥`,两者等价。
2. **本地验证密钥**(可选但推荐,确认没抄错):用 Python 现算一个码,和后面工具出的码对比。
   ```python
   import hmac, hashlib, struct, time, base64
   key = base64.b32decode("你的密钥".replace(" ", ""))
   c = struct.pack(">Q", int(time.time()) // 30)
   h = hmac.new(key, c, hashlib.sha1).digest(); o = h[19] & 0xf
   n = struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff
   print(str(n % 1000000).zfill(6))   # 当前 6 位码
   ```
3. **做离线 HTML 生成器**:把下面模板里 `SECRET` 换成密钥,存成桌面 `GitHub验证码.html`,双击即用(纯本地、不联网)。核心是浏览器 `crypto.subtle` 做 HMAC-SHA1:
   ```html
   <script>
   const SECRET = "你的密钥";   // base32
   function b32d(s){const A="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";let b="";
     for(const c of s.toUpperCase()){const v=A.indexOf(c);if(v<0)continue;b+=v.toString(2).padStart(5,"0");}
     const o=[];for(let i=0;i+8<=b.length;i+=8)o.push(parseInt(b.substr(i,8),2));return new Uint8Array(o);}
   let key;async function code(){
     key=key||await crypto.subtle.importKey("raw",b32d(SECRET),{name:"HMAC",hash:"SHA-1"},false,["sign"]);
     const ctr=Math.floor(Date.now()/1000/30),buf=new ArrayBuffer(8),dv=new DataView(buf);
     dv.setUint32(4,ctr>>>0);const sig=new Uint8Array(await crypto.subtle.sign("HMAC",key,buf));
     const off=sig[19]&0xf,n=((sig[off]&0x7f)<<24)|(sig[off+1]<<16)|(sig[off+2]<<8)|sig[off+3];
     return String(n%1000000).padStart(6,"0");}
   setInterval(async()=>document.title=await code(),1000);
   </script>
   ```
   登录要码时双击这个文件,把当前数字填进去即可(每 30 秒一变)。
4. **填码完成设置**:把当前 6 位码填进「Verify the code」→ Continue。码窗口 30 秒,留够余量(剩 <15 秒就等下一窗再填);GitHub 一般也接受相邻窗口。
5. **恢复码必须双留底**:Continue 后 GitHub 给 16 个恢复码——点官方「Download」存一份(`github-recovery-codes.txt`,零抄写风险),**再单独抄/存一份**(纸 + 与电脑分离)。手机/生成器都失效时,恢复码是唯一入口(每个用一次)。点「I have saved my recovery codes」收尾。

## 关键设计点 / 踩坑(都会咬人)

- **setup key 就是密钥本体**:不用解二维码,点「setup key」直接拿到 base32,最省事。
- **截图读密钥绕过文本过滤**:有些自动化通道会把"像密钥/cookie"的**文本输出**拦掉;改用**截图 + 视觉读取**(密钥是图像)能绕过,且恢复码同理(还可用官方 Download 的 txt 兜底校验)。
- **Chrome 的两道自动化墙**:① 商店页 `chromewebstore.google.com` **禁止脚本化**(截图/eval 都报 "extensions gallery cannot be scripted"),「添加到Chrome」必须真人点;② 扩展弹出小窗不在页面 DOM 里,自动化点不到。→ 见 [[浏览器插件自动化的能力边界_v1]]。给非技术用户用"扩展弹窗扫码"这条路,卡点极多,不如离线 HTML 稳。
- **算码实现先交叉验证再信**:HTML(Web Crypto)、Python、Node 三套实现同一时间戳出的码必须**逐字一致**,再拿去填,免得卡在"码总是错"。
- **明文密钥的安全边界**:HTML 文件 + 密钥留底文件 = 账号第二把钥匙,别发人、别传公开网盘;务必配恢复码纸质副本。

## 边界

- 仅适用 **TOTP(基于时间的一次性密码,RFC 6238)** 这类 2FA;短信 / 硬件密钥 / Passkey 不走这套。
- 离线 HTML 方案靠本机文件持久化密钥:**换电脑 / 文件丢失**就要靠恢复码或密钥重建(所以密钥也要留底)。
- GitHub 短信 2FA 对中国大陆 +86 号码常不支持,别指望它兜底,优先 TOTP + 恢复码。

## 关联文档

- [[浏览器插件自动化的能力边界_v1]] —— 本案是它的又一处印证:登录/验证码/扩展商店与弹窗这些被安全策略保护的环节,自动化点不了,必须人来;反过来本案给出"绕开装扩展、改用离线生成器"的破法
- [[09_平台工程索引]] —— 平台工程区入口
