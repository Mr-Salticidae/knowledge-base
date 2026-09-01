[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$SourcePsd,
    [Parameter(Mandatory = $true)][string]$PortraitPng,
    [Parameter(Mandatory = $true)][string]$TeacherText,
    [Parameter(Mandatory = $true)][string]$OutPsd,
    [Parameter(Mandatory = $true)][string]$OutPng,
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
if ([System.IO.Path]::GetExtension($source).ToLowerInvariant() -ne '.psd') { throw "Source must be a PSD: $source" }
if ([System.IO.Path]::GetExtension($portrait).ToLowerInvariant() -ne '.png') { throw "Portrait must be a PNG: $portrait" }
if ([string]::IsNullOrWhiteSpace($TeacherText)) { throw 'TeacherText must not be empty.' }

$outPsdResolved = Resolve-OutputPath $OutPsd '.psd'
$outPngResolved = Resolve-OutputPath $OutPng '.png'
if ($source -eq $outPsdResolved) { throw 'Refusing to overwrite the source PSD.' }
[System.IO.File]::Copy($source, $outPsdResolved, $false)

$app = $null
$photoshopWasRunning = [bool](Get-Process -Name Photoshop -ErrorAction SilentlyContinue)
$completed = $false
try {
    $app = New-Object -ComObject Photoshop.Application
    $psdLiteral = ConvertTo-Json -Compress $outPsdResolved
    $pngLiteral = ConvertTo-Json -Compress $outPngResolved
    $portraitLiteral = ConvertTo-Json -Compress $portrait
    $teacherLiteral = ConvertTo-Json -Compress $TeacherText

    $jsx = @"
var previousDialogs = app.displayDialogs;
app.displayDialogs = DialogModes.NO;
var doc = null;
var smartDoc = null;
var portraitDoc = null;
var outputText = null;
try {
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
        var layer = findLayer(doc, id);
        if (!layer) throw new Error(label + ' layer missing: ' + id);
        return layer;
    }
    function textStyle(layer) {
        var item = layer.textItem;
        var color = item.color.rgb;
        return {
            font:String(item.font),
            size_pt:Number(item.size.as('pt')),
            leading_pt:(item.leading ? Number(item.leading.as('pt')) : null),
            tracking:Number(item.tracking),
            justification:String(item.justification),
            color:{red:Number(color.red),green:Number(color.green),blue:Number(color.blue)},
            position:{x:Number(item.position[0].as('px')),y:Number(item.position[1].as('px'))}
        };
    }
    function closeEnough(a,b) { return Math.abs(Number(a)-Number(b)) < 0.01; }
    function assertStyleSame(before, after, label) {
        if (before.font !== after.font || !closeEnough(before.size_pt,after.size_pt) ||
            !closeEnough(before.leading_pt,after.leading_pt) || before.tracking !== after.tracking ||
            before.justification !== after.justification ||
            !closeEnough(before.color.red,after.color.red) || !closeEnough(before.color.green,after.color.green) ||
            !closeEnough(before.color.blue,after.color.blue) || !closeEnough(before.position.x,after.position.x) ||
            !closeEnough(before.position.y,after.position.y)) {
            throw new Error(label + ' style or position changed');
        }
    }
    function textSnapshot(id, label) {
        var layer = requireLayer(id,label);
        if (layer.typename !== 'ArtLayer' || layer.kind !== LayerKind.TEXT) throw new Error(label + ' is not text');
        return {id:id, text:String(layer.textItem.contents), style:textStyle(layer), bounds:boundsPx(layer), visible:Boolean(layer.visible)};
    }
    function assertFixedTextSame(before, after, label) {
        if (before.text !== after.text || before.visible !== after.visible) throw new Error(label + ' content/visibility changed');
        assertStyleSame(before.style,after.style,label);
        if (!closeEnough(before.bounds.left,after.bounds.left) || !closeEnough(before.bounds.top,after.bounds.top) ||
            !closeEnough(before.bounds.right,after.bounds.right) || !closeEnough(before.bounds.bottom,after.bounds.bottom)) {
            throw new Error(label + ' bounds changed');
        }
    }

    doc = app.open(new File($psdLiteral));
    if (Number(doc.width.as('px')) !== 1080 || Number(doc.height.as('px')) !== 1920) throw new Error('Template canvas mismatch');

    var fixedTitleBefore = [
        textSnapshot(277,'title row 1'),
        textSnapshot(281,'title row 2'),
        textSnapshot(282,'title row 3')
    ];
    var teacherLayer = requireLayer(61,'teacher text');
    if (teacherLayer.typename !== 'ArtLayer' || teacherLayer.kind !== LayerKind.TEXT) throw new Error('Teacher layer is not text');
    if (String(teacherLayer.textItem.contents).replace(/\s+/g,'').toUpperCase() !== 'JELLY') throw new Error('Teacher source text mismatch');
    var teacherBefore = {text:String(teacherLayer.textItem.contents),style:textStyle(teacherLayer),bounds:boundsPx(teacherLayer)};

    var portraitLayer = requireLayer(35,'portrait smart object');
    if (portraitLayer.typename !== 'ArtLayer' || portraitLayer.kind !== LayerKind.SMARTOBJECT) throw new Error('Portrait contract mismatch');
    var portraitOuterBefore = boundsPx(portraitLayer);
    doc.activeLayer = portraitLayer;
    executeAction(stringIDToTypeID('placedLayerEditContents'), undefined, DialogModes.NO);
    smartDoc = app.activeDocument;
    if (smartDoc === doc) throw new Error('Portrait smart object did not open');
    for (var si = 0; si < smartDoc.layers.length; si++) smartDoc.layers[si].visible = false;
    portraitDoc = app.open(new File($portraitLiteral));
    portraitDoc.selection.selectAll(); portraitDoc.selection.copy(true);
    portraitDoc.close(SaveOptions.DONOTSAVECHANGES); portraitDoc = null;
    app.activeDocument = smartDoc;
    var pasted = smartDoc.paste(); pasted.name = '人物_透明PNG';
    var pb = boundsPx(pasted), pw = pb.right-pb.left, ph = pb.bottom-pb.top;
    if (pw <= 0 || ph <= 0) throw new Error('Portrait has empty pixel bounds');
    var scale = Math.min(735/pw, 930/ph) * 100;
    pasted.resize(scale, scale, AnchorPosition.MIDDLECENTER);
    pb = boundsPx(pasted);
    pasted.translate(UnitValue((Number(smartDoc.width.as('px'))-(pb.right-pb.left))/2-pb.left,'px'),
        UnitValue(Number(smartDoc.height.as('px'))-pb.bottom,'px'));
    var portraitInnerBounds = boundsPx(pasted);
    smartDoc.save(); smartDoc.close(SaveOptions.SAVECHANGES); smartDoc = null;
    app.activeDocument = doc;

    teacherLayer = requireLayer(61,'teacher text');
    teacherLayer.textItem.contents = $teacherLiteral;
    var teacherAfter = {text:String(teacherLayer.textItem.contents),style:textStyle(teacherLayer),bounds:boundsPx(teacherLayer)};
    assertStyleSame(teacherBefore.style,teacherAfter.style,'teacher text');

    var fixedTitleAfter = [
        textSnapshot(277,'title row 1'),
        textSnapshot(281,'title row 2'),
        textSnapshot(282,'title row 3')
    ];
    for (var ti=0; ti<fixedTitleBefore.length; ti++) assertFixedTextSame(fixedTitleBefore[ti],fixedTitleAfter[ti],'title row '+(ti+1));
    // Replacing the transparent pixels can change the visible bounds even when the
    // smart-object layer itself was never moved. Record both bounds for QA, but do
    // not treat a content-driven bounds change as a layer-position change.
    var portraitOuterAfter = boundsPx(requireLayer(35,'portrait smart object'));

    doc.save();
    var pngOptions = new PNGSaveOptions(); pngOptions.interlaced = false;
    doc.saveAs(new File($pngLiteral), pngOptions, true, Extension.LOWERCASE);
    outputText = toJson({
        schema_version:1, source_psd:$psdLiteral, portrait_png:$portraitLiteral,
        output_psd:(new File($psdLiteral)).fsName, output_png:(new File($pngLiteral)).fsName,
        changed_layer_ids:[35,61], locked_title_layer_ids:[277,281,282],
        fixed_main_title_region:'90天成为AI全能人才及其他非教师区域保持不变',
        teacher_before:teacherBefore, teacher_after:teacherAfter,
        fixed_title_before:fixedTitleBefore, fixed_title_after:fixedTitleAfter,
        portrait_outer_before:portraitOuterBefore, portrait_outer_after:portraitOuterAfter,
        portrait_inner_bounds:portraitInnerBounds
    });
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
    $result | Add-Member output_psd_sha256 ((Get-FileHash -LiteralPath $outPsdResolved -Algorithm SHA256).Hash.ToLowerInvariant())
    $result | Add-Member edited_at_utc ([DateTime]::UtcNow.ToString('o'))
    $formatted = $result | ConvertTo-Json -Depth 14
    if ($OutAudit) {
        $auditPath = [System.IO.Path]::GetFullPath($OutAudit)
        $auditParent = Split-Path -Parent $auditPath
        if (-not (Test-Path -LiteralPath $auditParent)) { New-Item -ItemType Directory -Path $auditParent | Out-Null }
        [System.IO.File]::WriteAllText($auditPath, $formatted + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
        Write-Output $auditPath
    } else {
        Write-Output $formatted
    }
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
