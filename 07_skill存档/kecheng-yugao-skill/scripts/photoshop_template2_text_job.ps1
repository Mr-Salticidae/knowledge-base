[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$JobPath
)

$ErrorActionPreference = 'Stop'

function Resolve-JobFile([string]$baseDirectory, [string]$value) {
    if ([System.IO.Path]::IsPathRooted($value)) {
        return [System.IO.Path]::GetFullPath($value)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $baseDirectory $value))
}

function Require-JobValue($object, [string]$name) {
    $property = $object.PSObject.Properties[$name]
    if ($null -eq $property -or $null -eq $property.Value -or [string]::IsNullOrWhiteSpace([string]$property.Value)) {
        throw "Missing required job field: $name"
    }
    return $property.Value
}

$resolvedJob = (Resolve-Path -LiteralPath $JobPath).Path
$jobDirectory = Split-Path -Parent $resolvedJob
$job = Get-Content -LiteralPath $resolvedJob -Raw -Encoding UTF8 | ConvertFrom-Json

if ($job.schema_version -ne 1) {
    throw 'Template 2 text job schema_version must be 1.'
}
if ($null -eq $job.text_layers -or $job.text_layers.Count -eq 0) {
    throw 'Template 2 text job must contain text_layers.'
}

$sourcePsd = Resolve-JobFile $jobDirectory ([string](Require-JobValue $job 'source_psd'))
$outPsd = Resolve-JobFile $jobDirectory ([string](Require-JobValue $job 'out_psd'))
$outPng = Resolve-JobFile $jobDirectory ([string](Require-JobValue $job 'out_png'))
$outAudit = Resolve-JobFile $jobDirectory ([string](Require-JobValue $job 'out_audit'))

if ($job.PSObject.Properties['icon_replacements']) {
    foreach ($iconSpec in $job.icon_replacements) {
        $iconFile = Resolve-JobFile $jobDirectory ([string](Require-JobValue $iconSpec 'icon_file'))
        if (-not (Test-Path -LiteralPath $iconFile -PathType Leaf)) {
            throw "Icon file does not exist: $iconFile"
        }
        if ($iconSpec.PSObject.Properties['expected_sha256']) {
            $actualIconHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $iconFile).Hash.ToLowerInvariant()
            if ($actualIconHash -ne ([string]$iconSpec.expected_sha256).ToLowerInvariant()) {
                throw "Icon hash mismatch for role $($iconSpec.role): $iconFile"
            }
        }
        $iconSpec.icon_file = $iconFile
    }
}

if (-not (Test-Path -LiteralPath $sourcePsd -PathType Leaf)) {
    throw "Source PSD does not exist: $sourcePsd"
}
foreach ($outputPath in @($outPsd, $outPng, $outAudit)) {
    if (Test-Path -LiteralPath $outputPath) {
        throw "Refusing to overwrite existing output: $outputPath"
    }
    $parent = Split-Path -Parent $outputPath
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }
}

$sourceLiteral = ConvertTo-Json -Compress $sourcePsd
$outPsdLiteral = ConvertTo-Json -Compress $outPsd
$outPngLiteral = ConvertTo-Json -Compress $outPng
$jobLiteral = $job | ConvertTo-Json -Depth 20 -Compress

$photoshopWasRunning = [bool](Get-Process -Name Photoshop -ErrorAction SilentlyContinue)
$app = $null

