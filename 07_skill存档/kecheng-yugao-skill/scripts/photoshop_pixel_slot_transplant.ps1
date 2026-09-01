[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$BasePng,

    [Parameter(Mandatory = $true)]
    [string]$DonorPng,

    [Parameter(Mandatory = $true)]
    [string]$OutPng,

    [Parameter(Mandatory = $true)]
    [string]$OutPsd,

    [int]$Left = 680,
    [int]$Top = 1494,
    [int]$Right = 982,
    [int]$Bottom = 1638,

    [string]$OutQaCrop,
    [string]$OutAudit
)

$ErrorActionPreference = 'Stop'

$resolvedBase = (Resolve-Path -LiteralPath $BasePng).Path
$resolvedDonor = (Resolve-Path -LiteralPath $DonorPng).Path
$resolvedOutput = [System.IO.Path]::GetFullPath($OutPng)
$resolvedPsd = [System.IO.Path]::GetFullPath($OutPsd)
if ([System.IO.Path]::GetExtension($resolvedBase).ToLowerInvariant() -ne '.png' -or
    [System.IO.Path]::GetExtension($resolvedDonor).ToLowerInvariant() -ne '.png' -or
    [System.IO.Path]::GetExtension($resolvedOutput).ToLowerInvariant() -ne '.png') {
    throw 'BasePng, DonorPng, and OutPng must all be PNG files.'
}
if ([System.IO.Path]::GetExtension($resolvedPsd).ToLowerInvariant() -ne '.psd') {
    throw 'OutPsd must end in .psd.'
}
if ($Right -le $Left -or $Bottom -le $Top) {
    throw 'The transplant rectangle is invalid.'
}
if (Test-Path -LiteralPath $resolvedOutput) {
    throw "Output PNG already exists: $resolvedOutput"
}
if (Test-Path -LiteralPath $resolvedPsd) {
    throw "Output PSD already exists: $resolvedPsd"
}

foreach ($outputPath in @($resolvedOutput, $resolvedPsd)) {
    $outputParent = Split-Path -Parent $outputPath
    if (-not (Test-Path -LiteralPath $outputParent)) {
        New-Item -ItemType Directory -Path $outputParent | Out-Null
    }
}
if ($OutQaCrop) {
    $resolvedQa = [System.IO.Path]::GetFullPath($OutQaCrop)
    if ([System.IO.Path]::GetExtension($resolvedQa).ToLowerInvariant() -ne '.png') {
        throw 'OutQaCrop must end in .png.'
    }
    if (Test-Path -LiteralPath $resolvedQa) {
        throw "QA crop already exists: $resolvedQa"
    }
    $qaParent = Split-Path -Parent $resolvedQa
    if (-not (Test-Path -LiteralPath $qaParent)) {
        New-Item -ItemType Directory -Path $qaParent | Out-Null
    }
} else {
    $resolvedQa = ''
}

$photoshopWasRunning = [bool](Get-Process -Name Photoshop -ErrorAction SilentlyContinue)
$app = $null
$completed = $false

