[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PsdPath,

    [Parameter(Mandatory = $true)]
    [int]$LayerId,

    [string]$OutJson
)

$ErrorActionPreference = 'Stop'

$resolvedPath = (Resolve-Path -LiteralPath $PsdPath).Path
if ([System.IO.Path]::GetExtension($resolvedPath).ToLowerInvariant() -ne '.psd') {
    throw "Only PSD files are supported: $resolvedPath"
}

$photoshopWasRunning = [bool](Get-Process -Name Photoshop -ErrorAction SilentlyContinue)
$app = $null

try {
    $app = New-Object -ComObject Photoshop.Application
    $pathLiteral = ConvertTo-Json -Compress $resolvedPath
    $jsx = @"
var previousDialogs = app.displayDialogs;
app.displayDialogs = DialogModes.NO;
var outputText = null;
var sourceDoc = null;
var smartDoc = null;
try {
    function quoteJson(value) {
        var source = String(value);
        var escaped = "";
        for (var qi = 0; qi < source.length; qi++) {
            var code = source.charCodeAt(qi);
            var ch = source.charAt(qi);
            if (ch === "\\") { escaped += "\\\\"; }
            else if (ch === '"') { escaped += '\\"'; }
            else if (ch === "\r") { escaped += "\\r"; }
            else if (ch === "\n") { escaped += "\\n"; }
            else if (ch === "\t") { escaped += "\\t"; }
            else if (code < 32 || code > 126) {
                var hex = code.toString(16);
                while (hex.length < 4) { hex = "0" + hex; }
                escaped += "\\u" + hex;
            } else { escaped += ch; }
        }
        return '"' + escaped + '"';
    }

    function toJson(value) {
        if (value === null || value === undefined) { return "null"; }
        var valueType = typeof value;
        if (valueType === "string") { return quoteJson(value); }
        if (valueType === "number") { return isFinite(value) ? String(value) : "null"; }
        if (valueType === "boolean") { return value ? "true" : "false"; }
        if (value instanceof Array) {
            var values = [];
            for (var ai = 0; ai < value.length; ai++) { values.push(toJson(value[ai])); }
            return "[" + values.join(",") + "]";
        }
        var pairs = [];
        for (var key in value) {
            if (value.hasOwnProperty(key)) { pairs.push(quoteJson(key) + ":" + toJson(value[key])); }
        }
        return "{" + pairs.join(",") + "}";
    }

    function findLayerById(container, id) {
        for (var i = 0; i < container.layers.length; i++) {
            var layer = container.layers[i];
            if (layer.id === id) { return layer; }
            if (layer.typename === "LayerSet") {
                var nested = findLayerById(layer, id);
                if (nested) { return nested; }
            }
        }
        return null;
    }

    function numberValue(value) {
        try { return Number(value.as("px")); }
        catch (error) { return null; }
    }

    function unitValue(value, unitName) {
        try { return Number(value.as(unitName)); }
        catch (error) { return null; }
    }

    function inspectLayers(container, prefix, output) {
        for (var i = 0; i < container.layers.length; i++) {
            var layer = container.layers[i];
            var layerPath = prefix ? prefix + "/" + layer.name : layer.name;
            var record = {
                path: layerPath,
                name: layer.name,
                id: layer.id,
                type: layer.typename,
                kind: null,
                visible: layer.visible,
                text: null,
                boundsPx: null,
                textJustification: null,
                textPositionPx: null,
                textStyle: null
            };
            try { record.kind = String(layer.kind); } catch (kindError) {}
            try {
                if (layer.typename === "ArtLayer" && layer.kind === LayerKind.TEXT) {
                    record.text = String(layer.textItem.contents);
                    try { record.textJustification = String(layer.textItem.justification); }
                    catch (justificationError) {}
                    try {
                        record.textPositionPx = {
                            x: numberValue(layer.textItem.position[0]),
                            y: numberValue(layer.textItem.position[1])
                        };
                    } catch (positionError) {}
                    record.textStyle = {};
                    try { record.textStyle.fontPostScriptName = String(layer.textItem.font); }
                    catch (fontError) {}
                    try { record.textStyle.sizePt = unitValue(layer.textItem.size, "pt"); }
                    catch (sizeError) {}
                    try { record.textStyle.leadingPt = unitValue(layer.textItem.leading, "pt"); }
                    catch (leadingError) {}
                    try { record.textStyle.tracking = Number(layer.textItem.tracking); }
                    catch (trackingError) {}
                    try { record.textStyle.horizontalScalePercent = Number(layer.textItem.horizontalScale); }
                    catch (horizontalScaleError) {}
                    try { record.textStyle.verticalScalePercent = Number(layer.textItem.verticalScale); }
                    catch (verticalScaleError) {}
                }
            } catch (textError) {}
            try {
                record.boundsPx = {
                    left: numberValue(layer.bounds[0]),
                    top: numberValue(layer.bounds[1]),
                    right: numberValue(layer.bounds[2]),
                    bottom: numberValue(layer.bounds[3])
                };
            } catch (boundsError) {}
            output.push(record);
            if (layer.typename === "LayerSet") { inspectLayers(layer, layerPath, output); }
        }
    }

    var sourceFile = new File($pathLiteral);
    sourceDoc = app.open(sourceFile);
    var smartLayer = findLayerById(sourceDoc, $LayerId);
    if (!smartLayer) { throw new Error("Layer ID not found: $LayerId"); }
    if (smartLayer.typename !== "ArtLayer" || smartLayer.kind !== LayerKind.SMARTOBJECT) {
        throw new Error("Layer ID is not a smart object: $LayerId");
    }
    app.activeDocument = sourceDoc;
    sourceDoc.activeLayer = smartLayer;
    executeAction(stringIDToTypeID("placedLayerEditContents"), undefined, DialogModes.NO);
    smartDoc = app.activeDocument;
    if (smartDoc === sourceDoc) { throw new Error("Smart object did not open for editing"); }

    var layers = [];
    inspectLayers(smartDoc, "", layers);
    outputText = toJson({
        schema_version: 1,
        source_psd: sourceFile.fsName,
        parent_layer_id: $LayerId,
        smart_document: {
            name: smartDoc.name,
            width_px: Number(smartDoc.width.as("px")),
            height_px: Number(smartDoc.height.as("px")),
            layer_count_recursive: layers.length
        },
        layers: layers
    });
} finally {
    if (smartDoc) { try { smartDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (smartCloseError) {} }
    if (sourceDoc) { try { sourceDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (sourceCloseError) {} }
    app.displayDialogs = previousDialogs;
}
outputText;
"@

    $jsonText = $app.DoJavaScript($jsx)
    $parsed = $jsonText | ConvertFrom-Json
    $parsed | Add-Member -NotePropertyName inspected_at_utc `
        -NotePropertyValue ([DateTime]::UtcNow.ToString('o'))
    $formatted = $parsed | ConvertTo-Json -Depth 12

    if ($OutJson) {
        $parent = Split-Path -Parent $OutJson
        if ($parent -and -not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Path $parent | Out-Null
        }
        [System.IO.File]::WriteAllText(
            [System.IO.Path]::GetFullPath($OutJson),
            $formatted + [Environment]::NewLine,
            [System.Text.UTF8Encoding]::new($false)
        )
        Write-Output ([System.IO.Path]::GetFullPath($OutJson))
    } else {
        Write-Output $formatted
    }
}
finally {
    if ($app -and -not $photoshopWasRunning) {
        try { $app.Quit() } catch {}
    }
    if ($app) {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