try {
    $app = New-Object -ComObject Photoshop.Application
    $jsx = @"
var sourcePsd = new File($sourceLiteral);
var outputPsd = new File($outPsdLiteral);
var outputPng = new File($outPngLiteral);
var job = $jobLiteral;
var previousDialogs = app.displayDialogs;
app.displayDialogs = DialogModes.NO;

var missingFonts = [];
if (job.required_fonts) {
    var fontTestDocument = null;
    try {
        fontTestDocument = app.documents.add(UnitValue(32, "px"), UnitValue(32, "px"), 72,
            "template2-font-preflight", NewDocumentMode.RGB, DocumentFill.TRANSPARENT);
        for (var requiredFontIndex = 0; requiredFontIndex < job.required_fonts.length; requiredFontIndex++) {
            var requiredFont = String(job.required_fonts[requiredFontIndex]);
            var fontTestLayer = fontTestDocument.artLayers.add();
            fontTestLayer.kind = LayerKind.TEXT;
            fontTestLayer.textItem.contents = "A";
            try { fontTestLayer.textItem.font = requiredFont; } catch (fontSetError) {}
            if (String(fontTestLayer.textItem.font) !== requiredFont) { missingFonts.push(requiredFont); }
            fontTestLayer.remove();
        }
    } finally {
        if (fontTestDocument) { fontTestDocument.close(SaveOptions.DONOTSAVECHANGES); }
    }
}
if (missingFonts.length > 0) {
    throw new Error("Missing required Photoshop fonts: " + missingFonts.join(", ") +
        ". Activate/install them before editing; font substitution is forbidden.");
}

function px(value) {
    return Number(value.as("px"));
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
    if (valueType === "number") { return isFinite(value) ? String(value) : "null"; }
    if (valueType === "boolean") { return value ? "true" : "false"; }
    if (value instanceof Array) {
        var arrayValues = [];
        for (var ai = 0; ai < value.length; ai++) { arrayValues.push(toJson(value[ai])); }
        return "[" + arrayValues.join(",") + "]";
    }
    var objectValues = [];
    for (var key in value) {
        if (value.hasOwnProperty(key)) { objectValues.push(quoteJson(key) + ":" + toJson(value[key])); }
    }
    return "{" + objectValues.join(",") + "}";
}

function pt(value) {
    return Number(value.as("pt"));
}

function boundsOf(layer) {
    return {
        left: px(layer.bounds[0]),
        top: px(layer.bounds[1]),
        right: px(layer.bounds[2]),
        bottom: px(layer.bounds[3])
    };
}

function positionOf(textItem) {
    return {x: px(textItem.position[0]), y: px(textItem.position[1])};
}

function closeEnough(a, b, tolerance) {
    return Math.abs(Number(a) - Number(b)) <= tolerance;
}

function boundsCloseEnough(actual, expected, tolerance) {
    return closeEnough(actual.left, expected.left, tolerance) &&
        closeEnough(actual.top, expected.top, tolerance) &&
        closeEnough(actual.right, expected.right, tolerance) &&
        closeEnough(actual.bottom, expected.bottom, tolerance);
}

function findLayerById(container, layerId) {
    for (var i = 0; i < container.layers.length; i++) {
        var layer = container.layers[i];
        if (Number(layer.id) === Number(layerId)) {
            return layer;
        }
        if (layer.typename === "LayerSet") {
            var nested = findLayerById(layer, layerId);
            if (nested) {
                return nested;
            }
        }
    }
    return null;
}

function setTextPreservingRanges(layer, targetText) {
    var layerReference = new ActionReference();
    layerReference.putIdentifier(charIDToTypeID("Lyr "), layer.id);
    var layerDescriptor = executeActionGet(layerReference);
    var textDescriptor = layerDescriptor.getObjectValue(stringIDToTypeID("textKey"));
    var descriptorText = textDescriptor.getString(stringIDToTypeID("textKey"));
    var terminalReturn = descriptorText.length > 0 && descriptorText.charAt(descriptorText.length - 1) === "\r";
    var replacementText = String(targetText).replace(/\r\n/g, "\r").replace(/\n/g, "\r");
    if (terminalReturn && replacementText.charAt(replacementText.length - 1) !== "\r") {
        replacementText += "\r";
    }
    var newLength = replacementText.length;
    textDescriptor.putString(stringIDToTypeID("textKey"), replacementText);

    function resizeTerminalRanges(listKey, objectKey) {
        if (!textDescriptor.hasKey(stringIDToTypeID(listKey))) { return; }
        var oldList = textDescriptor.getList(stringIDToTypeID(listKey));
        var newList = new ActionList();
        var terminalEnd = 0;
        for (var terminalIndex = 0; terminalIndex < oldList.count; terminalIndex++) {
            var terminalDescriptor = oldList.getObjectValue(terminalIndex);
            var terminalTo = terminalDescriptor.getInteger(stringIDToTypeID("to"));
            if (terminalTo > terminalEnd) { terminalEnd = terminalTo; }
        }
        for (var rangeIndex = 0; rangeIndex < oldList.count; rangeIndex++) {
            var rangeDescriptor = oldList.getObjectValue(rangeIndex);
            var toKey = stringIDToTypeID("to");
            if (rangeDescriptor.getInteger(toKey) === terminalEnd) {
                rangeDescriptor.putInteger(toKey, newLength);
            }
            newList.putObject(stringIDToTypeID(objectKey), rangeDescriptor);
        }
        textDescriptor.putList(stringIDToTypeID(listKey), newList);
    }

    resizeTerminalRanges("textStyleRange", "textStyleRange");
    resizeTerminalRanges("paragraphStyleRange", "paragraphStyleRange");
    var setReference = new ActionReference();
    setReference.putIdentifier(charIDToTypeID("Lyr "), layer.id);
    var setDescriptor = new ActionDescriptor();
    setDescriptor.putReference(charIDToTypeID("null"), setReference);
    setDescriptor.putObject(charIDToTypeID("T   "), stringIDToTypeID("textLayer"), textDescriptor);
    executeAction(charIDToTypeID("setd"), setDescriptor, DialogModes.NO);
    return findLayerById(app.activeDocument, layer.id);
}

function textSizeMetrics(layer) {
    var layerReference = new ActionReference();
    layerReference.putIdentifier(charIDToTypeID("Lyr "), layer.id);
    var layerDescriptor = executeActionGet(layerReference);
    var textDescriptor = layerDescriptor.getObjectValue(stringIDToTypeID("textKey"));
    var ranges = textDescriptor.getList(stringIDToTypeID("textStyleRange"));
    var styleDescriptor = ranges.getObjectValue(0).getObjectValue(stringIDToTypeID("textStyle"));
    var sizePt = styleDescriptor.getUnitDoubleValue(stringIDToTypeID("size"));
    var impliedSizePt = styleDescriptor.hasKey(stringIDToTypeID("impliedFontSize")) ?
        styleDescriptor.getUnitDoubleValue(stringIDToTypeID("impliedFontSize")) : sizePt;
    return {
        sizePt: sizePt,
        impliedSizePt: impliedSizePt,
        impliedScale: sizePt === 0 ? 1 : impliedSizePt / sizePt
    };
}

function setUniformTextSize(layer, sizePt, impliedScale) {
    var layerId = layer.id;
    var layerReference = new ActionReference();
    layerReference.putIdentifier(charIDToTypeID("Lyr "), layerId);
    var layerDescriptor = executeActionGet(layerReference);
    var textDescriptor = layerDescriptor.getObjectValue(stringIDToTypeID("textKey"));
    var rangeKey = stringIDToTypeID("textStyleRange");
    var styleKey = stringIDToTypeID("textStyle");
    var oldList = textDescriptor.getList(rangeKey);
    var newList = new ActionList();
    for (var i = 0; i < oldList.count; i++) {
        var rangeDescriptor = oldList.getObjectValue(i);
        var styleDescriptor = rangeDescriptor.getObjectValue(styleKey);
        styleDescriptor.putUnitDouble(stringIDToTypeID("size"), charIDToTypeID("#Pnt"), Number(sizePt));
        if (styleDescriptor.hasKey(stringIDToTypeID("impliedFontSize"))) {
            styleDescriptor.putUnitDouble(stringIDToTypeID("impliedFontSize"),
                charIDToTypeID("#Pnt"), Number(sizePt) * Number(impliedScale));
        }
        rangeDescriptor.putObject(styleKey, styleKey, styleDescriptor);
        newList.putObject(rangeKey, rangeDescriptor);
    }
    textDescriptor.putList(rangeKey, newList);
    var setReference = new ActionReference();
    setReference.putIdentifier(charIDToTypeID("Lyr "), layerId);
    var setDescriptor = new ActionDescriptor();
    setDescriptor.putReference(charIDToTypeID("null"), setReference);
    setDescriptor.putObject(charIDToTypeID("T   "), stringIDToTypeID("textLayer"), textDescriptor);
    executeAction(charIDToTypeID("setd"), setDescriptor, DialogModes.NO);
    return findLayerById(app.activeDocument, layerId);
}

function fits(bounds, safe) {
    var tolerance = 0.75;
    return bounds.left >= Number(safe.left) - tolerance &&
        bounds.top >= Number(safe.top) - tolerance &&
        bounds.right <= Number(safe.right) + tolerance &&
        bounds.bottom <= Number(safe.bottom) + tolerance;
}

function maximizeTitleSize(layer, spec, lockedFont) {
    var low = Number(spec.minimum_font_size_pt);
    var high = Number(spec.maximum_font_size_pt);
    var sourceSizeMetrics = textSizeMetrics(layer);
    layer = setUniformTextSize(layer, low, sourceSizeMetrics.impliedScale);
    layer.textItem.font = lockedFont;
    var minimumBounds = boundsOf(layer);
    if (!fits(minimumBounds, spec.safe_bounds_px)) {
        throw new Error("Title does not fit at minimum size for role " + spec.role +
            "; minimum_size_pt=" + low +
            "; actual_bounds=" + toJson(minimumBounds) +
            "; safe_bounds=" + toJson(spec.safe_bounds_px));
    }
    var best = low;
    for (var i = 0; i < 18; i++) {
        var middle = (low + high) / 2;
        layer = setUniformTextSize(layer, middle, sourceSizeMetrics.impliedScale);
        layer.textItem.font = lockedFont;
        if (fits(boundsOf(layer), spec.safe_bounds_px)) {
            best = middle;
            low = middle;
        } else {
            high = middle;
        }
    }
    layer = setUniformTextSize(layer, best, sourceSizeMetrics.impliedScale);
    layer.textItem.font = lockedFont;
    var finalBounds = boundsOf(layer);
    var safeWidth = Number(spec.safe_bounds_px.right) - Number(spec.safe_bounds_px.left);
    var fillRatio = (finalBounds.right - finalBounds.left) / safeWidth;
    if (fillRatio + 0.0001 < Number(spec.minimum_fill_ratio)) {
        throw new Error("Title is not visually full enough for role " + spec.role +
            "; final_size_pt=" + best +
            "; fill_ratio=" + fillRatio +
            "; required_fill_ratio=" + spec.minimum_fill_ratio +
            "; final_bounds=" + toJson(finalBounds) +
            "; split the title differently instead of moving the layer.");
    }
    return {
        sizePt: best,
        fillRatio: fillRatio,
        boundsPx: finalBounds,
        sourceSizeMetrics: sourceSizeMetrics
    };
}

function styleSnapshot(layer) {
    var item = layer.textItem;
    var leading = null;
    var textBoxWidth = null;
    try { leading = pt(item.leading); } catch (errorLeading) {}
    try { textBoxWidth = px(item.width); } catch (errorWidth) {}
    return {
        font: String(item.font),
        sizePt: pt(item.size),
        leadingPt: leading,
        tracking: Number(item.tracking),
        justification: String(item.justification),
        positionPx: positionOf(item),
        textType: String(item.kind),
        textBoxWidthPx: textBoxWidth
    };
}

function centerLayerOn(layer, targetX, targetY) {
    var before = boundsOf(layer);
    var currentX = (before.left + before.right) / 2;
    var currentY = (before.top + before.bottom) / 2;
    var dx = targetX === null || targetX === undefined ? 0 : Number(targetX) - currentX;
    var dy = targetY === null || targetY === undefined ? 0 : Number(targetY) - currentY;
    layer.translate(UnitValue(dx, "px"), UnitValue(dy, "px"));
    return boundsOf(layer);
}

function transformLayerByContract(doc, spec) {
    var layer = findLayerById(doc, Number(spec.layer_id));
    if (!layer) {
        throw new Error("Missing contracted transform layer ID " + spec.layer_id + " for role " + spec.role);
    }
    var before = {
        id: Number(layer.id),
        name: String(layer.name),
        visible: Boolean(layer.visible),
        boundsPx: boundsOf(layer)
    };
    if (spec.expected_bounds_px && !boundsCloseEnough(before.boundsPx, spec.expected_bounds_px, 0.75)) {
        throw new Error("Source transform bounds mismatch for role " + spec.role);
    }
    var scaleX = spec.scale_x_percent === undefined ? 100 : Number(spec.scale_x_percent);
    var scaleY = spec.scale_y_percent === undefined ? 100 : Number(spec.scale_y_percent);
    if (!(scaleX > 0) || !(scaleY > 0)) {
        throw new Error("Invalid transform scale for role " + spec.role);
    }
    if (!closeEnough(scaleX, 100, 0.001) || !closeEnough(scaleY, 100, 0.001)) {
        layer.resize(scaleX, scaleY, AnchorPosition.MIDDLECENTER);
    }
    var resized = boundsOf(layer);
    var dx = spec.translate_x_px === undefined ? 0 : Number(spec.translate_x_px);
    var dy = spec.translate_y_px === undefined ? 0 : Number(spec.translate_y_px);
    if (dx !== 0 || dy !== 0) {
        layer.translate(UnitValue(dx, "px"), UnitValue(dy, "px"));
    }
    var after = {
        id: Number(layer.id),
        name: String(layer.name),
        visible: Boolean(layer.visible),
        boundsPx: boundsOf(layer)
    };
    if (spec.safe_bounds_px && !fits(after.boundsPx, spec.safe_bounds_px)) {
        throw new Error("Transformed layer exceeded safe bounds for role " + spec.role);
    }
    return {role: String(spec.role), before: before, resized_bounds_px: resized, after: after};
}

function setLayerVisibilityByContract(doc, spec) {
    var layer = findLayerById(doc, Number(spec.layer_id));
    if (!layer) {
        throw new Error("Missing contracted visibility layer ID " + spec.layer_id + " for role " + spec.role);
    }
    var before = {
        id: Number(layer.id),
        name: String(layer.name),
        visible: Boolean(layer.visible),
        boundsPx: boundsOf(layer)
    };
    if (spec.expected_visible !== undefined && before.visible !== Boolean(spec.expected_visible)) {
        throw new Error("Source visibility mismatch for role " + spec.role);
    }
    if (spec.expected_text !== undefined) {
        if (layer.typename !== "ArtLayer" || layer.kind !== LayerKind.TEXT) {
            throw new Error("Visibility contract expected editable text for role " + spec.role);
        }
        if (String(layer.textItem.contents) !== String(spec.expected_text)) {
            throw new Error("Source text mismatch in visibility contract for role " + spec.role);
        }
    }
    if (spec.expected_bounds_px && !boundsCloseEnough(before.boundsPx, spec.expected_bounds_px, 0.75)) {
        throw new Error("Source bounds mismatch in visibility contract for role " + spec.role);
    }
    layer.visible = Boolean(spec.visible);
    var after = {
        id: Number(layer.id),
        name: String(layer.name),
        visible: Boolean(layer.visible),
        boundsPx: boundsOf(layer)
    };
    if (!boundsCloseEnough(before.boundsPx, after.boundsPx, 0.1)) {
        throw new Error("Layer moved while changing visibility for role " + spec.role);
    }
    return {role: String(spec.role), before: before, after: after};
}

function copyMergedSlice(sourceDoc, targetDoc, rect, name) {
    app.activeDocument = sourceDoc;
    sourceDoc.selection.select([
        [Number(rect.left), Number(rect.top)],
        [Number(rect.right), Number(rect.top)],
        [Number(rect.right), Number(rect.bottom)],
        [Number(rect.left), Number(rect.bottom)]
    ]);
    sourceDoc.selection.copy(false);
    sourceDoc.selection.deselect();
    app.activeDocument = targetDoc;
    var pasted = targetDoc.paste();
    pasted.name = String(name);
    pasted.visible = true;
    return pasted;
}

function fitSliceToHorizontalRange(layer, left, right) {
    var before = boundsOf(layer);
    var width = before.right - before.left;
    var targetWidth = Number(right) - Number(left);
    if (!(width > 0) || !(targetWidth > 0)) {
        throw new Error("Invalid adaptive column slice width for " + layer.name);
    }
    layer.resize(targetWidth / width * 100, 100, AnchorPosition.MIDDLECENTER);
    var resized = boundsOf(layer);
    layer.translate(UnitValue(Number(left) - resized.left, "px"), UnitValue(0, "px"));
    return {before: before, after: boundsOf(layer)};
}

function fitSliceToRect(layer, rect) {
    var before = boundsOf(layer);
    var width = before.right - before.left;
    var height = before.bottom - before.top;
    var targetWidth = Number(rect.right) - Number(rect.left);
    var targetHeight = Number(rect.bottom) - Number(rect.top);
    if (!(width > 0) || !(height > 0) || !(targetWidth > 0) || !(targetHeight > 0)) {
        throw new Error("Invalid adaptive overlay rectangle for " + layer.name);
    }
    layer.resize(targetWidth / width * 100, targetHeight / height * 100, AnchorPosition.MIDDLECENTER);
    var resized = boundsOf(layer);
    layer.translate(UnitValue(Number(rect.left) - resized.left, "px"),
        UnitValue(Number(rect.top) - resized.top, "px"));
    return {before: before, after: boundsOf(layer)};
}

function adaptiveColumnsByContract(doc, spec) {
    var originalVisibility = [];
    var hiddenIds = spec.clean_copy_hidden_layer_ids || [];
    for (var hi = 0; hi < hiddenIds.length; hi++) {
        var hiddenLayer = findLayerById(doc, Number(hiddenIds[hi]));
        if (!hiddenLayer) throw new Error("Missing adaptive-column clean-copy layer ID " + hiddenIds[hi]);
        originalVisibility.push({layer: hiddenLayer, visible: Boolean(hiddenLayer.visible)});
        hiddenLayer.visible = false;
    }

    var slices = {};
    var cleanBaseDoc = null;
    try {
        cleanBaseDoc = doc.duplicate("AUTO_COLUMN_CLEAN_BASE", false);
        app.activeDocument = cleanBaseDoc;
        cleanBaseDoc.flatten();
        var sourceSlices = spec.source_slices;
        for (var key in sourceSlices) {
            if (!sourceSlices.hasOwnProperty(key)) continue;
            slices[key] = copyMergedSlice(cleanBaseDoc, doc, sourceSlices[key], "AUTO_COLUMN_BASE_" + key);
        }
    } finally {
        if (cleanBaseDoc) {
            try { cleanBaseDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (cleanBaseCloseError) {}
        }
        app.activeDocument = doc;
        for (var ri = 0; ri < originalVisibility.length; ri++) {
            originalVisibility[ri].layer.visible = originalVisibility[ri].visible;
        }
    }

    var softwareRight = Number(spec.software_right_px);
    var canvasRight = Number(spec.canvas_right_px || 1080);
    var softwareLeftCap = Number(spec.software_left_cap_width_px || 245);
    var softwareRightCap = Number(spec.software_right_cap_width_px || 140);
    var dateLeftCap = Number(spec.date_left_cap_width_px || 110);
    var dateRightCap = Number(spec.date_right_cap_width_px || 130);
    if (softwareRight < softwareLeftCap + softwareRightCap) {
        throw new Error("Adaptive software panel is too narrow for its preserved caps");
    }
    if (canvasRight - softwareRight <= dateLeftCap + dateRightCap) {
        throw new Error("Adaptive date panel is too narrow for its preserved caps");
    }

    var placement = {};
    placement.date_left = fitSliceToHorizontalRange(slices.date_left, softwareRight, softwareRight + dateLeftCap);
    placement.date_middle = fitSliceToHorizontalRange(
        slices.date_middle, softwareRight + dateLeftCap, canvasRight - dateRightCap);
    placement.date_right = fitSliceToHorizontalRange(slices.date_right, canvasRight - dateRightCap, canvasRight);
    placement.software_left = fitSliceToHorizontalRange(slices.software_left, 0, softwareLeftCap);
    placement.software_middle = fitSliceToHorizontalRange(
        slices.software_middle, softwareLeftCap, softwareRight - softwareRightCap);
    placement.software_right = fitSliceToHorizontalRange(
        slices.software_right, softwareRight - softwareRightCap, softwareRight);
    if (slices.zero_tool_gap_clean) {
        placement.zero_tool_gap_clean = fitSliceToRect(slices.zero_tool_gap_clean, {
            left: 225, top: 835, right: softwareRight, bottom: 872
        });
    }
    var order = ["date_right", "date_middle", "date_left", "software_right", "software_middle", "software_left", "zero_tool_gap_clean"];
    for (var oi = 0; oi < order.length; oi++) {
        if (slices[order[oi]]) slices[order[oi]].move(doc.layers[0], ElementPlacement.PLACEBEFORE);
    }

    var label = findLayerById(doc, Number(spec.delivery_label_layer_id));
    var labelBackground = findLayerById(doc, Number(spec.delivery_label_background_layer_id));
    var dateLayer = findLayerById(doc, Number(spec.date_layer_id));
    var weekdayLayer = findLayerById(doc, Number(spec.weekday_time_layer_id));
    if (!label || !labelBackground || !dateLayer || !weekdayLayer) {
        throw new Error("Adaptive-column date header/text layers are missing");
    }
    weekdayLayer = setTextPreservingRanges(weekdayLayer, String(spec.target_weekday));
    var timeLayer = weekdayLayer.duplicate();
    timeLayer.name = "AUTO_TIME_" + String(spec.target_time);
    timeLayer = setTextPreservingRanges(timeLayer, String(spec.target_time));

    var panelWidth = canvasRight - softwareRight;
    var panelCenter = (softwareRight + canvasRight) / 2;
    centerLayerOn(labelBackground, panelCenter, Number(spec.delivery_label_center_y_px || 822));
    centerLayerOn(label, panelCenter, Number(spec.delivery_label_center_y_px || 822));
    var dateBounds = boundsOf(dateLayer);
    var weekdayBounds = boundsOf(weekdayLayer);
    var timeBounds = boundsOf(timeLayer);
    var dateWidth = dateBounds.right - dateBounds.left;
    var weekdayWidth = weekdayBounds.right - weekdayBounds.left;
    var timeWidth = timeBounds.right - timeBounds.left;
    var totalTextWidth = dateWidth + weekdayWidth + timeWidth;
    var gap = (panelWidth - totalTextWidth) / 4;
    var dateTextLayout = "single_row";
    if (gap >= Number(spec.minimum_date_text_gap_px || 6)) {
        var cursor = softwareRight + gap;
        var rowY = Number(spec.date_row_center_y_px || 930);
        centerLayerOn(dateLayer, cursor + dateWidth / 2, rowY);
        cursor += dateWidth + gap;
        centerLayerOn(weekdayLayer, cursor + weekdayWidth / 2, rowY);
        cursor += weekdayWidth + gap;
        centerLayerOn(timeLayer, cursor + timeWidth / 2, rowY);
    } else {
        dateTextLayout = "compact_two_rows";
        centerLayerOn(dateLayer, panelCenter, Number(spec.date_compact_center_y_px || 900));
        var bottomGap = (panelWidth - weekdayWidth - timeWidth) / 3;
        if (bottomGap < Number(spec.minimum_date_text_gap_px || 6)) {
            throw new Error("Adaptive compact weekday/time row does not fit without overlap");
        }
        var bottomY = Number(spec.weekday_time_compact_center_y_px || 978);
        centerLayerOn(weekdayLayer, softwareRight + bottomGap + weekdayWidth / 2, bottomY);
        centerLayerOn(timeLayer, canvasRight - bottomGap - timeWidth / 2, bottomY);
    }

    // The reconstructed bases must cover the old merged artwork, while every
    // editable label remains above them. Keep the content editable and do not
    // flatten the result.
    var foregroundIds = spec.foreground_layer_ids || [];
    for (var fi = foregroundIds.length - 1; fi >= 0; fi--) {
        var foreground = findLayerById(doc, Number(foregroundIds[fi]));
        if (foreground) foreground.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
    }
    // Reassert label z-order after moving all foreground layers: paper first,
    // then its editable text. This prevents the header artwork from covering
    // the white label text.
    var softwareLabelBackground = findLayerById(doc, Number(spec.software_label_background_layer_id));
    var softwareLabel = findLayerById(doc, Number(spec.software_label_layer_id));
    if (softwareLabelBackground) softwareLabelBackground.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
    if (softwareLabel) softwareLabel.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
    labelBackground.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
    label.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
    timeLayer.move(doc.layers[0], ElementPlacement.PLACEBEFORE);

    return {
        tool_count: Number(spec.tool_count),
        software_right_px: softwareRight,
        date_panel_width_px: panelWidth,
        preserved_software_right_sticker: true,
        editable_base_layer_names: [
            slices.software_left.name, slices.software_middle.name, slices.software_right.name,
            slices.date_left.name, slices.date_middle.name, slices.date_right.name
        ],
        slice_placements: placement,
        text_layout: {
            delivery_label: boundsOf(label),
            date: boundsOf(dateLayer),
            weekday: boundsOf(weekdayLayer),
            time: boundsOf(timeLayer),
            weekday_text: String(weekdayLayer.textItem.contents),
            time_text: String(timeLayer.textItem.contents),
            layout_mode: dateTextLayout
        }
    };
}

function replaceIconInsideContractedSlot(doc, spec) {
    var originalLayer = findLayerById(doc, Number(spec.layer_id));
    if (!originalLayer) {
        throw new Error("Missing contracted icon layer ID " + spec.layer_id + " for role " + spec.role);
    }
    if (originalLayer.typename !== "ArtLayer" || originalLayer.kind === LayerKind.TEXT) {
        throw new Error("Contracted icon layer is not a raster art layer for role " + spec.role);
    }
    if (!spec.target_bounds_px) {
        throw new Error("Missing target_bounds_px for icon role " + spec.role);
    }
    var originalBefore = {
        id: Number(originalLayer.id),
        name: String(originalLayer.name),
        visible: Boolean(originalLayer.visible),
        boundsPx: boundsOf(originalLayer)
    };
    if (spec.expected_bounds_px &&
            !boundsCloseEnough(originalBefore.boundsPx, spec.expected_bounds_px, 0.75)) {
        throw new Error("Source icon bounds mismatch for role " + spec.role);
    }

    var iconFile = new File(String(spec.icon_file));
    if (!iconFile.exists) {
        throw new Error("Resolved icon file is missing for role " + spec.role + ": " + iconFile.fsName);
    }
    var iconDocument = null;
    var pastedLayer = null;
    try {
        iconDocument = app.open(iconFile);
        app.activeDocument = iconDocument;
        iconDocument.selection.selectAll();
        iconDocument.selection.copy(true);
        app.activeDocument = doc;
        originalLayer.visible = false;
        pastedLayer = doc.paste();
        pastedLayer.name = "AUTO_ICON_" + String(spec.role) + "_" + String(spec.tool_name);
        pastedLayer.move(originalLayer, ElementPlacement.PLACEBEFORE);
        pastedLayer.move(doc.layers[0], ElementPlacement.PLACEBEFORE);

        var initialBounds = boundsOf(pastedLayer);
        var initialWidth = initialBounds.right - initialBounds.left;
        var initialHeight = initialBounds.bottom - initialBounds.top;
        if (initialWidth <= 0 || initialHeight <= 0) {
            throw new Error("Replacement icon has empty visible bounds for role " + spec.role);
        }
        var target = spec.target_bounds_px;
        var targetWidth = Number(target.right) - Number(target.left);
        var targetHeight = Number(target.bottom) - Number(target.top);
        var fitScale = Math.min(targetWidth / initialWidth, targetHeight / initialHeight);
        if (!(fitScale > 0)) {
            throw new Error("Invalid contracted icon slot for role " + spec.role);
        }
        pastedLayer.resize(fitScale * 100, fitScale * 100, AnchorPosition.MIDDLECENTER);
        var resizedBounds = boundsOf(pastedLayer);
        var targetCenterX = (Number(target.left) + Number(target.right)) / 2;
        var targetCenterY = (Number(target.top) + Number(target.bottom)) / 2;
        var actualCenterX = (resizedBounds.left + resizedBounds.right) / 2;
        var actualCenterY = (resizedBounds.top + resizedBounds.bottom) / 2;
        pastedLayer.translate(UnitValue(targetCenterX - actualCenterX, "px"),
            UnitValue(targetCenterY - actualCenterY, "px"));

        var replacementBounds = boundsOf(pastedLayer);
        if (!fits(replacementBounds, target)) {
            throw new Error("Replacement icon exceeded its contracted slot for role " + spec.role);
        }
        var originalAfter = {
            id: Number(originalLayer.id),
            name: String(originalLayer.name),
            visible: Boolean(originalLayer.visible),
            boundsPx: boundsOf(originalLayer)
        };
        if (!boundsCloseEnough(originalBefore.boundsPx, originalAfter.boundsPx, 0.1)) {
            throw new Error("Existing icon layer moved for role " + spec.role);
        }
        return {
            role: String(spec.role),
            tool_name: String(spec.tool_name),
            icon_file: iconFile.fsName,
            original_layer_before: originalBefore,
            original_layer_after: originalAfter,
            replacement_layer: {
                id: Number(pastedLayer.id),
                name: String(pastedLayer.name),
                boundsPx: replacementBounds
            },
            target_bounds_px: target
        };
    } finally {
        if (iconDocument) {
            try { iconDocument.close(SaveOptions.DONOTSAVECHANGES); } catch (iconCloseError) {}
            app.activeDocument = doc;
        }
    }
}

var doc = null;
var audit = {schema_version: 1, source_psd: sourcePsd.fsName, outputs: {}, text_layers: [], layer_visibility: [], layer_transforms: [], icon_replacements: [], adaptive_columns: null};
try {
    doc = app.open(sourcePsd);
    for (var li = 0; li < job.text_layers.length; li++) {
        var spec = job.text_layers[li];
        var layer = findLayerById(doc, Number(spec.layer_id));
        if (!layer) {
            throw new Error("Missing contracted text layer ID " + spec.layer_id + " for role " + spec.role);
        }
        if (layer.typename !== "ArtLayer" || layer.kind !== LayerKind.TEXT) {
            throw new Error("Contracted layer is not editable text for role " + spec.role);
        }
        if (String(layer.textItem.contents) !== String(spec.expected_text)) {
            throw new Error("Source text mismatch for role " + spec.role);
        }

        var before = {text: String(layer.textItem.contents), boundsPx: boundsOf(layer), style: styleSnapshot(layer)};
        if (String(layer.textItem.contents) !== String(spec.target_text)) {
            layer = setTextPreservingRanges(layer, spec.target_text);
        }
        layer.textItem.font = before.style.font;
        if (spec.expand_paragraph_text_width_px !== undefined) {
            if (String(layer.textItem.kind) !== String(TextType.PARAGRAPHTEXT)) {
                throw new Error("Text-box width expansion is allowed only for paragraph text; role " + spec.role);
            }
            var requestedTextBoxWidth = Number(spec.expand_paragraph_text_width_px);
            if (!(requestedTextBoxWidth > 0)) {
                throw new Error("Invalid paragraph text-box width for role " + spec.role);
            }
            layer.textItem.width = UnitValue(requestedTextBoxWidth, "px");
        }
        var titleFit = null;
        if (spec.allow_font_size_adjustment === true) {
            if (!spec.safe_bounds_px || spec.minimum_font_size_pt === undefined ||
                    spec.maximum_font_size_pt === undefined || spec.minimum_fill_ratio === undefined) {
                throw new Error("Title fitting contract is incomplete for role " + spec.role);
            }
            titleFit = maximizeTitleSize(layer, spec, before.style.font);
            layer = findLayerById(doc, Number(spec.layer_id));
        }

        if (spec.justification_center === true) {
            layer.textItem.justification = Justification.CENTER;
        }
        if (spec.center_x_px !== undefined || spec.center_y_px !== undefined) {
            centerLayerOn(
                layer,
                spec.center_x_px === undefined ? null : Number(spec.center_x_px),
                spec.center_y_px === undefined ? null : Number(spec.center_y_px)
            );
        }

        var afterStyle = styleSnapshot(layer);
        var afterBounds = boundsOf(layer);
        if (spec.allow_position_adjustment !== true &&
                (!closeEnough(before.style.positionPx.x, afterStyle.positionPx.x, 0.1) ||
                !closeEnough(before.style.positionPx.y, afterStyle.positionPx.y, 0.1))) {
            throw new Error("Layer position moved for role " + spec.role);
        }
        var leadingChanged = false;
        if (before.style.leadingPt === null || afterStyle.leadingPt === null) {
            leadingChanged = before.style.leadingPt !== afterStyle.leadingPt;
        } else {
            leadingChanged = !closeEnough(before.style.leadingPt, afterStyle.leadingPt, 0.01);
        }
        if (before.style.font !== afterStyle.font ||
                (spec.justification_center !== true && before.style.justification !== afterStyle.justification) ||
                !closeEnough(before.style.tracking, afterStyle.tracking, 0.01) ||
                (spec.allow_font_size_adjustment !== true && leadingChanged)) {
            throw new Error("Locked text style changed for role " + spec.role +
                "; before=" + toJson(before.style) +
                "; after=" + toJson(afterStyle));
        }
        if (spec.allow_font_size_adjustment !== true &&
                !closeEnough(before.style.sizePt, afterStyle.sizePt, 0.01)) {
            throw new Error("Non-title font size changed for role " + spec.role);
        }
        if (spec.safe_bounds_px && !fits(afterBounds, spec.safe_bounds_px)) {
            throw new Error("Text exceeded its fixed slot for role " + spec.role +
                "; do not move or shrink the layer.");
        }

        audit.text_layers.push({
            role: String(spec.role),
            layer_id: Number(spec.layer_id),
            before: before,
            after: {text: String(layer.textItem.contents), boundsPx: afterBounds, style: afterStyle},
            title_fit: titleFit
        });
    }

    if (job.layer_visibility) {
        for (var visibilityIndex = 0; visibilityIndex < job.layer_visibility.length; visibilityIndex++) {
            audit.layer_visibility.push(
                setLayerVisibilityByContract(doc, job.layer_visibility[visibilityIndex]));
        }
    }


    if (job.layer_transforms) {
        for (var transformIndex = 0; transformIndex < job.layer_transforms.length; transformIndex++) {
            audit.layer_transforms.push(
                transformLayerByContract(doc, job.layer_transforms[transformIndex]));
        }
    }

    if (job.adaptive_columns) {
        audit.adaptive_columns = adaptiveColumnsByContract(doc, job.adaptive_columns);
    }

    if (job.icon_replacements) {
        for (var iconIndex = 0; iconIndex < job.icon_replacements.length; iconIndex++) {
            audit.icon_replacements.push(
                replaceIconInsideContractedSlot(doc, job.icon_replacements[iconIndex]));
        }
    }

    var psdOptions = new PhotoshopSaveOptions();
    psdOptions.layers = true;
    doc.saveAs(outputPsd, psdOptions, true, Extension.LOWERCASE);
    var pngOptions = new PNGSaveOptions();
    doc.saveAs(outputPng, pngOptions, true, Extension.LOWERCASE);
    audit.outputs.psd = outputPsd.fsName;
    audit.outputs.png = outputPng.fsName;
} finally {
    if (doc) {
        try { doc.close(SaveOptions.DONOTSAVECHANGES); } catch (errorClose) {}
    }
    app.displayDialogs = previousDialogs;
}
toJson(audit);
"@

    $auditText = $app.DoJavaScript($jsx)
    $audit = $auditText | ConvertFrom-Json
    $audit | Add-Member -NotePropertyName source_sha256 -NotePropertyValue ((Get-FileHash -Algorithm SHA256 -LiteralPath $sourcePsd).Hash.ToLowerInvariant())
    $audit.outputs | Add-Member -NotePropertyName psd_sha256 -NotePropertyValue ((Get-FileHash -Algorithm SHA256 -LiteralPath $outPsd).Hash.ToLowerInvariant())
    $audit.outputs | Add-Member -NotePropertyName png_sha256 -NotePropertyValue ((Get-FileHash -Algorithm SHA256 -LiteralPath $outPng).Hash.ToLowerInvariant())
    $audit | Add-Member -NotePropertyName completed_at_utc -NotePropertyValue ([DateTime]::UtcNow.ToString('o'))
    $formatted = $audit | ConvertTo-Json -Depth 20
    [System.IO.File]::WriteAllText($outAudit, $formatted + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
    Write-Output $outAudit
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
