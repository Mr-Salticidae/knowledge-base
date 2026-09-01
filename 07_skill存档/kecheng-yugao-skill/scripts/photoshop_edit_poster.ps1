[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourcePsd,

    [Parameter(Mandatory = $true)]
    [string]$OutPsd,

    [Parameter(Mandatory = $true)]
    [string]$OutPng,

    [Parameter(Mandatory = $true)]
    [string]$TitleText,

    [Parameter(Mandatory = $true)]
    [string]$ExpectedTitle,

    [Parameter(Mandatory = $true)]
    [string]$DateText,

    [Parameter(Mandatory = $true)]
    [string]$ExpectedDate,

    [Parameter(Mandatory = $true)]
    [string]$TimeText,

    [string]$ExpectedTime,

    [Parameter(Mandatory = $true)]
    [string]$StatusText,

    [string]$ExpectedStatus,

    [Parameter(Mandatory = $true)]
    [string]$ObjectiveText,

    [string]$ExpectedObjective,

    [int]$TitleSmartLayerId = 32,
    [int]$TitleTextLayerId = 34,
    [int]$DateLayerId = 35,
    [int]$TimeLayerId = 38,
    [int]$StatusLayerId = 42,
    [int]$ObjectiveLayerId = 5,

    [double]$TitleTranslateX = 0,
    [double]$TitleTranslateY = 0,

    [double]$TitleTextTranslateY = 0,

    [double]$ObjectiveTranslateX = 0,
    [double]$ObjectiveTranslateY = 0,

    [ValidateSet('preserve', 'center', 'left', 'right')]
    [string]$TitleJustification = 'preserve',

    [switch]$CenterTitleHorizontally,

    [double]$TitleCenterTargetX = -1,

    [double]$MaxTitleCenterDeltaPx = 12,

    [switch]$FitTitleToSafeBounds,

    [double]$MinTitleFontSizePt = -1,

    [string]$MinTitleFontSizeByLineCountJson = '',

    [double]$MaxTitleFontSizePt = -1,

    [double]$TitleSafeLeftPx = -1,

    [double]$TitleSafeTopPx = -1,

    [double]$TitleSafeRightPx = -1,

    [double]$TitleSafeBottomPx = -1,

    [double]$TitleLeadingRatio = 1,

    [double]$MinTitleFillRatio = 0,

    [double]$MinTitleLineGlyphHeightPx = 0,

    [double]$TitleDecorationTopPx = -1,

    [double]$MinTitleDecorationGapPx = 0,

    [switch]$NormalizeTitleCharacterColor,

    [switch]$HideTitleAccentOverlay,

    [int]$TitleAccentOverlayLayerId = 42,

    [double]$MinTitleGapPx = 20,

    [double]$MinObjectiveTimeGapPx = 20,

    [double]$ObjectiveBottomLimitPx = -1,

    [switch]$SkipTitleCanvasGuard,

    [switch]$SkipObjectiveSafeAreaGuard,

    [string]$OutAudit
)

$ErrorActionPreference = 'Stop'

if (-not $PSBoundParameters.ContainsKey('ExpectedTime')) {
    $ExpectedTime = $TimeText
}
if (-not $PSBoundParameters.ContainsKey('ExpectedStatus')) {
    $ExpectedStatus = $StatusText
}
if (-not $PSBoundParameters.ContainsKey('ExpectedObjective')) {
    $ExpectedObjective = $ObjectiveText
}

$resolvedSource = (Resolve-Path -LiteralPath $SourcePsd).Path
if ([System.IO.Path]::GetExtension($resolvedSource).ToLowerInvariant() -ne '.psd') {
    throw "Only PSD source files are supported: $resolvedSource"
}

$resolvedOutPsd = [System.IO.Path]::GetFullPath($OutPsd)
$resolvedOutPng = [System.IO.Path]::GetFullPath($OutPng)
if ([System.IO.Path]::GetExtension($resolvedOutPsd).ToLowerInvariant() -ne '.psd') {
    throw "OutPsd must end in .psd: $resolvedOutPsd"
}
if ([System.IO.Path]::GetExtension($resolvedOutPng).ToLowerInvariant() -ne '.png') {
    throw "OutPng must end in .png: $resolvedOutPng"
}
if ($resolvedSource -eq $resolvedOutPsd) {
    throw 'Refusing to overwrite the source PSD.'
}
if (Test-Path -LiteralPath $resolvedOutPsd) {
    throw "Output PSD already exists: $resolvedOutPsd"
}
if (Test-Path -LiteralPath $resolvedOutPng) {
    throw "Output PNG already exists: $resolvedOutPng"
}

foreach ($path in @($resolvedOutPsd, $resolvedOutPng)) {
    $parent = Split-Path -Parent $path
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }
}
[System.IO.File]::Copy($resolvedSource, $resolvedOutPsd, $false)

$photoshopWasRunning = [bool](Get-Process -Name Photoshop -ErrorAction SilentlyContinue)
$app = $null
$completed = $false

