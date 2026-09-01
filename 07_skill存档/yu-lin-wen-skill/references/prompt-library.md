# Image2 鱼鳞纹修复提示词库

按诊断结果选择一个阶段使用。花括号内容应替换成当前图片的真实信息。

## 1. 直接修复模板

```text
Use case: precise-object-edit / restoration.

图片1是唯一编辑目标。{其他图片及其角色，例如：图片2只用于参考景深和光影，不得复制其中的界面元素。}

请基于图片1进行忠实修复，不要重新设计或重新解释画面。只修改鱼鳞纹、蜂窝纹、重复薄片、噪点、过度微细节和错误焦点。

严格保留：{画幅比例、镜头位置、人物身份、面部、姿势、手势、道具数量与位置、主体大小、场景结构、主要物体位置、配色、光影方向、材质基调和风向}。

材质修复：彻底移除鱼鳞、蜂窝、多边形、叶片砖块、甲片、网格、碎玻璃、密集丝带和重复小片。将 {问题材质} 重建为少量宽幅、连续的 {丝绸/薄纱/皮肤/金属/其他真实材质} 平面，只保留优雅的大褶皱、长轮廓和低频光影渐变。保持原有体积、透光和整体轮廓。

画质：smooth shading, soft lighting, controlled details, minimal microtexture, high clarity, refined edges, smooth gradients, clean tonal transitions, restrained detail density.

禁止：noise, grain, artifacts, compression traces, high-frequency detail, dirty texture, oversharpening, blotchy details, chaotic details, ultra high detail, hyper-detailed microtexture, fish scales, cellular texture, repetitive polygon patterns, overlapping tiles, text, logo, watermark, interface arrows, extra characters, extra objects.
```

## 2. AO 白模模板

```text
Use case: precise-object-edit / AO clay reconstruction.

图片1是唯一几何、构图、轮廓、姿势和镜头参考。生成完全相同场景的中性灰白 AO 白模；这是中间重建图，不是新作品。

严格保留：{画幅、镜头、人物身份结构、姿势、手、头发大轮廓、道具、主体比例与位置、场景大结构、所有主要物体关系、问题材质的整体轮廓与运动方向}。

只简化问题表面：把 {问题材质} 重建为少量宽幅、连续、平滑的曲面和大褶皱；彻底去除鱼鳞几何、叶片砖块、蜂窝多边形、重复甲片、蕾丝、网格、裂纹、碎片和过多细丝。

渲染为无纹理哑光白色黏土材质，平滑阴影，柔和大面积照明，仅在大结构接触处保留轻柔 AO，细节受控、极少纹理、边缘干净、渐变平顺。

禁止：颜色、印刷纹理、鱼鳞、蜂窝、噪点、颗粒、脏污、高频细节、过度锐化、斑驳阴影、文字、logo、水印、界面箭头、新角色、新道具。
```

## 3. AO 材质回填模板

```text
Use case: precise-object-edit / material reconstruction.

图片1是 AO 白模，是唯一几何、构图、姿势、轮廓、镜头和景深目标。图片2是原始彩图，只用于参考配色、材质类别、光线方向、氛围和风格；禁止复制图片2中的鱼鳞、蜂窝或重复薄片。

仅重绘白模的色彩、材质、纹理与光影，不重建几何，不重新设计物体。

回填：{逐项描述环境颜色、主体颜色、光源颜色、材质、透光方式和反射关系}。保持白模的宽幅连续曲面，只允许少量长褶线和低频渐变。

使用 smooth shading, soft lighting, controlled details, minimal microtexture, high clarity, refined edges, smooth gradients。

禁止生成重复碎片、鳞片、叶片、羽毛、蜂窝、多边形、网格、裂纹、甲片或密集丝带。禁止噪点、颗粒、伪影、高频细节、脏污、过锐、文字、logo、水印、界面元素、新角色、新道具。
```

## 4. 最终清理模板

