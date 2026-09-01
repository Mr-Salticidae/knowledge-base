[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$JobPath
)

$ErrorActionPreference = 'Stop'

function Require-Value($job, [string]$name) {
    $property = $job.PSObject.Properties[$name]
    if ($null -eq $property -or $null -eq $property.Value -or [string]::IsNullOrWhiteSpace([string]$property.Value)) {
        throw "Missing required poster job field: $name"
    }
    return $property.Value
}

function Resolve-JobPath([string]$baseDirectory, [string]$value) {
    if ([System.IO.Path]::IsPathRooted($value)) {
        return [System.IO.Path]::GetFullPath($value)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $baseDirectory $value))
}

function Normalize-PhotoshopText([string]$value) {
    return $value.Replace("`r`n", "`r").Replace("`n", "`r")
}

$resolvedJob = (Resolve-Path -LiteralPath $JobPath).Path
$jobDirectory = Split-Path -Parent $resolvedJob
$job = Get-Content -LiteralPath $resolvedJob -Raw -Encoding UTF8 | ConvertFrom-Json

if ($job.schema_version -ne 1) {
    throw 'poster job schema_version must be 1'
}

$sourcePsd = Resolve-JobPath $jobDirectory ([string](Require-Value $job 'source_psd'))
$outPsd = Resolve-JobPath $jobDirectory ([string](Require-Value $job 'out_psd'))
$outPng = Resolve-JobPath $jobDirectory ([string](Require-Value $job 'out_png'))
$outAudit = Resolve-JobPath $jobDirectory ([string](Require-Value $job 'out_audit'))

$layerContract = $job.layer_contract
if ($null -eq $layerContract) {
    $layerContract = [pscustomobject]@{}
}

$guard = $job.guards
if ($null -eq $guard) {
    $guard = [pscustomobject]@{}
}

$titleFit = $job.title_fit
if ($null -eq $titleFit) {
    $titleFit = [pscustomobject]@{}
}

# Horizontal title geometry is part of the template contract. Requiring it in
# every editable-PSD job prevents a visually off-centre title from passing just
# because it stays inside the smart-object canvas.
$titleJustification = [string](Require-Value $job 'target_title_justification')
$titleCenterTargetX = Require-Value $guard 'title_center_target_x_px'
$maximumTitleCenterDelta = Require-Value $guard 'maximum_title_center_delta_px'

$params = @{
    SourcePsd = $sourcePsd
    OutPsd = $outPsd
    OutPng = $outPng
    TitleText = Normalize-PhotoshopText ([string](Require-Value $job 'target_title'))
    ExpectedTitle = Normalize-PhotoshopText ([string](Require-Value $job 'source_expected_title'))
    DateText = [string](Require-Value $job 'target_date')
    ExpectedDate = [string](Require-Value $job 'source_expected_date')
    TimeText = [string](Require-Value $job 'target_time')
    ExpectedTime = [string](Require-Value $job 'source_expected_time')
    StatusText = Normalize-PhotoshopText ([string](Require-Value $job 'target_status'))
    ExpectedStatus = Normalize-PhotoshopText ([string](Require-Value $job 'source_expected_status'))
    ObjectiveText = Normalize-PhotoshopText ([string](Require-Value $job 'target_objective'))
    ExpectedObjective = Normalize-PhotoshopText ([string](Require-Value $job 'source_expected_objective'))
    OutAudit = $outAudit
    TitleSmartLayerId = if ($layerContract.title_smart_layer_id) { [int]$layerContract.title_smart_layer_id } else { 32 }
    TitleTextLayerId = if ($layerContract.title_text_layer_id) { [int]$layerContract.title_text_layer_id } else { 34 }
    DateLayerId = if ($layerContract.date_layer_id) { [int]$layerContract.date_layer_id } else { 35 }
    TimeLayerId = if ($layerContract.time_layer_id) { [int]$layerContract.time_layer_id } else { 38 }
    StatusLayerId = if ($layerContract.status_layer_id) { [int]$layerContract.status_layer_id } else { 42 }
    ObjectiveLayerId = if ($layerContract.objective_layer_id) { [int]$layerContract.objective_layer_id } else { 5 }
    TitleTranslateX = if ($job.title_translate_x_px) { [double]$job.title_translate_x_px } else { 0 }
    TitleTranslateY = if ($job.title_translate_y_px) { [double]$job.title_translate_y_px } else { 0 }
    TitleTextTranslateY = if ($job.title_text_translate_y_px) { [double]$job.title_text_translate_y_px } else { 0 }
    ObjectiveTranslateX = if ($job.objective_translate_x_px) { [double]$job.objective_translate_x_px } else { 0 }
    ObjectiveTranslateY = if ($job.objective_translate_y_px) { [double]$job.objective_translate_y_px } else { 0 }
    TitleJustification = $titleJustification
    TitleCenterTargetX = [double]$titleCenterTargetX
    MaxTitleCenterDeltaPx = [double]$maximumTitleCenterDelta
    MinTitleGapPx = if ($null -ne $guard.minimum_title_gap_px) { [double]$guard.minimum_title_gap_px } else { 20 }
    MinObjectiveTimeGapPx = if ($null -ne $guard.minimum_objective_time_gap_px) { [double]$guard.minimum_objective_time_gap_px } else { 20 }
    ObjectiveBottomLimitPx = if ($null -ne $guard.objective_bottom_limit_px) { [double]$guard.objective_bottom_limit_px } else { -1 }
}

