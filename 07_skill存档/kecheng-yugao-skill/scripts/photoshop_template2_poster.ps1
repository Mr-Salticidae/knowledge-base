[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$SourcePsd,
    [Parameter(Mandatory = $true)][string]$PortraitPng,
    [Parameter(Mandatory = $true)][string]$OutPsd,
    [Parameter(Mandatory = $true)][string]$OutPng,
    [Parameter(Mandatory = $true)][string]$TitleLine1,
    [Parameter(Mandatory = $true)][string]$TitleLine2,
    [Parameter(Mandatory = $true)][string]$TitleLine3,
    [Parameter(Mandatory = $true)][string]$Subtitle,
    [Parameter(Mandatory = $true)][string]$DateText,
    [Parameter(Mandatory = $true)][string]$TimeText,
    [Parameter(Mandatory = $true)][string]$DeliveryLabel,
    [Parameter(Mandatory = $true)][string]$TeacherText,
    [Parameter(Mandatory = $true)][string]$Tool1,
    [Parameter(Mandatory = $true)][string]$Tool2,
    [Parameter(Mandatory = $true)][string]$Tool3,
    [Parameter(Mandatory = $true)][string]$Tool4,
    [Parameter(Mandatory = $true)][string]$Icon1Png,
    [Parameter(Mandatory = $true)][string]$Icon2Png,
    [Parameter(Mandatory = $true)][string]$Icon3Png,
    [Parameter(Mandatory = $true)][string]$Icon4Png,
    [Parameter(Mandatory = $true)][string]$Objective1,
    [Parameter(Mandatory = $true)][string]$Objective2,
    [Parameter(Mandatory = $true)][string]$Objective3,
    [Parameter(Mandatory = $true)][string]$Homework1,
    [Parameter(Mandatory = $true)][string]$Homework2,
    [string]$OutAudit
)

$ErrorActionPreference = 'Stop'

function Resolve-OutputPath([string]$Path, [string]$Extension) {
    $resolved = [System.IO.Path]::GetFullPath($Path)
    if ([System.IO.Path]::GetExtension($resolved).ToLowerInvariant() -ne $Extension) {
        throw "Output path must end in $Extension`: $resolved"
    }
    if (Test-Path -LiteralPath $resolved) {
        throw "Refusing to overwrite existing output: $resolved"
    }
    $parent = Split-Path -Parent $resolved
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }
    return $resolved
}

$source = (Resolve-Path -LiteralPath $SourcePsd).Path
$portrait = (Resolve-Path -LiteralPath $PortraitPng).Path
if ([System.IO.Path]::GetExtension($source).ToLowerInvariant() -ne '.psd') {
    throw "Source must be a PSD: $source"
}
if ([System.IO.Path]::GetExtension($portrait).ToLowerInvariant() -ne '.png') {
    throw "Portrait must be a PNG: $portrait"
}
$iconPaths = @($Icon1Png, $Icon2Png, $Icon3Png, $Icon4Png) | ForEach-Object {
    $resolvedIcon = (Resolve-Path -LiteralPath $_).Path
    if ([System.IO.Path]::GetExtension($resolvedIcon).ToLowerInvariant() -ne '.png') {
        throw "Tool icon must be a PNG: $resolvedIcon"
    }
    $resolvedIcon
}
$outPsdResolved = Resolve-OutputPath $OutPsd '.psd'
$outPngResolved = Resolve-OutputPath $OutPng '.png'
if ($source -eq $outPsdResolved) { throw 'Refusing to overwrite the source PSD.' }
[System.IO.File]::Copy($source, $outPsdResolved, $false)