```text
Use case: precise-object-edit / final restoration.

图片1是唯一编辑目标。这不是新生成。

请基于上传图片进行整体修复，不要重新生成或重构画面。严格保留排版、人物外观、面部、动作、场景关系、构图、镜头位置、焦点层次和所有重要物体的位置。

只修改：
1. 移除 {问题区域} 中残留的鱼鳞状、叶片状、蜂窝状、多边形、编织状、网状和砖片状重复结构。
2. 将残余碎片合并为少量宽幅、连续的 {目标材质} 平面，使用大尺度褶皱、干净连续表面和低频光影渐变。
3. 去除数字噪点、颗粒、压缩痕迹、振铃、斑驳、杂乱微纹理、锯齿边缘和过度锐化。

smooth shading, soft lighting, controlled details, minimal texture, high clarity, refined edges, smooth gradients, clean tonal transitions.

禁止：noise, grain, artifacts, high-frequency detail, dirty texture, oversharpening, blotchy details, chaotic details, fish scales, cellular polygons, cracked glass, lace, netting, repeated tiles, UI arrows, text, logo, watermark, new characters, new objects.
```

## 5. 人物主体景深模块

```text
人物是唯一主焦点。人物面部、上半身、双手、关键道具和主要服装轮廓清晰干净，但禁止人工锐化。近镜头的前景遮挡物、画面最外侧结构和最近处地面反射柔和虚化；远处光源、建筑和背景植被轻柔失焦。85mm 电影人像镜头感，焦平面落在人物身上，浅至中等景深，焦点自然渐落，禁止全画面同时锐利。

The character is the only primary focus. The face, upper torso, hands, key prop, and main clothing contours are cleanly resolved without artificial sharpening. Nearby foreground occluders, extreme side structures, and the closest ground reflection are softly defocused; distant light sources, architecture, and foliage are gently soft. 85mm cinematic portrait-lens character, a clear focus plane on the subject, shallow-to-moderate depth of field, smooth optical focus falloff, never sharp everywhere.
```

## 6. 预防性生图规则

### 6.1 生成前预检

删除或改写以下高风险表达：

- 大量重叠薄片
- 无数膜片或碎片
- 数百层复杂细丝
- 密集破碎边缘
- 极致微细节、全画面锐利
- ultra high detail, hyper-detailed, extreme detail
- intricate microtexture, countless fragments, hundreds of layers
- razor sharp everywhere, complex high-frequency surface detail

不要只删除质量词，也要删除会把柔软材质实体化成重复单元的数量与结构语义。

### 6.2 正向材质替换模块

```text
少量宽幅、连续的半透明材质层；修长的大褶皱；干净的连续表面；低频、平滑的透光渐变；外轮廓随运动延伸，但内部纹理克制。

A limited number of broad, continuous translucent material planes; elongated large-scale folds; clean uninterrupted surfaces; low-frequency smooth transmission gradients; the outer silhouette follows the motion while internal microtexture remains restrained.
```

### 6.3 普通新图质量控制模块

根据画面需要酌情选取，不要求全部堆叠：

```text
smooth shading, soft lighting, controlled details, minimal microtexture, high clarity on the subject, refined edges, smooth gradients, clean tonal transitions, restrained detail density

no noise, grain, artifacts, compression traces, high-frequency detail, dirty texture, oversharpening, blotchy details, chaotic details
```

中文版本：

```text
平滑光影效果、柔和照明处理、细节控制得当、纹理简约、主体清晰度高、边缘处理精细、渐变过渡平滑。

禁止：噪点、颗粒感、人为痕迹、压缩伪影、高频细节、脏乱纹理、过度锐化、斑点状细节、杂乱细节。
```

不要写“清晰度极高、全画面锐利”。应写明人物、产品或关键物体是清晰焦平面，前后景按镜头需要自然柔化。

### 6.4 完整预防性生图尾段

```text
Material structure: use a limited number of broad continuous surfaces and elongated large-scale folds. Keep internal microtexture restrained and transitions clean. Avoid repeated small closed units or dense layered fragments.

Quality: smooth shading, controlled details, minimal microtexture, high clarity on the primary subject, refined edges, smooth gradients, clean tonal transitions, restrained detail density.

Prohibit: noise, grain, artifacts, compression traces, high-frequency detail, dirty texture, oversharpening, blotchy or chaotic details, ultra high detail, hyper-detailed microtexture, countless fragments, hundreds of layers, razor sharp everywhere.
```