if ($job.center_title_horizontally -eq $true) {
    $params.CenterTitleHorizontally = $true
}

if ($titleFit.enabled -eq $true) {
    $params.FitTitleToSafeBounds = $true
    $params.MinTitleFontSizePt = [double](Require-Value $titleFit 'minimum_font_size_pt')
    if ($null -ne $titleFit.minimum_font_size_pt_by_line_count) {
        $params.MinTitleFontSizeByLineCountJson = ConvertTo-Json -Compress $titleFit.minimum_font_size_pt_by_line_count
    }
    $resolvedMaximumTitleSize = [double](Require-Value $titleFit 'maximum_font_size_pt')
    if ($null -ne $titleFit.maximum_font_size_pt_by_line_count) {
        $normalizedTargetTitle = Normalize-PhotoshopText ([string](Require-Value $job 'target_title'))
        $titleLineCount = $normalizedTargetTitle.Split("`r").Count
        $lineMaximumProperty = $titleFit.maximum_font_size_pt_by_line_count.PSObject.Properties[[string]$titleLineCount]
        if ($null -ne $lineMaximumProperty) {
            $resolvedMaximumTitleSize = [double]$lineMaximumProperty.Value
        }
    }
    $params.MaxTitleFontSizePt = $resolvedMaximumTitleSize
    $params.TitleLeadingRatio = [double](Require-Value $titleFit 'leading_ratio')
    $params.MinTitleFillRatio = [double](Require-Value $titleFit 'minimum_fill_ratio')
    $params.MinTitleLineGlyphHeightPx = [double](Require-Value $titleFit 'minimum_line_glyph_height_px')
    $safeBounds = $titleFit.safe_bounds_px
    if ($null -eq $safeBounds) {
        throw 'title_fit.safe_bounds_px is required when title fitting is enabled'
    }
    $params.TitleSafeLeftPx = [double](Require-Value $safeBounds 'left')
    $params.TitleSafeTopPx = [double](Require-Value $safeBounds 'top')
    $params.TitleSafeRightPx = [double](Require-Value $safeBounds 'right')
    $params.TitleSafeBottomPx = [double](Require-Value $safeBounds 'bottom')
    $params.TitleDecorationTopPx = [double](Require-Value $titleFit 'decoration_top_px')
    $params.MinTitleDecorationGapPx = [double](Require-Value $titleFit 'minimum_decoration_gap_px')
    if ($titleFit.normalize_character_color -eq $true) {
        $params.NormalizeTitleCharacterColor = $true
    }
    if ($titleFit.hide_accent_overlay -eq $true) {
        $params.HideTitleAccentOverlay = $true
        $params.TitleAccentOverlayLayerId = [int](Require-Value $titleFit 'accent_overlay_layer_id')
    }
}

if ($guard.skip_title_canvas_guard -eq $true) {
    $params.SkipTitleCanvasGuard = $true
}
if ($guard.skip_objective_safe_area_guard -eq $true) {
    $params.SkipObjectiveSafeAreaGuard = $true
}

$editScript = Join-Path $PSScriptRoot 'photoshop_edit_poster.ps1'
& $editScript @params
