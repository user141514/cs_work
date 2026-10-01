[CmdletBinding()]
param(
  [ValidateSet('New','Continue')]
  [string]$Mode,
  [Parameter(Mandatory=$true)]
  [string]$PromptFile,
  [Parameter(Mandatory=$true)]
  [string]$Cwd,
  [Parameter(Mandatory=$true)]
  [string]$SessionDir
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Omp = 'C:\Users\Administrator\.bun\bin\omp.exe'
if (-not (Test-Path -LiteralPath $Omp)) { throw "Missing OMP: $Omp" }
if (-not (Test-Path -LiteralPath $PromptFile)) { throw "Missing prompt: $PromptFile" }
if (-not (Test-Path -LiteralPath $Cwd)) { throw "Missing cwd: $Cwd" }

New-Item -ItemType Directory -Force -Path $SessionDir | Out-Null
$prompt = Get-Content -LiteralPath $PromptFile -Raw

$env:PI_PROXY = 'http://127.0.0.1:7897'

$args = @(
  '--model','openai-codex/gpt-5.6-sol',
  '--thinking','xhigh',
  '--tools','read,bash,edit,write,grep,glob',
  '--no-skills',
  '--no-rules',
  '--no-extensions',
  '--no-title',
  '--auto-approve',
  '--session-dir',$SessionDir,
  '--cwd',$Cwd,
  '--max-time','45m',
  '--print'
)
if ($Mode -eq 'Continue') {
  $args += '--continue'
}

& $Omp @args $prompt
exit $LASTEXITCODE
