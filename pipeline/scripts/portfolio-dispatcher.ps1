# ==============================================================================
# MODE 2: HACKATHON PORTFOLIO BATCH DISPATCHER
# Multiplexes 4 Google AI Pro accounts across 8 hackathons (17-25 day runway)
# ==============================================================================

param(
    [string]$Task = "solution",
    [int]$Tier = 0,
    [switch]$DryRun = $false
)

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  MODE 2: HACKATHON PORTFOLIO DISPATCHER (Task: $Task | Tier: $(if ($Tier -eq 0) { 'ALL' } else { $Tier }))" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$ManifestPath = if (Test-Path "pipeline/specs/hackathon_portfolio.json") { "pipeline/specs/hackathon_portfolio.json" } else { "specs/hackathon_portfolio.json" }
if (-not (Test-Path $ManifestPath)) {
    Write-Error "Portfolio manifest not found at: $ManifestPath"
    exit 1
}

$Portfolio = Get-Content $ManifestPath | ConvertFrom-Json
$Projects = $Portfolio.projects

if ($Tier -ne 0) {
    $Projects = $Projects | Where-Object { $_.tier -eq $Tier }
}

# Sort projects by urgency (deadline_days ascending)
$Projects = $Projects | Sort-Object deadline_days

Write-Host "Found $($Projects.Count) active project(s) matching criteria:`n" -ForegroundColor Yellow

foreach ($Proj in $Projects) {
    Write-Host ">>> [$($Proj.id)] $($Proj.name)" -ForegroundColor White
    Write-Host "    Tier: $($Proj.tier) | Deadline: in $($Proj.deadline_days) days | Profile: $($Proj.primary_profile)" -ForegroundColor Gray
    Write-Host "    Target Path: $($Proj.path)" -ForegroundColor Gray

    $safeTitle = $Proj.name -replace '"', ''
    $CmdArgs = @(
        "-m", "scripts.orchestrator.task_dispatcher",
        "--task", $Task,
        "--target", $Proj.path,
        "--title", "`"$safeTitle`""
    )

    if ($DryRun) {
        Write-Host "    [DRY RUN] Would execute: python $($CmdArgs -join ' ') using $($Proj.primary_profile)" -ForegroundColor DarkYellow
    } else {
        Write-Host "    Dispatching worker execution..." -ForegroundColor Green
        # Execute synchronously per project or spawn asynchronously with 5s backoff
        $process = Start-Process -FilePath "python" -ArgumentList $CmdArgs -NoNewWindow -PassThru -Wait
        Write-Host "    Completed with exit code: $($process.ExitCode)`n" -ForegroundColor $(if ($process.ExitCode -eq 0) { "Green" } else { "Red" })
    }
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  PORTFOLIO DISPATCH COMPLETE                                         " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
