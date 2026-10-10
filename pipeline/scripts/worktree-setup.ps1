# ==============================================================================
# MODE 1: DEEP SURGE WORKTREE GENERATOR
# Sets up 4 isolated Git Worktrees for 4 concurrent Google AI Pro accounts on 1 project
# ==============================================================================

param(
    [string]$BaseDir = "D:\BE_Research_lanes"
)

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  MODE 1: DEEP SURGE - GIT WORKTREE SETUP (4 Accounts, 1 Project)     " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$Worktrees = @(
    @{ Name = "surge-alpha"; Branch = "surge/alpha-core"; Role = "Alpha: Core Domain & Architecture" },
    @{ Name = "surge-beta";  Branch = "surge/beta-adversarial"; Role = "Beta: Adversarial SDET & E2E" },
    @{ Name = "surge-gamma"; Branch = "surge/gamma-audit"; Role = "Gamma: Security & Mutation Auditor" },
    @{ Name = "surge-delta"; Branch = "surge/delta-pitch"; Role = "Delta: OmniDeck Presentation Architect" }
)

foreach ($Wt in $Worktrees) {
    $TargetDir = Join-Path $BaseDir $Wt.Name
    Write-Host "`n>>> Configuring Worktree [$($Wt.Name)] for $($Wt.Role)..." -ForegroundColor Yellow

    if (Test-Path $TargetDir) {
        Write-Host "    Worktree directory already exists at: $TargetDir" -ForegroundColor Green
    } else {
        # Check if branch exists
        $branchExists = git branch --list $Wt.Branch
        if ($branchExists) {
            git worktree add $TargetDir $Wt.Branch
        } else {
            git worktree add $TargetDir -b $Wt.Branch
        }
        Write-Host "    ✅ Created worktree at: $TargetDir (Branch: $($Wt.Branch))" -ForegroundColor Green
    }
}

Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "  ACTIVE WORKTREES CONFIGURED:                                        " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
git worktree list

Write-Host "`nReady for concurrent multi-profile execution:" -ForegroundColor Green
Write-Host "  Account 1 (Master IDE): Active directory (d:\BE_Research)"
Write-Host "  Account 2 (CLI Beta)  : agy --profile account-2 --cwd ../surge-beta"
Write-Host "  Account 3 (CLI Gamma) : agy --profile account-3 --cwd ../surge-gamma"
Write-Host "  Account 4 (CLI Delta) : agy --profile account-4 --cwd ../surge-delta"