$textValues = @{
    TitleLine1 = $TitleLine1; TitleLine2 = $TitleLine2; TitleLine3 = $TitleLine3; Subtitle = $Subtitle
    DateText = $DateText; TimeText = $TimeText; DeliveryLabel = $DeliveryLabel; TeacherText = $TeacherText
    Tool1 = $Tool1; Tool2 = $Tool2; Tool3 = $Tool3; Tool4 = $Tool4
    Objective1 = $Objective1; Objective2 = $Objective2; Objective3 = $Objective3
    Homework1 = $Homework1; Homework2 = $Homework2
}
foreach ($key in $textValues.Keys) {
    if ([string]::IsNullOrWhiteSpace([string]$textValues[$key])) {
        throw "Required text is empty: $key"
    }
}

$app = $null
$photoshopWasRunning = [bool](Get-Process -Name Photoshop -ErrorAction SilentlyContinue)
$completed = $false
try {
    $app = New-Object -ComObject Photoshop.Application
    $psdLiteral = ConvertTo-Json -Compress $outPsdResolved
    $pngLiteral = ConvertTo-Json -Compress $outPngResolved
    $portraitLiteral = ConvertTo-Json -Compress $portrait
    $icon1Literal = ConvertTo-Json -Compress $iconPaths[0]
    $icon2Literal = ConvertTo-Json -Compress $iconPaths[1]
    $icon3Literal = ConvertTo-Json -Compress $iconPaths[2]
    $icon4Literal = ConvertTo-Json -Compress $iconPaths[3]
    $jsonTextLiteral = ConvertTo-Json -Compress ($textValues | ConvertTo-Json -Compress)

    $jsx = @"
var previousDialogs = app.displayDialogs;
app.displayDialogs = DialogModes.NO;
var doc = null;
var smartDoc = null;
var portraitDoc = null;
var outputText = null;
try {
    // Photoshop's legacy ExtendScript engine does not always expose JSON.parse.
    var values = eval('(' + $jsonTextLiteral + ')');

    function q(value) {
        return '"' + String(value).replace(/\\/g, '\\\\').replace(/"/g, '\\"')
            .replace(/\r/g, '\\r').replace(/\n/g, '\\n').replace(/\t/g, '\\t') + '"';
    }
    function toJson(value) {
        if (value === null || value === undefined) return 'null';
        if (typeof value === 'string') return q(value);
        if (typeof value === 'number') return isFinite(value) ? String(value) : 'null';
        if (typeof value === 'boolean') return value ? 'true' : 'false';
        if (value instanceof Array) {
            var av = []; for (var ai = 0; ai < value.length; ai++) av.push(toJson(value[ai]));
            return '[' + av.join(',') + ']';
        }
        var ov = []; for (var k in value) if (value.hasOwnProperty(k)) ov.push(q(k) + ':' + toJson(value[k]));
        return '{' + ov.join(',') + '}';
    }
    function normalizeText(v) { return String(v).replace(/\s+/g, '').toLowerCase(); }
    function boundsPx(layer) {
        return {left:Number(layer.bounds[0].as('px')), top:Number(layer.bounds[1].as('px')),
            right:Number(layer.bounds[2].as('px')), bottom:Number(layer.bounds[3].as('px'))};
    }
    function findLayer(container, id) {
        for (var i = 0; i < container.layers.length; i++) {
            var layer = container.layers[i];
            if (layer.id === id) return layer;
            if (layer.typename === 'LayerSet') {
                var nested = findLayer(layer, id); if (nested) return nested;
            }
        }
        return null;
    }
    function requireLayer(id, label) {
        var layer = findLayer(doc, id); if (!layer) throw new Error(label + ' layer missing: ' + id); return layer;
    }
    function updateText(id, expected, target, label, maxWidth, fixedSize) {
        var layer = requireLayer(id, label);
        if (layer.typename !== 'ArtLayer' || layer.kind !== LayerKind.TEXT) throw new Error(label + ' is not text');
        var before = String(layer.textItem.contents);
        if (normalizeText(before) !== normalizeText(expected)) throw new Error(label + ' source mismatch: ' + before);
        layer.textItem.contents = target;
        if (fixedSize) layer.textItem.size = UnitValue(fixedSize, 'pt');
        var b = boundsPx(layer);
        if (maxWidth && b.right - b.left > maxWidth) {
            var sizeBefore = Number(layer.textItem.size.as('pt'));
            layer.textItem.size = UnitValue(Math.max(16, sizeBefore * maxWidth / (b.right - b.left)), 'pt');
            b = boundsPx(layer);
        }
        layer.name = label;
        return {layer_id:id, before:before, after:String(layer.textItem.contents), bounds:b};
    }
    function color(r,g,b) { var c = new SolidColor(); c.rgb.red=r; c.rgb.green=g; c.rgb.blue=b; return c; }
    function fillRect(group, name, x1,y1,x2,y2, fillColor, opacity) {
        var layer = group.artLayers.add(); layer.name = name; layer.opacity = opacity;
        doc.activeLayer = layer;
        doc.selection.select([[x1,y1],[x2,y1],[x2,y2],[x1,y2]]);
        doc.selection.fill(fillColor, ColorBlendMode.NORMAL, 100, false); doc.selection.deselect();
        return layer;
    }
    function fillPolygon(group, name, points, fillColor, opacity, noiseAmount) {
        var layer = group.artLayers.add(); layer.name = name; layer.opacity = opacity;
        doc.activeLayer = layer; doc.selection.select(points);
        doc.selection.fill(fillColor, ColorBlendMode.NORMAL, 100, false); doc.selection.deselect();
        if (noiseAmount) {
            try { layer.applyAddNoise(noiseAmount, NoiseDistribution.UNIFORM, true); } catch (noiseError) {}
        }
        return layer;
    }
    function jaggedRectPoints(left, top, right, bottom, step, jitter) {
        var points=[], x, y;
        for(x=left;x<right;x+=step) points.push([x,top+(Math.random()*2-1)*jitter]);
        points.push([right,top+(Math.random()*2-1)*jitter]);
        for(y=top+step;y<bottom;y+=step) points.push([right+(Math.random()*2-1)*jitter,y]);
        points.push([right+(Math.random()*2-1)*jitter,bottom]);
        for(x=right-step;x>left;x-=step) points.push([x,bottom+(Math.random()*2-1)*jitter]);
        points.push([left,bottom+(Math.random()*2-1)*jitter]);
        for(y=bottom-step;y>top;y-=step) points.push([left+(Math.random()*2-1)*jitter,y]);
        return points;
    }
    function offsetPoints(points, dx, dy) {
        var shifted=[]; for(var i=0;i<points.length;i++) shifted.push([points[i][0]+dx,points[i][1]+dy]);
        return shifted;
    }
    function addText(group, name, content, x, y, size, fillColor, justification, maxWidth, fontName, minSize) {
        var layer = group.artLayers.add(); layer.kind = LayerKind.TEXT; layer.name = name;
        var item = layer.textItem; item.contents = content; item.size = UnitValue(size, 'pt');
        try { item.font = fontName || 'MicrosoftYaHei-Bold'; }
        catch (fontError) { try { item.font = 'NotoSansSC-Black'; } catch (ignore) {} }
        item.color = fillColor; item.justification = justification; item.position = [UnitValue(x,'px'),UnitValue(y,'px')];
        var b = boundsPx(layer);
        if (maxWidth && b.right - b.left > maxWidth) {
            item.size = UnitValue(Math.max(minSize || 22, size * maxWidth / (b.right - b.left)), 'pt'); b = boundsPx(layer);
        }
        return {bounds:b, font:String(item.font), size_pt:Number(item.size.as('pt')), text:String(item.contents)};
    }
    function placePng(group, name, filePath, cx, cy, maxWidth, maxHeight) {
        var iconDoc = app.open(new File(filePath));
        iconDoc.selection.selectAll(); iconDoc.selection.copy(true); iconDoc.close(SaveOptions.DONOTSAVECHANGES);
        app.activeDocument = doc; var layer = doc.paste(); layer.name = name;
        try { layer.move(group, ElementPlacement.INSIDE); } catch (moveError) {}
        var b = boundsPx(layer); var w = b.right-b.left, h = b.bottom-b.top;
        var scale = Math.min(maxWidth/w, maxHeight/h) * 100;
        layer.resize(scale, scale, AnchorPosition.MIDDLECENTER); b = boundsPx(layer);
        layer.translate(UnitValue(cx-(b.left+b.right)/2,'px'), UnitValue(cy-(b.top+b.bottom)/2,'px'));
        return {bounds:boundsPx(layer),source:filePath};
    }
    function addSpeckles(group, name, x1, y1, x2, y2, fillColor, count) {
        var layer = group.artLayers.add(); layer.name = name; layer.opacity = 72; doc.activeLayer = layer;
        for (var i=0; i<count; i++) {
            var w = 2 + Math.random()*10, h = 1 + Math.random()*4;
            var x = x1 + Math.random()*(x2-x1-w), y = y1 + Math.random()*(y2-y1-h);
            doc.selection.select([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]);
            doc.selection.fill(fillColor, ColorBlendMode.NORMAL, 100, false); doc.selection.deselect();
        }
        return layer;
    }

    var psdFile = new File($psdLiteral);
    var pngFile = new File($pngLiteral);
    doc = app.open(psdFile);
    if (Number(doc.width.as('px')) !== 1080 || Number(doc.height.as('px')) !== 1920) throw new Error('Template canvas mismatch');

    requireLayer(101, '\u65e7\u4e3b\u6807\u9898\u56fe\u5c42').visible = false;
    requireLayer(249, '\u65e7\u526f\u6807\u9898\u56fe\u5c42').visible = false;
    requireLayer(129, '\u65e7\u5de5\u5177\u56fe\u68071').visible = false;
    requireLayer(128, '\u65e7\u5de5\u5177\u56fe\u68072').visible = false;
    requireLayer(127, '\u65e7\u5de5\u5177\u56fe\u68073').visible = false;
    requireLayer(126, '\u65e7\u5de5\u5177\u56fe\u68074').visible = false;
    requireLayer(64, '\u65e7\u5de5\u5177\u6587\u5b571').visible = false;
    requireLayer(222, '\u65e7\u5de5\u5177\u6587\u5b572').visible = false;
    requireLayer(223, '\u65e7\u5de5\u5177\u6587\u5b573').visible = false;
    requireLayer(224, '\u65e7\u5de5\u5177\u6587\u5b574').visible = false;

    var changes = {};
    changes.date = updateText(58, '08/12', values.DateText, 'T2_\u65e5\u671f', 260);
    changes.time = updateText(59, '\u5468\u4e09 19:00', values.TimeText, 'T2_\u65f6\u95f4', 270);
    changes.delivery = updateText(231, '\u8bfe\u7a0b\u65f6\u95f4', values.DeliveryLabel, 'T2_\u6388\u8bfe\u5f62\u5f0f', 175);
    changes.teacher = updateText(61, 'JELLY', values.TeacherText, 'T2_\u8bb2\u5e08', 190);
    changes.objectives = [
        updateText(40, '\u62c6\u89e3\u9ad8\u8d28\u611f\u4ea7\u54c1\u56fe\u7684\u6784\u56fe\u4e0e\u89c6\u89c9\u5c42\u7ea7', values.Objective1, 'T2_\u8bfe\u7a0b\u76ee\u6807_1', 535, 30),
        updateText(42, '\u51c6\u786e\u8868\u73b0\u4ea7\u54c1\u7684\u6750\u8d28\u3001\u5149\u5f71\u4e0e\u7ec6\u8282', values.Objective2, 'T2_\u8bfe\u7a0b\u76ee\u6807_2', 535, 30),
        updateText(159, '\u638c\u63e1\u4ea7\u54c1\u56fe\u63d0\u793a\u8bcd\u7684\u64b0\u5199\u4e0e\u4f18\u5316\u65b9\u6cd5', values.Objective3, 'T2_\u8bfe\u7a0b\u76ee\u6807_3', 535, 30)
    ];
    changes.homework = [
        updateText(74, '1\u5957\u53ef\u7528\u4e8e\u4f5c\u54c1\u96c6\u7684AI\u4ea7\u54c1\u7ec6\u8282\u56fe', values.Homework1, 'T2_\u8bfe\u7a0b\u4f5c\u4e1a_1', 625, 28),
        updateText(75, '1\u5957\u53ef\u590d\u7528\u7684\u4ea7\u54c1\u56fe\u63d0\u793a\u8bcd\u4e0e\u5236\u4f5c\u6d41\u7a0b', values.Homework2, 'T2_\u8bfe\u7a0b\u4f5c\u4e1a_2', 625, 28)
    ];

    var portraitLayer = requireLayer(35, '\u4eba\u7269\u667a\u80fd\u5bf9\u8c61');
    if (portraitLayer.typename !== 'ArtLayer' || portraitLayer.kind !== LayerKind.SMARTOBJECT) throw new Error('Portrait contract mismatch');
    doc.activeLayer = portraitLayer;
    executeAction(stringIDToTypeID('placedLayerEditContents'), undefined, DialogModes.NO);
    smartDoc = app.activeDocument;
    if (smartDoc === doc) throw new Error('Portrait smart object did not open');
    for (var si = 0; si < smartDoc.layers.length; si++) smartDoc.layers[si].visible = false;
    portraitDoc = app.open(new File($portraitLiteral));
    portraitDoc.selection.selectAll(); portraitDoc.selection.copy(true); portraitDoc.close(SaveOptions.DONOTSAVECHANGES); portraitDoc = null;
    app.activeDocument = smartDoc; var pasted = smartDoc.paste(); pasted.name = 'T2_\u4eba\u7269_\u900f\u660ePNG';
    var pb = boundsPx(pasted); var pw = pb.right-pb.left; var ph = pb.bottom-pb.top;
    var scale = Math.min(735/pw, 930/ph) * 100; pasted.resize(scale, scale, AnchorPosition.MIDDLECENTER);
    pb = boundsPx(pasted);
    pasted.translate(UnitValue((Number(smartDoc.width.as('px'))-(pb.right-pb.left))/2-pb.left,'px'), UnitValue(Number(smartDoc.height.as('px'))-pb.bottom,'px'));
    var portraitInnerBounds = boundsPx(pasted);
    smartDoc.save(); smartDoc.close(SaveOptions.SAVECHANGES); smartDoc = null;
    app.activeDocument = doc;

    var titleGroup = doc.layerSets.add(); titleGroup.name = 'T2_\u8bfe\u7a0b\u6807\u9898_\u53ef\u7f16\u8f91';
    var white = color(250,249,245), black = color(12,12,12), blue = color(35,80,210), lime = color(190,232,0), silver = color(215,216,214), shadow = color(35,42,58);
    var paper1=jaggedRectPoints(82,142,842,342,22,8);
    var paper2=jaggedRectPoints(78,331,982,520,22,9);
    var paper3=jaggedRectPoints(156,501,968,700,22,8);
    var tape=jaggedRectPoints(286,692,832,773,18,5);
    fillPolygon(titleGroup,'T2_\u6495\u7eb8\u9634\u5f71_1',offsetPoints(paper1,8,12),shadow,22,0);
    fillPolygon(titleGroup,'T2_\u767d\u8272\u6495\u7eb8_1',paper1,white,100,3);
    fillPolygon(titleGroup,'T2_\u6495\u7eb8\u9634\u5f71_2',offsetPoints(paper2,7,13),shadow,26,0);
    fillPolygon(titleGroup,'T2_\u8367\u5149\u7eff\u6495\u7eb8',paper2,lime,100,4);
    fillPolygon(titleGroup,'T2_\u6495\u7eb8\u9634\u5f71_3',offsetPoints(paper3,8,12),shadow,22,0);
    fillPolygon(titleGroup,'T2_\u767d\u8272\u6495\u7eb8_3',paper3,white,100,3);
    fillPolygon(titleGroup,'T2_\u94f6\u8272\u80f6\u5e26\u9634\u5f71',offsetPoints(tape,7,10),shadow,26,0);
    fillPolygon(titleGroup,'T2_\u94f6\u8272\u80f6\u5e26',tape,silver,96,7);
    var titleFont='NotoSansSC-Black';
    var t1 = addText(titleGroup,'T2_\u6807\u9898_1',values.TitleLine1,540,314,154,black,Justification.CENTER,760,titleFont,100);
    var t2 = addText(titleGroup,'T2_\u6807\u9898_2',values.TitleLine2,540,497,164,black,Justification.CENTER,840,titleFont,100);
    var t3 = addText(titleGroup,'T2_\u6807\u9898_3',values.TitleLine3,540,681,108,blue,Justification.CENTER,800,titleFont,76);
    var ts = addText(titleGroup,'T2_\u526f\u6807\u9898',values.Subtitle,540,758,42,black,Justification.CENTER,500,'NotoSansSC-Black',30);
    addSpeckles(titleGroup,'T2_\u6807\u9898\u505a\u65e7\u7eb9\u7406_1',140,190,930,325,white,22);
    addSpeckles(titleGroup,'T2_\u6807\u9898\u505a\u65e7\u7eb9\u7406_2',120,382,950,498,lime,22);
    addSpeckles(titleGroup,'T2_\u6807\u9898\u505a\u65e7\u7eb9\u7406_3',190,555,930,680,white,18);
    changes.title = {rows:[t1,t2,t3,ts], reference_bounds:{left:67,top:138,right:997,bottom:779}, style:'torn-paper oversized distressed'};

    var markerGroup = doc.layerSets.add(); markerGroup.name = 'T2_\u8f6f\u4ef6\u56fe\u6807_\u7f51\u7edc\u7d20\u6750';
    var toolCenters=[99,246,397,546], cardTop=869, cardBottom=963;
    for(var ci=0;ci<4;ci++) {
        fillRect(markerGroup,'T2_\u56fe\u6807\u5361\u7247\u9634\u5f71_'+(ci+1),toolCenters[ci]-43,cardTop+5,toolCenters[ci]+43,cardBottom+5,shadow,18);
        fillRect(markerGroup,'T2_\u56fe\u6807\u5361\u7247_'+(ci+1),toolCenters[ci]-43,cardTop,toolCenters[ci]+43,cardBottom,white,100);
    }
    var icon1=placePng(markerGroup,'T2_\u56fe\u6807_ChatGPT',$icon1Literal,99,916,60,60);
    var icon2=placePng(markerGroup,'T2_\u56fe\u6807_Gemini',$icon2Literal,246,916,60,60);
    var icon3=placePng(markerGroup,'T2_\u56fe\u6807_CapCut',$icon3Literal,397,916,60,60);
    var icon4=placePng(markerGroup,'T2_\u56fe\u6807_MiniMax',$icon4Literal,546,916,60,60);
    var toolColor=color(23,37,62);
    var toolText1=addText(markerGroup,'T2_\u5de5\u5177_1',values.Tool1,99,998,20,toolColor,Justification.CENTER,125,'NotoSansSC-Bold',16);
    var toolText2=addText(markerGroup,'T2_\u5de5\u5177_2',values.Tool2,246,998,20,toolColor,Justification.CENTER,125,'NotoSansSC-Bold',16);
    var toolText3=addText(markerGroup,'T2_\u5de5\u5177_3',values.Tool3,397,998,20,toolColor,Justification.CENTER,125,'NotoSansSC-Bold',16);
    var toolText4=addText(markerGroup,'T2_\u5de5\u5177_4',values.Tool4,546,998,20,toolColor,Justification.CENTER,125,'NotoSansSC-Bold',16);
    changes.tools={icons:[icon1,icon2,icon3,icon4],labels:[toolText1,toolText2,toolText3,toolText4]};

    var titleBottom = Math.max(t1.bounds.bottom,t2.bounds.bottom,t3.bounds.bottom,ts.bounds.bottom);
    if (titleBottom > 779) throw new Error('Title block exceeds registered lower boundary: ' + titleBottom);
    var titleRows=[t1,t2,t3,ts];
    for(var ti=0;ti<titleRows.length;ti++) {
        var rowCenter=(titleRows[ti].bounds.left+titleRows[ti].bounds.right)/2;
        if(Math.abs(rowCenter-540)>15) throw new Error('Title row center exceeds tolerance: '+rowCenter);
    }
    for (var oi=0; oi<changes.objectives.length; oi++) {
        if (changes.objectives[oi].bounds.right > 690 || changes.objectives[oi].bounds.bottom > 1490) throw new Error('Objective exceeds safe area');
    }
    for (var hi=0; hi<changes.homework.length; hi++) {
        if (changes.homework[hi].bounds.right > 720 || changes.homework[hi].bounds.bottom > 1850) throw new Error('Homework exceeds safe area');
    }

    doc.save();
    var pngOptions = new PNGSaveOptions(); pngOptions.interlaced = false;
    doc.saveAs(pngFile, pngOptions, true, Extension.LOWERCASE);
    outputText = toJson({schema_version:1, source_psd:$psdLiteral, portrait_png:$portraitLiteral,
        output_psd:psdFile.fsName, output_png:pngFile.fsName, poster_editability_grade:'A',
        semantic_mapping:{objectives:'\u5b8c\u6210\u8fd9\u8282\u8bfe\u4f60\u5c06\u5b66\u4f1a',homework:'\u4e0b\u8bfe\u5373\u53ef\u5e26\u8d70'},
        hidden_source_layer_ids:[101,249,129,128,127,126,64,222,223,224], portrait_smart_layer_id:35,
        portrait_inner_bounds:portraitInnerBounds, changes:changes});
    doc.close(SaveOptions.DONOTSAVECHANGES); doc = null;
} finally {
    if (portraitDoc) try { portraitDoc.close(SaveOptions.DONOTSAVECHANGES); } catch(e1) {}
    if (smartDoc) try { smartDoc.close(SaveOptions.DONOTSAVECHANGES); } catch(e2) {}
    if (doc) try { doc.close(SaveOptions.DONOTSAVECHANGES); } catch(e3) {}
    app.displayDialogs = previousDialogs;
}
outputText;
"@
    $resultText = $app.DoJavaScript($jsx)
    $result = $resultText | ConvertFrom-Json
    $result | Add-Member source_sha256 ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant())
    $result | Add-Member portrait_sha256 ((Get-FileHash -LiteralPath $portrait -Algorithm SHA256).Hash.ToLowerInvariant())
    $result | Add-Member icon_sha256 (@($iconPaths | ForEach-Object {
        [pscustomobject]@{
            path = $_
            sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }))
    $result | Add-Member edited_at_utc ([DateTime]::UtcNow.ToString('o'))
    $formatted = $result | ConvertTo-Json -Depth 14
    if ($OutAudit) {
        $auditPath = [System.IO.Path]::GetFullPath($OutAudit)
        $auditParent = Split-Path -Parent $auditPath
        if (-not (Test-Path -LiteralPath $auditParent)) { New-Item -ItemType Directory -Path $auditParent | Out-Null }
        [System.IO.File]::WriteAllText($auditPath, $formatted + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
        Write-Output $auditPath
    } else { Write-Output $formatted }
    $completed = $true
}
finally {
    if (-not $completed) {
        if (Test-Path -LiteralPath $outPsdResolved) { Remove-Item -LiteralPath $outPsdResolved -Force }
        if (Test-Path -LiteralPath $outPngResolved) { Remove-Item -LiteralPath $outPngResolved -Force }
    }
    if ($app -and -not $photoshopWasRunning) { try { $app.Quit() } catch {} }
    if ($app) { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) }
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
