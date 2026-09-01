[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$PsdPath,

    [string]$OutJson
)

$ErrorActionPreference = 'Stop'

$resolvedPath = (Resolve-Path -LiteralPath $PsdPath).Path
if ([System.IO.Path]::GetExtension($resolvedPath).ToLowerInvariant() -ne '.psd') {
    throw "Only PSD files are supported: $resolvedPath"
}

$photoshopWasRunning = [bool](Get-Process -Name Photoshop -ErrorAction SilentlyContinue)
$app = $null
$openedDocument = $false

try {
    $app = New-Object -ComObject Photoshop.Application
    $pathLiteral = ConvertTo-Json -Compress $resolvedPath
    $jsx = @"
var previousDialogs = app.displayDialogs;
app.displayDialogs = DialogModes.NO;
var result = null;
var outputText = null;
try {
    var sourceFile = new File($pathLiteral);
    if (!sourceFile.exists) {
        throw new Error("PSD does not exist: " + sourceFile.fsName);
    }
    var doc = app.open(sourceFile);

    function numberValue(value) {
        try { return Number(value.as("px")); }
        catch (error) { return null; }
    }

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
        if (valueType === "number") {
            return isFinite(value) ? String(value) : "null";
        }
        if (valueType === "boolean") { return value ? "true" : "false"; }
        if (value instanceof Array) {
            var arrayValues = [];
            for (var ai = 0; ai < value.length; ai++) {
                arrayValues.push(toJson(value[ai]));
            }
            return "[" + arrayValues.join(",") + "]";
        }
        var objectValues = [];
        for (var key in value) {
            if (value.hasOwnProperty(key)) {
                objectValues.push(quoteJson(key) + ":" + toJson(value[key]));
            }
        }
        return "{" + objectValues.join(",") + "}";
    }

    function inspectTextRanges(layerId, listKey) {
        var ranges = [];
        try {
            var layerReference = new ActionReference();
            layerReference.putIdentifier(charIDToTypeID("Lyr "), layerId);
            var layerDescriptor = executeActionGet(layerReference);
            var textDescriptor = layerDescriptor.getObjectValue(stringIDToTypeID("textKey"));
            var rangeList = textDescriptor.getList(stringIDToTypeID(listKey));
            for (var ri = 0; ri < rangeList.count; ri++) {
                var rangeDescriptor = rangeList.getObjectValue(ri);
                ranges.push({
                    from: rangeDescriptor.getInteger(stringIDToTypeID("from")),
                    to: rangeDescriptor.getInteger(stringIDToTypeID("to"))
                });
            }
        } catch (rangeError) {}
        return ranges;
    }

    function inspectTextItem(textItem) {
        var style = {
            fontPostScriptName: null,
            sizePt: null,
            leadingPt: null,
            tracking: null,
            horizontalScalePercent: null,
            verticalScalePercent: null,
            justification: null,
            colorRgb: null
        };
        try { style.fontPostScriptName = String(textItem.font); } catch (errorFont) {}
        try { style.sizePt = Number(textItem.size.as("pt")); } catch (errorSize) {}
        try { style.leadingPt = Number(textItem.leading.as("pt")); } catch (errorLeading) {}
        try { style.tracking = Number(textItem.tracking); } catch (errorTracking) {}
        try { style.horizontalScalePercent = Number(textItem.horizontalScale); } catch (errorHorizontalScale) {}
        try { style.verticalScalePercent = Number(textItem.verticalScale); } catch (errorVerticalScale) {}
        try { style.justification = String(textItem.justification); } catch (errorJustification) {}
        try {
            style.colorRgb = {
                red: Number(textItem.color.rgb.red),
                green: Number(textItem.color.rgb.green),
                blue: Number(textItem.color.rgb.blue)
            };
        } catch (errorColor) {}
        return style;
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
                visible: layer.visible,
                opacity: layer.opacity,
                blendMode: String(layer.blendMode),
                kind: null,
                text: null,
                textStyle: null,
                textStyleRanges: null,
                paragraphStyleRanges: null,
                boundsPx: null
            };
            try { record.kind = String(layer.kind); } catch (error1) {}
            try {
                if (layer.typename === "ArtLayer" && layer.kind === LayerKind.TEXT) {
                    record.text = String(layer.textItem.contents);
                    record.textStyle = inspectTextItem(layer.textItem);
                    record.textStyleRanges = inspectTextRanges(layer.id, "textStyleRange");
                    record.paragraphStyleRanges = inspectTextRanges(layer.id, "paragraphStyleRange");
                }
            } catch (errorText) {}
            try {
                record.boundsPx = {
                    left: numberValue(layer.bounds[0]),
                    top: numberValue(layer.bounds[1]),
                    right: numberValue(layer.bounds[2]),
                    bottom: numberValue(layer.bounds[3])
                };
            } catch (error2) {}
            output.push(record);
            if (layer.typename === "LayerSet") {
                inspectLayers(layer, layerPath, output);
            }
        }
    }

    var layers = [];
    inspectLayers(doc, "", layers);
    result = {
        schema_version: 1,
        source_psd: sourceFile.fsName,
        document: {
            name: doc.name,
            width_px: Number(doc.width.as("px")),
            height_px: Number(doc.height.as("px")),
            resolution_ppi: Number(doc.resolution),
            color_mode: String(doc.mode),
            layer_count_recursive: layers.length
        },
        layers: layers,
        warnings: [
            "This inspection is read-only and does not prove that a smart object is embedded rather than linked.",
            "Create or verify a template layer contract before editing."
        ]
    };
    doc.close(SaveOptions.DONOTSAVECHANGES);
    outputText = toJson(result);
} finally {
    app.displayDialogs = previousDialogs;
}
outputText;
"@

    $jsonText = $app.DoJavaScript($jsx)
    $openedDocument = $true
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