### 6.5 出图后判别与分流

- 只有噪点、颗粒、过锐或局部斑驳：进入直接修复。
- 已形成重复闭合轮廓、蜂窝、多边形、叶片砖块、甲片或网格：判定为结构型问题，进入 AO 三步修复。
- 用户要求光影、材质和镜头严格不变：优先进入光影保真流程，从原图做局部修补，不先做 AO。
- 第一轮生成正确时立即停止，不追加“最终美化”或“再增强细节”。

## 7. 光影保真流程模板

仅当用户明确要求材质、质感、光影、影调、色彩基调和镜头效果严格不变时使用。优先对原图做一次保守局部修复，不强制多轮生成。

### 7.1 原图单次局部修复（首选）

```text
Use case: precise-object-edit / local defect retouching.

图片1是唯一编辑目标和唯一视觉参考。执行保守的局部修补，不重新设计、不重建材质，也不生成新画面。

只修改一个问题：擦除 {问题材质} 内部形成鱼鳞、蜂窝、叶片砖块或蜂窝结构的小型重复闭合轮廓线与内部接缝。每一条被擦除的小接缝，使用该位置紧邻区域原有的颜色和亮度进行修补。保留所有大块暗带、亮部、褶皱脊线、透光开口、外轮廓和运动线。不要合并、重塑或重建大块材质。

像素区域不可变量：保持原图低频亮度场与色彩场，严格保留曝光、黑位、白位、局部对比、色相、饱和度、亮部覆盖、暗部覆盖、高光与阴影的位置和边界、轮廓光宽度、透光范围和强度、主光源亮度、环境亮部、建筑暗部、地面/水面反射、空气透视、景深、焦点、前景虚化、背景虚化和光学柔度。

严格保留：{材质类别、质感、构图、镜头、人物、面部、姿势、道具、全部物体位置、轮廓、运动方向、影调、色彩基调和镜头效果}。

禁止：重新打光、重新调色、色调映射、平滑大块光影、全局提亮或压暗、增强对比、增加发光、改变透明度、改变材质类别、重画大褶皱、改变反射、改变焦点或模糊、添加元素，以及删除小型重复闭合接缝之外的任何内容。
```

### 7.2 可选结构参考回退

仅当 7.1 仍残留明显结构型鱼鳞纹时使用。重新从原始问题图开始，不串联上一轮生成结果。

```text
Use case: precise-object-edit / light-locked material repair.

图片1是原始问题图：唯一编辑目标，也是构图、人物、材质、质感、亮度、颜色、曝光、阴影、高光、透光、倒影、影调和镜头效果的绝对母版。
图片2是无鳞结构参考：只参考连续表面与大褶皱尺度；绝对禁止参考图片2的亮度、颜色、曝光、光源、反射、影调和景深。

只把 {问题区域} 的重复小型鱼鳞拓扑替换为连续 {目标材质}，沿用图片1的大轮廓、体积和运动方向。逐区域保持图片1的低频亮度与色彩、亮暗覆盖、高光、阴影、轮廓光、透光、反射和全部镜头效果。

禁止 relight, repaint lighting, soft lighting, studio lighting, premium glow, clean luminous look, brighter subject, darker subject, color grading, tone mapping, global contrast adjustment, exposure change, broad emissive glow，以及任何新增元素。
```

### 7.3 分区验收与停止规则

生成后逐区比较主体、问题材质、背景主光源、环境亮部、建筑暗部和地面/水面反射。检查曝光、亮暗覆盖、色温、饱和度、反射范围、焦点和虚实关系。

- 鱼鳞消失且光影接近：立即采用，停止生成。
- 鱼鳞仍在但光影正确：可从原图重新执行一次更局部的 7.1。
- 光影、材质或镜头明显漂移：淘汰结果，回到原图；不要在漂移结果上继续“校正光影”。