try {
    $app = New-Object -ComObject Photoshop.Application
    $baseLiteral = ConvertTo-Json -Compress $resolvedBase
    $donorLiteral = ConvertTo-Json -Compress $resolvedDonor
    $outputLiteral = ConvertTo-Json -Compress $resolvedOutput
    $psdLiteral = ConvertTo-Json -Compress $resolvedPsd
    $qaLiteral = ConvertTo-Json -Compress $resolvedQa
    $jsx = @"
var previousDialogs = app.displayDialogs;
app.displayDialogs = DialogModes.NO;
var outputText = null;
var baseDoc = null;
var donorDoc = null;
var renderDoc = null;
var qaDoc = null;
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
    function px(value) { return Number(value.as("px")); }

    var baseFile = new File($baseLiteral);
    var donorFile = new File($donorLiteral);
    var outputFile = new File($outputLiteral);
    var psdFile = new File($psdLiteral);
    baseDoc = app.open(baseFile);
    donorDoc = app.open(donorFile);

    var baseWidth = px(baseDoc.width);
    var baseHeight = px(baseDoc.height);
    var donorWidth = px(donorDoc.width);
    var donorHeight = px(donorDoc.height);
    if (baseWidth !== donorWidth || baseHeight !== donorHeight) {
        throw new Error("Base/donor dimensions differ: " + baseWidth + "x" + baseHeight + " vs " + donorWidth + "x" + donorHeight);
    }
    if ($Left < 0 || $Top < 0 || $Right > baseWidth || $Bottom > baseHeight) {
        throw new Error("Transplant rectangle exceeds the canvas bounds");
    }

    app.activeDocument = donorDoc;
    donorDoc.selection.select([[$Left, $Top], [$Right, $Top], [$Right, $Bottom], [$Left, $Bottom]]);
    donorDoc.selection.copy();
    donorDoc.selection.deselect();

    app.activeDocument = baseDoc;
    if (baseDoc.layers.length > 0) {
        baseDoc.layers[baseDoc.layers.length - 1].name = "historical_poster_base";
    }
    var pasted = baseDoc.paste();
    pasted.name = "date_time_replacement";
    var pastedBounds = pasted.bounds;
    pasted.translate($Left - px(pastedBounds[0]), $Top - px(pastedBounds[1]));

    var psdOptions = new PhotoshopSaveOptions();
    psdOptions.layers = true;
    psdOptions.embedColorProfile = true;
    baseDoc.saveAs(psdFile, psdOptions, true, Extension.LOWERCASE);

    renderDoc = baseDoc.duplicate("poster-render");
    renderDoc.flatten();

    var pngOptions = new PNGSaveOptions();
    pngOptions.interlaced = false;
    renderDoc.saveAs(outputFile, pngOptions, true, Extension.LOWERCASE);

    if ($qaLiteral !== "") {
        qaDoc = renderDoc.duplicate("slot-qa", true);
        var margin = 16;
        var qaLeft = Math.max(0, $Left - margin);
        var qaTop = Math.max(0, $Top - margin);
        var qaRight = Math.min(baseWidth, $Right + margin);
        var qaBottom = Math.min(baseHeight, $Bottom + margin);
        qaDoc.crop([qaLeft, qaTop, qaRight, qaBottom]);
        qaDoc.saveAs(new File($qaLiteral), pngOptions, true, Extension.LOWERCASE);
        qaDoc.close(SaveOptions.DONOTSAVECHANGES);
        qaDoc = null;
    }

    renderDoc.close(SaveOptions.DONOTSAVECHANGES);
    renderDoc = null;

    outputText = toJson({
        schema_version: 2,
        base_png: baseFile.fsName,
        donor_png: donorFile.fsName,
        output_png: outputFile.fsName,
        output_psd: psdFile.fsName,
        poster_source_type: "flattened_date_slot",
        poster_editability_grade: "B",
        width_px: baseWidth,
        height_px: baseHeight,
        slot: { left: $Left, top: $Top, right: $Right, bottom: $Bottom },
        psd_layers: ["historical_poster_base", "date_time_replacement"],
        qa_crop: $qaLiteral
    });
    donorDoc.close(SaveOptions.DONOTSAVECHANGES);
    donorDoc = null;
    baseDoc.close(SaveOptions.DONOTSAVECHANGES);
    baseDoc = null;
} finally {
    if (qaDoc) { try { qaDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (qaCloseError) {} }
    if (renderDoc) { try { renderDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (renderCloseError) {} }
    if (donorDoc) { try { donorDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (donorCloseError) {} }
    if (baseDoc) { try { baseDoc.close(SaveOptions.DONOTSAVECHANGES); } catch (baseCloseError) {} }
    app.displayDialogs = previousDialogs;
}
outputText;
"@

    $jsonText = $app.DoJavaScript($jsx)
    $parsed = $jsonText | ConvertFrom-Json
    $parsed | Add-Member -NotePropertyName edited_at_utc `
        -NotePropertyValue ([DateTime]::UtcNow.ToString('o'))
    $formatted = $parsed | ConvertTo-Json -Depth 10
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
        if (Test-Path -LiteralPath $resolvedOutput) {
            Remove-Item -LiteralPath $resolvedOutput -Force
        }
        if (Test-Path -LiteralPath $resolvedPsd) {
            Remove-Item -LiteralPath $resolvedPsd -Force
        }
        if ($resolvedQa -and (Test-Path -LiteralPath $resolvedQa)) {
            Remove-Item -LiteralPath $resolvedQa -Force
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