try {
    $app = New-Object -ComObject Photoshop.Application
    $sourceLiteral = ConvertTo-Json -Compress $resolvedSource
    $psdLiteral = ConvertTo-Json -Compress $resolvedOutPsd
    $pngLiteral = ConvertTo-Json -Compress $resolvedOutPng
    $titleLiteral = ConvertTo-Json -Compress $TitleText
    $expectedTitleLiteral = ConvertTo-Json -Compress $ExpectedTitle
    $dateLiteral = ConvertTo-Json -Compress $DateText
    $expectedDateLiteral = ConvertTo-Json -Compress $ExpectedDate
    $timeLiteral = ConvertTo-Json -Compress $TimeText
    $expectedTimeLiteral = ConvertTo-Json -Compress $ExpectedTime
    $statusLiteral = ConvertTo-Json -Compress $StatusText
    $expectedStatusLiteral = ConvertTo-Json -Compress $ExpectedStatus
    $objectiveLiteral = ConvertTo-Json -Compress $ObjectiveText
    $expectedObjectiveLiteral = ConvertTo-Json -Compress $ExpectedObjective
    $titleTranslateXLiteral = $TitleTranslateX.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleTranslateYLiteral = $TitleTranslateY.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleTextTranslateYLiteral = $TitleTextTranslateY.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $objectiveTranslateXLiteral = $ObjectiveTranslateX.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $objectiveTranslateYLiteral = $ObjectiveTranslateY.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleJustificationLiteral = ConvertTo-Json -Compress $TitleJustification
    $centerTitleHorizontallyLiteral = if ($CenterTitleHorizontally) { 'true' } else { 'false' }
    $titleCenterTargetXLiteral = $TitleCenterTargetX.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $maxTitleCenterDeltaLiteral = $MaxTitleCenterDeltaPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $fitTitleLiteral = if ($FitTitleToSafeBounds) { 'true' } else { 'false' }
    $normalizeTitleCharacterColorLiteral = if ($NormalizeTitleCharacterColor) { 'true' } else { 'false' }
    $hideTitleAccentOverlayLiteral = if ($HideTitleAccentOverlay) { 'true' } else { 'false' }
    $minTitleFontSizeLiteral = $MinTitleFontSizePt.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $minTitleFontSizeByLineCountLiteral = if ([string]::IsNullOrWhiteSpace($MinTitleFontSizeByLineCountJson)) {
        '{}'
    } else {
        $MinTitleFontSizeByLineCountJson
    }
    $maxTitleFontSizeLiteral = $MaxTitleFontSizePt.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleSafeLeftLiteral = $TitleSafeLeftPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleSafeTopLiteral = $TitleSafeTopPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleSafeRightLiteral = $TitleSafeRightPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleSafeBottomLiteral = $TitleSafeBottomPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleLeadingRatioLiteral = $TitleLeadingRatio.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $minTitleFillRatioLiteral = $MinTitleFillRatio.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $minTitleLineGlyphHeightLiteral = $MinTitleLineGlyphHeightPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $titleDecorationTopLiteral = $TitleDecorationTopPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $minTitleDecorationGapLiteral = $MinTitleDecorationGapPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $minTitleGapLiteral = $MinTitleGapPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $minObjectiveTimeGapLiteral = $MinObjectiveTimeGapPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $objectiveBottomLimitLiteral = $ObjectiveBottomLimitPx.ToString(
        [System.Globalization.CultureInfo]::InvariantCulture
    )
    $skipTitleCanvasGuardLiteral = if ($SkipTitleCanvasGuard) { 'true' } else { 'false' }
    $skipObjectiveSafeAreaGuardLiteral = if ($SkipObjectiveSafeAreaGuard) { 'true' } else { 'false' }

    $jsx = @"
var previousDialogs = app.displayDialogs;
app.displayDialogs = DialogModes.NO;
var outputText = null;
var doc = null;
var smartDoc = null;
var currentStage = "initialize";
try {
    function quoteJson(value) {
        return '"' + String(value)
            .replace(/\\/g, "\\\\")
            .replace(/"/g, '\\"')
            .replace(/\r/g, "\\r")
            .replace(/\n/g, "\\n")
            .replace(/\t/g, "\\t") + '"';
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

    function normalizeText(value) {
        return String(value).replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/\s+/g, "").toLowerCase();
    }

    function layerBoundsPx(layer) {
        return {
            left: Number(layer.bounds[0].as("px")),
            top: Number(layer.bounds[1].as("px")),
            right: Number(layer.bounds[2].as("px")),
            bottom: Number(layer.bounds[3].as("px"))
        };
    }

    function textStyleSummary(layer) {
        var fontName = null;
        var sizePt = null;
        var leadingPt = null;
        var tracking = null;
        var horizontalScale = null;
        var verticalScale = null;
        try { fontName = String(layer.textItem.font); } catch (fontError) {}
        try { sizePt = Number(layer.textItem.size.as("pt")); } catch (sizeError) {}
        try { leadingPt = Number(layer.textItem.leading.as("pt")); } catch (leadingError) {}
        try { tracking = Number(layer.textItem.tracking); } catch (trackingError) {}
        try { horizontalScale = Number(layer.textItem.horizontalScale); } catch (horizontalScaleError) {}
        try { verticalScale = Number(layer.textItem.verticalScale); } catch (verticalScaleError) {}
        return {
            font_postscript_name: fontName,
            size_pt: sizePt,
            leading_pt: leadingPt,
            tracking: tracking,
            horizontal_scale_percent: horizontalScale,
            vertical_scale_percent: verticalScale
        };
    }

    function countTitleLines(value) {
        return String(value).replace(/\r\n/g, "\r").replace(/\n/g, "\r").split("\r").length;
    }

    function setTitleSize(layer, sizePt, leadingRatio, lineCount) {
        layer.textItem.size = UnitValue(sizePt, "pt");
        if (lineCount > 1) {
            layer.textItem.leading = UnitValue(sizePt * leadingRatio, "pt");
        }
    }

    function alignTitleInsideSafeBounds(layer, safeBounds, centerX) {
        var before = layerBoundsPx(layer);
        var currentCenterX = (before.left + before.right) / 2;
        var targetBottom = safeBounds.bottom;
        layer.translate(
            UnitValue(centerX - currentCenterX, "px"),
            UnitValue(targetBottom - before.bottom, "px")
        );
        return layerBoundsPx(layer);
    }

    function titleFitsSafeBounds(bounds, safeBounds) {
        var epsilon = 0.75;
        return bounds.left >= safeBounds.left - epsilon &&
            bounds.top >= safeBounds.top - epsilon &&
            bounds.right <= safeBounds.right + epsilon &&
            bounds.bottom <= safeBounds.bottom + epsilon;
    }

    function resolveMinimumTitleSize(defaultMinimum, minimumByLineCount, lineCount) {
        if (minimumByLineCount && minimumByLineCount.hasOwnProperty(String(lineCount))) {
            return Number(minimumByLineCount[String(lineCount)]);
        }
        return defaultMinimum;
    }

    function maximizeTitleInSafeBounds(layer, safeBounds, centerX, defaultMinimumSize,
            minimumByLineCount, maximumSize, leadingRatio, minimumFillRatio) {
        var lineCount = countTitleLines(layer.textItem.contents);
        var minimumSize = resolveMinimumTitleSize(
            defaultMinimumSize,
            minimumByLineCount,
            lineCount
        );
        if (minimumSize <= 0 || maximumSize < minimumSize) {
            throw new Error("invalid title font-size fit range");
        }
        if (safeBounds.right <= safeBounds.left || safeBounds.bottom <= safeBounds.top) {
            throw new Error("invalid title safe bounds");
        }
        if (leadingRatio <= 0) { throw new Error("invalid title leading ratio"); }
        setTitleSize(layer, minimumSize, leadingRatio, lineCount);
        var minimumBounds = alignTitleInsideSafeBounds(layer, safeBounds, centerX);
        if (!titleFitsSafeBounds(minimumBounds, safeBounds)) {
            throw new Error(
                "title cannot fit the registered safe bounds at the minimum readable font size: " +
                minimumSize + "pt"
            );
        }
        var low = minimumSize;
        var high = maximumSize;
        var best = minimumSize;
        for (var fitAttempt = 0; fitAttempt < 16; fitAttempt++) {
            var candidate = (low + high) / 2;
            setTitleSize(layer, candidate, leadingRatio, lineCount);
            var candidateBounds = alignTitleInsideSafeBounds(layer, safeBounds, centerX);
            if (titleFitsSafeBounds(candidateBounds, safeBounds)) {
                best = candidate;
                low = candidate;
            } else {
                high = candidate;
            }
        }
        setTitleSize(layer, best, leadingRatio, lineCount);
        var finalBounds = alignTitleInsideSafeBounds(layer, safeBounds, centerX);
        var safeWidth = safeBounds.right - safeBounds.left;
        var fillRatio = (finalBounds.right - finalBounds.left) / safeWidth;
        if (minimumFillRatio > 0 && best < maximumSize - 0.1 && fillRatio < minimumFillRatio) {
            throw new Error(
                "title remains visually under-filled after fitting: " + fillRatio +
                " < " + minimumFillRatio
            );
        }
        return {
            enabled: true,
            line_count: lineCount,
            safe_bounds: safeBounds,
            minimum_font_size_pt: minimumSize,
            default_minimum_font_size_pt: defaultMinimumSize,
            minimum_font_size_by_line_count: minimumByLineCount,
            maximum_font_size_pt: maximumSize,
            selected_font_size_pt: best,
            leading_ratio: leadingRatio,
            minimum_fill_ratio: minimumFillRatio,
            actual_fill_ratio: fillRatio,
            final_bounds: finalBounds
        };
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

    function requireTextLayer(container, id, label) {
        var layer = findLayerById(container, id);
        if (!layer) { throw new Error(label + " layer ID not found: " + id); }
        if (layer.typename !== "ArtLayer" || layer.kind !== LayerKind.TEXT) {
            throw new Error(label + " layer is not a text layer: " + id);
        }
        return layer;
    }

    function verifyAndUpdate(layer, target, expected, label) {
        var before = String(layer.textItem.contents);
        if (expected !== null && expected !== "" && normalizeText(before) !== normalizeText(expected)) {
            throw new Error(label + " content mismatch. Expected '" + expected + "' but found '" + before + "'.");
        }
        if (normalizeText(before) !== normalizeText(target)) {
            layer.textItem.contents = target;
        }
        return { before: before, after: String(layer.textItem.contents), layer_id: layer.id };
    }

    function verifyAndUpdatePreservingRanges(layer, target, expected, label) {
        var before = String(layer.textItem.contents);
        if (expected !== null && expected !== "" && normalizeText(before) !== normalizeText(expected)) {
            throw new Error(label + " content mismatch. Expected '" + expected + "' but found '" + before + "'.");
        }
        if (normalizeText(before) === normalizeText(target)) {
            return { before: before, after: before, layer_id: layer.id, style_ranges_preserved: true };
        }

        var layerReference = new ActionReference();
        layerReference.putIdentifier(charIDToTypeID("Lyr "), layer.id);
        var layerDescriptor = executeActionGet(layerReference);
        var textDescriptor = layerDescriptor.getObjectValue(stringIDToTypeID("textKey"));
        var descriptorText = textDescriptor.getString(stringIDToTypeID("textKey"));
        if (normalizeText(descriptorText) !== normalizeText(expected)) {
            throw new Error(label + " action-descriptor content mismatch");
        }
        var terminalReturn = descriptorText.length > 0 && descriptorText.charAt(descriptorText.length - 1) === "\r";
        var replacementText = target;
        if (terminalReturn && replacementText.charAt(replacementText.length - 1) !== "\r") {
            replacementText += "\r";
        }
        var oldLength = descriptorText.length;
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
                var oldTo = rangeDescriptor.getInteger(toKey);
                if (oldTo === terminalEnd) {
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

        var updatedLayer = findLayerById(app.activeDocument, layer.id);
        return {
            before: before,
            after: String(updatedLayer.textItem.contents),
            layer_id: layer.id,
            style_ranges_preserved: true
        };
    }

    function normalizeTitleCharacterColors(layer) {
        var layerReference = new ActionReference();
        layerReference.putIdentifier(charIDToTypeID("Lyr "), layer.id);
        var layerDescriptor = executeActionGet(layerReference);
        var textDescriptor = layerDescriptor.getObjectValue(stringIDToTypeID("textKey"));
        var rangesKey = stringIDToTypeID("textStyleRange");
        if (!textDescriptor.hasKey(rangesKey)) {
            var white = new SolidColor();
            white.rgb.red = 255;
            white.rgb.green = 255;
            white.rgb.blue = 255;
            layer.textItem.color = white;
            return { normalized: true, range_count: 0, rgb: [255, 255, 255] };
        }
        var oldRanges = textDescriptor.getList(rangesKey);
        if (oldRanges.count < 1) {
            throw new Error("title textStyleRange is empty");
        }
        var styleKey = stringIDToTypeID("textStyle");
        var firstRange = oldRanges.getObjectValue(0);
        if (!firstRange.hasKey(styleKey)) {
            throw new Error("first title style range has no textStyle");
        }
        var baseStyle = firstRange.getObjectValue(styleKey);
        var rgbDescriptor = new ActionDescriptor();
        rgbDescriptor.putDouble(stringIDToTypeID("red"), 255);
        rgbDescriptor.putDouble(stringIDToTypeID("green"), 255);
        rgbDescriptor.putDouble(stringIDToTypeID("blue"), 255);
        baseStyle.putObject(
            stringIDToTypeID("color"),
            stringIDToTypeID("RGBColor"),
            rgbDescriptor
        );

        // Collapse every inherited character override to one base style range.
        // Merely recolouring each old range is insufficient: historical PSDs
        // can retain a local yellow emphasis through range-specific overrides.
        var fullText = textDescriptor.getString(stringIDToTypeID("textKey"));
        var collapsedRange = new ActionDescriptor();
        collapsedRange.putInteger(stringIDToTypeID("from"), 0);
        collapsedRange.putInteger(stringIDToTypeID("to"), fullText.length);
        collapsedRange.putObject(styleKey, styleKey, baseStyle);
        var newRanges = new ActionList();
        newRanges.putObject(rangesKey, collapsedRange);
        textDescriptor.putList(rangesKey, newRanges);

        var setReference = new ActionReference();
        setReference.putIdentifier(charIDToTypeID("Lyr "), layer.id);
        var setDescriptor = new ActionDescriptor();
        setDescriptor.putReference(charIDToTypeID("null"), setReference);
        setDescriptor.putObject(
            charIDToTypeID("T   "),
            stringIDToTypeID("textLayer"),
            textDescriptor
        );
        executeAction(charIDToTypeID("setd"), setDescriptor, DialogModes.NO);
        // Photoshop may retain per-character overrides even after every
        // descriptor range reports white. Assigning TextItem.color once more
        // applies the base color to the complete visible text selection and
        // removes inherited yellow emphasis from historical titles.
        var updatedLayer = findLayerById(app.activeDocument, layer.id);
        var uniformWhite = new SolidColor();
        uniformWhite.rgb.red = 255;
        uniformWhite.rgb.green = 255;
        uniformWhite.rgb.blue = 255;
        updatedLayer.textItem.color = uniformWhite;
        return {
            normalized: true,
            source_range_count: oldRanges.count,
            final_range_count: 1,
            rgb: [255, 255, 255]
        };
    }

    var psdFile = new File($psdLiteral);
    var pngFile = new File($pngLiteral);
    currentStage = "open copied PSD";
    doc = app.open(psdFile);

    currentStage = "resolve parent text layers";
    var dateLayer = requireTextLayer(doc, $DateLayerId, "date");
    var timeLayer = requireTextLayer(doc, $TimeLayerId, "time");
    var statusLayer = requireTextLayer(doc, $StatusLayerId, "status");
    var objectiveLayer = requireTextLayer(doc, $ObjectiveLayerId, "objective");

    var changes = {};
    currentStage = "update parent text";
    changes.date = verifyAndUpdate(dateLayer, $dateLiteral, $expectedDateLiteral, "date");
    changes.time = verifyAndUpdate(timeLayer, $timeLiteral, $expectedTimeLiteral, "time");
    changes.status = verifyAndUpdate(statusLayer, $statusLiteral, $expectedStatusLiteral, "status");
    changes.objective = verifyAndUpdatePreservingRanges(objectiveLayer, $objectiveLiteral, $expectedObjectiveLiteral, "objective");

    var smartLayer = findLayerById(doc, $TitleSmartLayerId);
    if (!smartLayer || smartLayer.typename !== "ArtLayer" || smartLayer.kind !== LayerKind.SMARTOBJECT) {
        throw new Error("title smart-object contract mismatch: $TitleSmartLayerId");
    }
    app.activeDocument = doc;
    doc.activeLayer = smartLayer;
    currentStage = "open title smart object";
    executeAction(stringIDToTypeID("placedLayerEditContents"), undefined, DialogModes.NO);
    smartDoc = app.activeDocument;
    if (smartDoc === doc) { throw new Error("Title smart object did not open"); }
    if ($hideTitleAccentOverlayLiteral) {
        currentStage = "hide inherited title accent overlay";
        var accentOverlay = findLayerById(smartDoc, $TitleAccentOverlayLayerId);
        if (!accentOverlay) {
            throw new Error("title accent overlay layer not found: $TitleAccentOverlayLayerId");
        }
        changes.title_accent_overlay = {
            layer_id: accentOverlay.id,
            before_visible: accentOverlay.visible,
            after_visible: false
        };
        accentOverlay.visible = false;
    } else {
        changes.title_accent_overlay = { hidden: false };
    }
    var titleLayer = requireTextLayer(smartDoc, $TitleTextLayerId, "title text");
    var titleInnerBoundsBefore = layerBoundsPx(titleLayer);
    var titleJustificationBefore = String(titleLayer.textItem.justification);
    var titleTextStyleBefore = textStyleSummary(titleLayer);
    currentStage = "update title text";
    changes.title = verifyAndUpdate(titleLayer, $titleLiteral, $expectedTitleLiteral, "title");
    if ($normalizeTitleCharacterColorLiteral) {
        currentStage = "normalize title character colors";
        changes.title_character_color = normalizeTitleCharacterColors(titleLayer);
        titleLayer = requireTextLayer(smartDoc, $TitleTextLayerId, "title text");
    } else {
        changes.title_character_color = { normalized: false };
    }
    var titleCanvas = {
        width: Number(smartDoc.width.as("px")),
        height: Number(smartDoc.height.as("px"))
    };
    if ($titleJustificationLiteral !== "preserve") {
        if ($titleJustificationLiteral === "center") {
            titleLayer.textItem.justification = Justification.CENTER;
        } else if ($titleJustificationLiteral === "left") {
            titleLayer.textItem.justification = Justification.LEFT;
        } else if ($titleJustificationLiteral === "right") {
            titleLayer.textItem.justification = Justification.RIGHT;
        }
    }
    var titleBoundsBeforeCentering = layerBoundsPx(titleLayer);
    var titleTargetCenterX = $titleCenterTargetXLiteral >= 0
        ? $titleCenterTargetXLiteral
        : titleCanvas.width / 2;
    if ($fitTitleLiteral) {
        currentStage = "fit title inside smart-object safe bounds";
        var minimumTitleSizeByLineCount = $minTitleFontSizeByLineCountLiteral;
        var titleSafeBounds = {
            left: $titleSafeLeftLiteral,
            top: $titleSafeTopLiteral,
            right: $titleSafeRightLiteral,
            bottom: $titleSafeBottomLiteral
        };
        try {
            changes.title_fit = maximizeTitleInSafeBounds(
                titleLayer,
                titleSafeBounds,
                titleTargetCenterX,
                $minTitleFontSizeLiteral,
                minimumTitleSizeByLineCount,
                $maxTitleFontSizeLiteral,
                $titleLeadingRatioLiteral,
                $minTitleFillRatioLiteral
            );
        } catch (titleFitError) {
            throw new Error("title safe-bound fitting failed: " + titleFitError.message);
        }
    } else {
        changes.title_fit = {
            enabled: false,
            reason: "job_did_not_request_safe_bound_title_fit"
        };
    }
    titleBoundsBeforeCentering = layerBoundsPx(titleLayer);
    var titleCenterTranslationX = 0;
    if ($centerTitleHorizontallyLiteral) {
        currentStage = "center fitted title";
        var titleCenterBefore = (
            titleBoundsBeforeCentering.left + titleBoundsBeforeCentering.right
        ) / 2;
        titleCenterTranslationX = titleTargetCenterX - titleCenterBefore;
        if (Math.abs(titleCenterTranslationX) > 0.01) {
            titleLayer.translate(UnitValue(titleCenterTranslationX, "px"), UnitValue(0, "px"));
        }
    }
    var titleBoundsBeforeVerticalTranslation = layerBoundsPx(titleLayer);
    currentStage = "apply title vertical offset and typography guards";
    if ($titleTextTranslateYLiteral !== 0) {
        titleLayer.translate(UnitValue(0, "px"), UnitValue($titleTextTranslateYLiteral, "px"));
    }
    var titleInnerBounds = layerBoundsPx(titleLayer);
    var titleCenterAfter = (titleInnerBounds.left + titleInnerBounds.right) / 2;
    var titleCenterDeltaAfter = titleCenterAfter - titleTargetCenterX;
    var titleTextStyleAfter = textStyleSummary(titleLayer);
        var titleDecorationGap = $titleDecorationTopLiteral >= 0
        ? $titleDecorationTopLiteral - titleInnerBounds.bottom
        : null;
    var titleLineCount = $fitTitleLiteral ? changes.title_fit.line_count : countTitleLines(titleLayer.textItem.contents);
    var actualLineGlyphHeight = (titleInnerBounds.bottom - titleInnerBounds.top) / titleLineCount;
    changes.title_typography_guard = {
        before: titleTextStyleBefore,
        after: titleTextStyleAfter,
        minimum_font_size_pt: $fitTitleLiteral
            ? changes.title_fit.minimum_font_size_pt
            : $minTitleFontSizeLiteral,
        requested_selected_font_size_pt: $fitTitleLiteral
            ? changes.title_fit.selected_font_size_pt
            : null,
        reported_text_item_size_pt: titleTextStyleAfter.size_pt,
        font_size_valid: !$fitTitleLiteral || (
            changes.title_fit.selected_font_size_pt >=
                changes.title_fit.minimum_font_size_pt - 0.05
        ),
        line_count: titleLineCount,
        actual_line_glyph_height_px: actualLineGlyphHeight,
        minimum_line_glyph_height_px: $minTitleLineGlyphHeightLiteral,
        line_glyph_height_valid: $minTitleLineGlyphHeightLiteral <= 0 ||
            actualLineGlyphHeight >= $minTitleLineGlyphHeightLiteral,
        decoration_top_px: $titleDecorationTopLiteral,
        actual_decoration_gap_px: titleDecorationGap,
        minimum_decoration_gap_px: $minTitleDecorationGapLiteral,
        decoration_gap_valid: $titleDecorationTopLiteral < 0 ||
            titleDecorationGap >= $minTitleDecorationGapLiteral
    };
    if (!changes.title_typography_guard.font_size_valid) {
        throw new Error("title font size is below the registered readable minimum");
    }
    if (!changes.title_typography_guard.line_glyph_height_valid) {
        throw new Error(
            "title's rendered glyph height per line is below the registered readable minimum: " +
            actualLineGlyphHeight + "px < " + $minTitleLineGlyphHeightLiteral + "px"
        );
    }
    if (!changes.title_typography_guard.decoration_gap_valid) {
        throw new Error(
            "title glyph bounds are too close to or overlap the internal decoration line: " +
            titleDecorationGap + "px < " + $minTitleDecorationGapLiteral + "px"
        );
    }
    changes.title_horizontal_alignment = {
        justification_before: titleJustificationBefore,
        justification_after: String(titleLayer.textItem.justification),
        bounds_before_centering: titleBoundsBeforeCentering,
        bounds_after_centering: titleInnerBounds,
        target_center_x_px: titleTargetCenterX,
        actual_center_x_px: titleCenterAfter,
        applied_translation_x_px: titleCenterTranslationX,
        actual_center_delta_px: titleCenterDeltaAfter,
        maximum_center_delta_px: $maxTitleCenterDeltaLiteral,
        auto_centered: $centerTitleHorizontallyLiteral,
        enforced: $centerTitleHorizontallyLiteral || $titleCenterTargetXLiteral >= 0
    };
    changes.title_inner_vertical_position = {
        before: titleBoundsBeforeVerticalTranslation,
        delta_y_px: $titleTextTranslateYLiteral,
        after: titleInnerBounds
    };
    if (
        changes.title_horizontal_alignment.enforced &&
        Math.abs(titleCenterDeltaAfter) > $maxTitleCenterDeltaLiteral
    ) {
        throw new Error(
            "title horizontal center delta exceeds tolerance: " +
            titleCenterDeltaAfter + "px > " + $maxTitleCenterDeltaLiteral + "px"
        );
    }
    changes.title_canvas_guard = {
        before_bounds: titleInnerBoundsBefore,
        after_bounds: titleInnerBounds,
        canvas: titleCanvas,
        skipped: $skipTitleCanvasGuardLiteral
    };
    var allowedOverflow = {
        left: Math.max(0, -titleInnerBoundsBefore.left),
        top: Math.max(0, -titleInnerBoundsBefore.top),
        right: Math.max(0, titleInnerBoundsBefore.right - titleCanvas.width),
        bottom: Math.max(0, titleInnerBoundsBefore.bottom - titleCanvas.height)
    };
    changes.title_canvas_guard.allowed_source_overflow = allowedOverflow;
    if (!$skipTitleCanvasGuardLiteral && (
        titleInnerBounds.left < -allowedOverflow.left ||
        titleInnerBounds.top < -allowedOverflow.top ||
        titleInnerBounds.right > titleCanvas.width + allowedOverflow.right ||
        titleInnerBounds.bottom > titleCanvas.height + allowedOverflow.bottom
    )) {
        throw new Error("title text exceeds the source title's smart-object overflow allowance");
    }
    currentStage = "save title smart object";
    smartDoc.close(SaveOptions.SAVECHANGES);
    smartDoc = null;

    app.activeDocument = doc;
    currentStage = "apply parent poster geometry";
    smartLayer = findLayerById(doc, $TitleSmartLayerId);
    var titlePositionBefore = layerBoundsPx(smartLayer);
    if ($titleTranslateXLiteral !== 0 || $titleTranslateYLiteral !== 0) {
        smartLayer.translate(
            UnitValue($titleTranslateXLiteral, "px"),
            UnitValue($titleTranslateYLiteral, "px")
        );
    }
    var titlePositionAfter = layerBoundsPx(smartLayer);
    changes.title_position = {
        before: titlePositionBefore,
        delta_x_px: $titleTranslateXLiteral,
        delta_y_px: $titleTranslateYLiteral,
        after: titlePositionAfter
    };
    var statusBounds = layerBoundsPx(statusLayer);
    var dateBounds = layerBoundsPx(dateLayer);
    var timeBounds = layerBoundsPx(timeLayer);
    var objectivePositionBefore = layerBoundsPx(objectiveLayer);
    if ($objectiveTranslateXLiteral !== 0 || $objectiveTranslateYLiteral !== 0) {
        objectiveLayer.translate(
            UnitValue($objectiveTranslateXLiteral, "px"),
            UnitValue($objectiveTranslateYLiteral, "px")
        );
    }
    var objectiveBounds = layerBoundsPx(objectiveLayer);
    changes.objective_position = {
        before: objectivePositionBefore,
        delta_x_px: $objectiveTranslateXLiteral,
        delta_y_px: $objectiveTranslateYLiteral,
        after: objectiveBounds
    };
    var lowerBlockTop = Math.min(statusBounds.top, objectiveBounds.top);
    var titleGap = lowerBlockTop - titlePositionAfter.bottom;
    changes.layout_guard = {
        title_bottom_px: titlePositionAfter.bottom,
        lower_block_top_px: lowerBlockTop,
        actual_gap_px: titleGap,
        minimum_gap_px: $minTitleGapLiteral,
        status_bounds: statusBounds,
        objective_bounds: objectiveBounds
    };
    if ($minTitleGapLiteral >= 0 && titleGap < $minTitleGapLiteral) {
        throw new Error(
            "title block is too close to or overlaps the lower content block: " +
            titleGap + "px < " + $minTitleGapLiteral + "px"
        );
    }

    var timeBlockLeft = Math.min(dateBounds.left, timeBounds.left, statusBounds.left);
    var timeBlockTop = Math.min(dateBounds.top, timeBounds.top, statusBounds.top);
    var timeBlockBottom = Math.max(dateBounds.bottom, timeBounds.bottom, statusBounds.bottom);
    var objectiveTimeGap = timeBlockLeft - objectiveBounds.right;
    var verticalOverlap = Math.max(
        0,
        Math.min(objectiveBounds.bottom, timeBlockBottom) -
        Math.max(objectiveBounds.top, timeBlockTop)
    );
    var canvasBounds = {
        width: Number(doc.width.as("px")),
        height: Number(doc.height.as("px"))
    };
    var objectiveBottomLimit = $objectiveBottomLimitLiteral >= 0
        ? $objectiveBottomLimitLiteral
        : canvasBounds.height;
    changes.objective_safe_area_guard = {
        objective_bounds: objectiveBounds,
        date_bounds: dateBounds,
        time_bounds: timeBounds,
        status_bounds: statusBounds,
        time_block_left_px: timeBlockLeft,
        time_block_top_px: timeBlockTop,
        time_block_bottom_px: timeBlockBottom,
        vertical_overlap_px: verticalOverlap,
        actual_horizontal_gap_px: objectiveTimeGap,
        minimum_horizontal_gap_px: $minObjectiveTimeGapLiteral,
        objective_bottom_limit_px: objectiveBottomLimit,
        canvas: canvasBounds,
        skipped: $skipObjectiveSafeAreaGuardLiteral
    };
    if (!$skipObjectiveSafeAreaGuardLiteral) {
        if (
            objectiveBounds.left < 0 ||
            objectiveBounds.top < 0 ||
            objectiveBounds.right > canvasBounds.width ||
            objectiveBounds.bottom > objectiveBottomLimit
        ) {
            throw new Error("objective text exceeds the registered poster safe area");
        }
        if (
            $minObjectiveTimeGapLiteral >= 0 &&
            verticalOverlap > 0 &&
            objectiveTimeGap < $minObjectiveTimeGapLiteral
        ) {
            throw new Error(
                "objective block is too close to or overlaps the date/time block: " +
                objectiveTimeGap + "px < " + $minObjectiveTimeGapLiteral + "px"
            );
        }
    }

    app.activeDocument = doc;
    currentStage = "save editable PSD and export PNG";
    doc.save();
    var pngOptions = new PNGSaveOptions();
    pngOptions.interlaced = false;
    doc.saveAs(pngFile, pngOptions, true, Extension.LOWERCASE);

    outputText = toJson({
        schema_version: 1,
        source_psd: $sourceLiteral,
        output_psd: psdFile.fsName,
        output_png: pngFile.fsName,
        poster_source_type: "editable_psd",
        poster_editability_grade: "A",
        layer_contract: {
            title_smart_layer_id: $TitleSmartLayerId,
            title_text_layer_id: $TitleTextLayerId,
            date_layer_id: $DateLayerId,
            time_layer_id: $TimeLayerId,
            status_layer_id: $StatusLayerId,
            objective_layer_id: $ObjectiveLayerId
        },
        changes: changes
    });
    doc.close(SaveOptions.DONOTSAVECHANGES);
    doc = null;
} catch (workflowError) {
    throw new Error(currentStage + ": " + workflowError.message);
} finally {
    if (smartDoc) { try { smartDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (smartCloseError) {} }
    if (doc) { try { doc.close(SaveOptions.DONOTSAVECHANGES); } catch (docCloseError) {} }
    app.displayDialogs = previousDialogs;
}
outputText;
"@

    $jsonText = $app.DoJavaScript($jsx)
    $parsed = $jsonText | ConvertFrom-Json
    $parsed | Add-Member -NotePropertyName edited_at_utc `
        -NotePropertyValue ([DateTime]::UtcNow.ToString('o'))
    $formatted = $parsed | ConvertTo-Json -Depth 12
    if ($OutAudit) {
        $auditParent = Split-Path -Parent $OutAudit
        if ($auditParent -and -not (Test-Path -LiteralPath $auditParent)) {
            New-Item -ItemType Directory -Path $auditParent | Out-Null
        }
        [System.IO.File]::WriteAllText(
            [System.IO.Path]::GetFullPath($OutAudit),
            $formatted + [Environment]::NewLine,
            [System.Text.UTF8Encoding]::new($false)
        )
        Write-Output ([System.IO.Path]::GetFullPath($OutAudit))
    } else {
        Write-Output $formatted
    }
    $completed = $true
}
finally {
    if (-not $completed) {
        if (Test-Path -LiteralPath $resolvedOutPsd) {
            Remove-Item -LiteralPath $resolvedOutPsd -Force
        }
        if (Test-Path -LiteralPath $resolvedOutPng) {
            Remove-Item -LiteralPath $resolvedOutPng -Force
        }
    }
    if ($app -and -not $photoshopWasRunning) {
        try { $app.Quit() } catch {}
    }
    if ($app) {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
