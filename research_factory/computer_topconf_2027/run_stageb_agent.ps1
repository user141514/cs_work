[CmdletBinding()]
param(
  [ValidateSet('Inspect','Preflight','PreflightClaude','Launch')]
  [string]$Action = 'Inspect',
  [string]$PromptFile = '',
  [string]$SessionId = '',
  [string]$ArmName = 's1-r0',
  [int]$TimeoutSeconds = 240
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = [IO.Path]::GetFullPath((Split-Path -Parent (Split-Path -Parent $PSScriptRoot)))
$RuntimeRoot = [IO.Path]::GetFullPath((Join-Path ([IO.Path]::GetPathRoot($RepoRoot)) 'stageb_agent_runtime'))
$LogRoot = Join-Path $RepoRoot 'external\spec_stageb_logs'
$FreezeReceipt = Join-Path $LogRoot 'stageb_backend_freeze.json'
$SourceArm = Join-Path $RepoRoot 'external\spec_stageb_s1_local'
$OriginalUser = [Environment]::GetFolderPath('UserProfile')
$CodexAuth = Join-Path $OriginalUser '.codex\auth.json'
$ClaudeSettings = Join-Path $OriginalUser '.claude\settings.json'
$BaseSha = '3c0991467af69675afa948c3ada45475a772fbeb'
$ExpectedDiff = @('dataclaw/anonymizer.py','tests/test_anonymizer.py')

$PowerShellCacheRoot = Join-Path $RuntimeRoot 'cache'
New-Item -ItemType Directory -Force -Path $RuntimeRoot,$LogRoot,$PowerShellCacheRoot | Out-Null

function Remove-RuntimePath([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) { return }
  $full = [IO.Path]::GetFullPath($Path)
  $root = $RuntimeRoot.TrimEnd('\') + '\'
  if (-not $full.StartsWith($root,[StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to remove path outside runtime root: $full"
  }
  Remove-Item -LiteralPath $full -Recurse -Force
}

function Get-NativeCodex {
  $p = Join-Path $env:APPDATA 'npm\node_modules\@openai\codex\node_modules\@openai\codex-win32-x64\vendor\x86_64-pc-windows-msvc\bin\codex.exe'
  if (-not (Test-Path -LiteralPath $p)) { throw "Native codex.exe missing: $p" }
  return $p
}

function Get-Claude {
  $c = Get-Command claude.exe -ErrorAction Stop
  return $c.Source
}

function Initialize-Arm([string]$Path) {
  if (-not (Test-Path -LiteralPath $SourceArm)) { throw "Missing source arm: $SourceArm" }
  Remove-RuntimePath $Path
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Path) | Out-Null
  $git = (Get-Command git.exe -ErrorAction Stop).Source
  $savedEap = $ErrorActionPreference
  try {
    $ErrorActionPreference = 'Continue'
    & $git clone --local --no-hardlinks -b windows $SourceArm $Path 1>$null 2>$null
    $cloneExit = $LASTEXITCODE
    if ($cloneExit -ne 0) { throw "S1 clone failed with exit code $cloneExit" }

    & $git -C $Path branch main $BaseSha 1>$null 2>$null
    $branchExit = $LASTEXITCODE
    if ($branchExit -ne 0) {
      $sha = (& $git -C $Path rev-parse main 2>$null).Trim()
      if ($sha -ne $BaseSha) { throw "Unexpected main ref: $sha" }
    }

    $actual = @(& $git -C $Path diff --name-only main windows 2>$null) | Sort-Object
    $diffExit = $LASTEXITCODE
    if ($diffExit -ne 0) { throw "S1 diff failed with exit code $diffExit" }
    $expected = @($ExpectedDiff) | Sort-Object
    if (($actual -join ',') -ne ($expected -join ',')) { throw "S1 diff mismatch: $($actual -join ',')" }

    & $git -C $Path remote remove origin 1>$null 2>$null
    $remoteExit = $LASTEXITCODE
    if ($remoteExit -ne 0) { throw "S1 remote removal failed with exit code $remoteExit" }

    $status = @(& $git -C $Path status --porcelain 2>$null)
    $statusExit = $LASTEXITCODE
    if ($statusExit -ne 0) { throw "S1 status failed with exit code $statusExit" }
    if ($status.Count -ne 0) { throw 'S1 arm dirty after init' }
  }
  finally {
    $ErrorActionPreference = $savedEap
  }
}

function Prepare-ArmEnvironment([string]$ArmName,[string]$ArmPath) {
  $venvRoot = Join-Path $RuntimeRoot 'venvs'
  $venv = Join-Path $venvRoot $ArmName
  Remove-RuntimePath $venv
  New-Item -ItemType Directory -Force -Path $venvRoot | Out-Null

  $uv = (Get-Command uv.exe -ErrorAction Stop).Source
  $savedEap = $ErrorActionPreference
  try {
    $ErrorActionPreference = 'Continue'
    & $uv venv --python 3.12 $venv 1>$null 2>$null
    $venvExit = $LASTEXITCODE
    if ($venvExit -ne 0) { throw "uv venv failed with exit code $venvExit" }

    $pythonExe = Join-Path $venv 'Scripts\python.exe'
    & $uv pip install --python $pythonExe $ArmPath 'pytest==8.3.4' 1>$null 2>$null
    $pipExit = $LASTEXITCODE
    if ($pipExit -ne 0) { throw "uv pip install failed with exit code $pipExit" }
  }
  finally {
    $ErrorActionPreference = $savedEap
  }

  $scripts = Join-Path $venv 'Scripts'
  $pyShim = Join-Path $scripts 'py.cmd'
  $shim = @'
@echo off
if /I "%~1"=="-3" shift
if /I "%~1"=="-3.12" shift
if /I "%~1"=="-3.14" shift
"%~dp0python.exe" %*
'@
  [IO.File]::WriteAllText($pyShim,$shim,[Text.ASCIIEncoding]::new())
  return [pscustomobject]@{ Venv=$venv; Scripts=$scripts; Python=(Join-Path $scripts 'python.exe') }
}

function New-CleanEnvironment([string]$ProfileHome,[string]$CodexHome,[hashtable]$Extra) {
  $keep = @('SystemRoot','WINDIR','ComSpec','PATHEXT','PATH','TEMP','TMP','APPDATA','LOCALAPPDATA','PROGRAMDATA','ProgramFiles','ProgramFiles(x86)','CommonProgramFiles','CommonProgramFiles(x86)','OS','PROCESSOR_ARCHITECTURE','NUMBER_OF_PROCESSORS')
  $h = @{}
  foreach ($k in $keep) {
    $v = [Environment]::GetEnvironmentVariable($k)
    if ($v) { $h[$k] = $v }
  }
  $h['HOME'] = $ProfileHome
  $h['USERPROFILE'] = $ProfileHome
  $h['NO_COLOR'] = '1'
  $h['CI'] = '1'
  $h['PSModuleAnalysisCachePath'] = (Join-Path $PowerShellCacheRoot 'ModuleAnalysisCache')
  if ($CodexHome) { $h['CODEX_HOME'] = $CodexHome }
  if ($Extra) { foreach ($k in $Extra.Keys) { $h[$k] = [string]$Extra[$k] } }
  return $h
}

function Invoke-Process([string]$Exe,[string[]]$ArgumentVector,[hashtable]$Environment,[string]$Cwd,[string]$PromptText,[int]$TimeoutSec) {
  $stamp = [guid]::NewGuid().ToString('N')
  $specFile = Join-Path $RuntimeRoot ($stamp + '.spec.json')
  $outFile = Join-Path $RuntimeRoot ($stamp + '.stdout.txt')
  $errFile = Join-Path $RuntimeRoot ($stamp + '.stderr.txt')
  $helperFile = Join-Path $RuntimeRoot 'invoke-stageb-child.ps1'

  $helper = @'
param([string]$SpecFile)
$ErrorActionPreference = 'Continue'
$spec = Get-Content -LiteralPath $SpecFile -Raw | ConvertFrom-Json
$argv = @($spec.arguments | ForEach-Object { [string]$_ })
$prompt = [string]$spec.prompt
[Console]::Error.WriteLine('STAGEB_HELPER_ARGC=' + $argv.Count)
[Console]::Error.WriteLine('STAGEB_HELPER_ARGS=' + ($argv -join ' || '))
[Console]::Error.WriteLine('STAGEB_HELPER_PROMPT_LENGTH=' + $prompt.Length)
& ([string]$spec.exe) @argv $prompt
exit $LASTEXITCODE
'@
  [IO.File]::WriteAllText($helperFile,$helper,[Text.UTF8Encoding]::new($false))

  $spec = [ordered]@{
    exe = $Exe
    arguments = @($ArgumentVector)
    prompt = $PromptText
  }
  [IO.File]::WriteAllText($specFile,($spec | ConvertTo-Json -Depth 4),[Text.UTF8Encoding]::new($false))

  $snapshot = @{}
  Get-ChildItem Env: | ForEach-Object { $snapshot[$_.Name] = $_.Value }
  try {
    Get-ChildItem Env: | ForEach-Object { Remove-Item ('Env:' + $_.Name) -ErrorAction SilentlyContinue }
    foreach ($k in $Environment.Keys) { Set-Item ('Env:' + $k) ([string]$Environment[$k]) }

    $powershellExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
    $transportArgs = @('-NoProfile','-ExecutionPolicy','Bypass','-File',$helperFile,'-SpecFile',$specFile)
    $p = Start-Process -FilePath $powershellExe -ArgumentList $transportArgs -WorkingDirectory $Cwd -RedirectStandardOutput $outFile -RedirectStandardError $errFile -WindowStyle Hidden -PassThru
  }
  finally {
    Get-ChildItem Env: | ForEach-Object { Remove-Item ('Env:' + $_.Name) -ErrorAction SilentlyContinue }
    foreach ($k in $snapshot.Keys) { Set-Item ('Env:' + $k) ([string]$snapshot[$k]) }
  }

  $finished = $p.WaitForExit($TimeoutSec * 1000)
  if (-not $finished) {
    try { & taskkill.exe /PID $p.Id /T /F *> $null } catch {}
    $timedOut = $true
    $exitCode = $null
  } else {
    $p.WaitForExit()
    $p.Refresh()
    $timedOut = $false
    $exitCode = [int]$p.ExitCode
  }

  $stdout = if(Test-Path $outFile){Get-Content $outFile -Raw}else{''}
  $stderr = if(Test-Path $errFile){Get-Content $errFile -Raw}else{''}
  Remove-Item $specFile,$outFile,$errFile -Force -ErrorAction SilentlyContinue
  return [pscustomobject]@{ ExitCode=$exitCode; TimedOut=$timedOut; StdOut=$stdout; StdErr=$stderr }
}

function Save-Log([string]$Name,[string]$Text) {
  $p = Join-Path $LogRoot $Name
  [IO.File]::WriteAllText($p,$Text,[Text.UTF8Encoding]::new($false))
  return $p
}

function Get-ForbiddenHits([string]$Text) {
  $n = $Text.Replace('\','/').ToLowerInvariant()
  $userNorm = $OriginalUser.Replace('\','/').ToLowerInvariant()
  $repoNorm = $RepoRoot.Replace('\','/').ToLowerInvariant()
  $needles = @(
    ($userNorm + '/.agents/'),
    ($userNorm + '/.codex/plugins/'),
    ($repoNorm + '/graft'),
    'software-engineering-review',
    'code-review-and-quality',
    'using-superpowers',
    '[graft]',
    'skill descriptions were shortened'
  )
  $hits = @()
  foreach ($x in $needles) { if ($n.Contains($x)) { $hits += $x } }
  return @($hits | Select-Object -Unique)
}

function Get-CodexThread([string]$StdOut) {
  foreach ($line in ($StdOut -split [char]10)) {
    if (-not $line.Trim()) { continue }
    try {
      $o = $line.Trim() | ConvertFrom-Json
      if ($o.type -eq 'thread.started' -and $o.thread_id) { return [string]$o.thread_id }
    } catch {}
  }
  return ''
}

function Get-DeepSeekEnv {
  if (-not (Test-Path -LiteralPath $ClaudeSettings)) { throw 'Claude settings missing' }
  $s = Get-Content -LiteralPath $ClaudeSettings -Raw | ConvertFrom-Json
  $h = @{}
  foreach ($k in @('ANTHROPIC_BASE_URL','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_MODEL','ANTHROPIC_DEFAULT_OPUS_MODEL','ANTHROPIC_DEFAULT_SONNET_MODEL','ANTHROPIC_DEFAULT_HAIKU_MODEL','CLAUDE_CODE_SUBAGENT_MODEL')) {
    $p = $s.env.PSObject.Properties[$k]
    if ($p -and [string]$p.Value) { $h[$k] = [string]$p.Value }
  }
  foreach ($k in @('ANTHROPIC_BASE_URL','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_MODEL')) {
    if (-not $h.ContainsKey($k)) { throw "Missing DeepSeek setting: $k" }
  }
  return $h
}

function Test-Codex {
  $profileHome = Join-Path $RuntimeRoot 'profiles\codex-user'
  $codexHome = Join-Path $RuntimeRoot 'profiles\codex-home'
  $arm = Join-Path $RuntimeRoot 'arms\codex-preflight'
  Remove-RuntimePath $profileHome
  Remove-RuntimePath $codexHome
  New-Item -ItemType Directory -Force -Path $profileHome,$codexHome | Out-Null
  if (-not (Test-Path -LiteralPath $CodexAuth)) { throw 'Codex auth.json missing' }
  Copy-Item -LiteralPath $CodexAuth -Destination (Join-Path $codexHome 'auth.json')
  Initialize-Arm $arm

  $exe = Get-NativeCodex
  $version = (& $exe --version).Trim()
  $envClean = New-CleanEnvironment $profileHome $codexHome @{}
  $prompt1 = @'
Runtime-isolation preflight only. Do not modify files.
Run read-only Git commands to verify git diff --name-status main windows resolves and changed files are exactly dataclaw/anonymizer.py and tests/test_anonymizer.py.
Do not inspect parent directories. Do not use web, subagents, skills, plugins, or external project context.
End with exactly STAGEB_CODEX_PREFLIGHT_OK
'@
  $args1 = @('exec','--json','--ignore-user-config','--ignore-rules','-m','gpt-5.6-sol','-c','model_reasoning_effort="xhigh"','-s','workspace-write','-C',$arm)
  $r1 = Invoke-Process $exe $args1 $envClean $arm $prompt1 $TimeoutSeconds
  $l1 = Save-Log 'stageb_codex_preflight_first.jsonl' $r1.StdOut
  $e1 = Save-Log 'stageb_codex_preflight_first.stderr.log' $r1.StdErr
  $thread = Get-CodexThread $r1.StdOut
  $hits1 = @(Get-ForbiddenHits ($r1.StdOut + [Environment]::NewLine + $r1.StdErr))
  $ok1 = (-not $r1.TimedOut) -and ($r1.ExitCode -eq 0) -and $thread -and $r1.StdOut.Contains('STAGEB_CODEX_PREFLIGHT_OK') -and ($hits1.Count -eq 0)
  if (-not $ok1) {
    return [pscustomobject]@{Pass=$false;Backend='codex';Version=$version;Model='gpt-5.6-sol';Effort='xhigh';SessionId=$thread;Reason='first_preflight_failed';ForbiddenHits=$hits1;Logs=@($l1,$e1)}
  }

  $prompt2 = 'Runtime-isolation resume preflight only. Do not modify files. Reply with exactly STAGEB_CODEX_RESUME_OK'
  $args2 = @('exec','resume','--json','--ignore-user-config','--ignore-rules','-m','gpt-5.6-sol','-c','model_reasoning_effort="xhigh"',$thread)
  $r2 = Invoke-Process $exe $args2 $envClean $arm $prompt2 $TimeoutSeconds
  $l2 = Save-Log 'stageb_codex_preflight_resume.jsonl' $r2.StdOut
  $e2 = Save-Log 'stageb_codex_preflight_resume.stderr.log' $r2.StdErr
  $hits2 = @(Get-ForbiddenHits ($r2.StdOut + [Environment]::NewLine + $r2.StdErr))
  $git = (Get-Command git.exe -ErrorAction Stop).Source
  $dirty = @(& $git -C $arm status --porcelain)
  $ok2 = (-not $r2.TimedOut) -and ($r2.ExitCode -eq 0) -and $r2.StdOut.Contains('STAGEB_CODEX_RESUME_OK') -and ($hits2.Count -eq 0) -and ($dirty.Count -eq 0)
  return [pscustomobject]@{Pass=$ok2;Backend='codex';Version=$version;Model='gpt-5.6-sol';Effort='xhigh';SessionId=$thread;Reason=$(if($ok2){'pass'}else{'resume_or_cleanliness_failed'});ForbiddenHits=@($hits1+$hits2|Select-Object -Unique);Logs=@($l1,$e1,$l2,$e2)}
}

function Test-Claude([string]$Generation) {
  $profileHome = Join-Path $RuntimeRoot ("profiles\claude-user-$Generation")
  $arm = Join-Path $RuntimeRoot ("arms\claude-preflight-$Generation")
  Remove-RuntimePath $profileHome
  New-Item -ItemType Directory -Force -Path $profileHome | Out-Null
  Initialize-Arm $arm

  $exe = Get-Claude
  $version = (& $exe --version).Trim()
  $provider = Get-DeepSeekEnv
  $envClean = New-CleanEnvironment $profileHome '' $provider
  $envClean['CLAUDE_CODE_SAFE_MODE'] = '1'
  $session = [guid]::NewGuid().ToString()
  $prompt1 = @'
Runtime-isolation preflight only. Do not modify files.
Run read-only Git commands to verify git diff --name-status main windows resolves and changed files are exactly dataclaw/anonymizer.py and tests/test_anonymizer.py.
Do not inspect parent directories. Do not use web or subagents.
End with exactly STAGEB_CLAUDE_PREFLIGHT_OK
'@
  $args1 = @('-p','--safe-mode','--disable-slash-commands','--model',$provider['ANTHROPIC_MODEL'],'--permission-mode','dontAsk','--allowedTools','Bash,Read,Glob,Grep','--output-format','stream-json','--input-format','text','--verbose','--session-id',$session)
  $r1 = Invoke-Process $exe $args1 $envClean $arm $prompt1 $TimeoutSeconds
  $l1 = Save-Log 'stageb_claude_preflight_first.jsonl' $r1.StdOut
  $e1 = Save-Log 'stageb_claude_preflight_first.stderr.log' $r1.StdErr
  $hits1 = @(Get-ForbiddenHits ($r1.StdOut + [Environment]::NewLine + $r1.StdErr))
  $ok1 = (-not $r1.TimedOut) -and ($r1.ExitCode -eq 0) -and $r1.StdOut.Contains('STAGEB_CLAUDE_PREFLIGHT_OK') -and ($hits1.Count -eq 0)
  if (-not $ok1) {
    return [pscustomobject]@{Pass=$false;Backend='claude-deepseek';Version=$version;Model=$provider['ANTHROPIC_MODEL'];Effort='provider-default';SessionId=$session;Reason='first_preflight_failed';ForbiddenHits=$hits1;Logs=@($l1,$e1);Generation=$Generation;ProfileHome=$profileHome;CodexHome=$null;FirstExitCode=$r1.ExitCode;FirstTimedOut=$r1.TimedOut;FirstMarker=$r1.StdOut.Contains('STAGEB_CLAUDE_PREFLIGHT_OK')}
  }

  $prompt2 = 'Runtime-isolation resume preflight only. Do not modify files. Reply with exactly STAGEB_CLAUDE_RESUME_OK'
  $args2 = @('-p','--safe-mode','--disable-slash-commands','--model',$provider['ANTHROPIC_MODEL'],'--permission-mode','dontAsk','--allowedTools','Bash,Read,Glob,Grep','--output-format','stream-json','--input-format','text','--verbose','--resume',$session)
  $r2 = Invoke-Process $exe $args2 $envClean $arm $prompt2 $TimeoutSeconds
  $l2 = Save-Log 'stageb_claude_preflight_resume.jsonl' $r2.StdOut
  $e2 = Save-Log 'stageb_claude_preflight_resume.stderr.log' $r2.StdErr
  $hits2 = @(Get-ForbiddenHits ($r2.StdOut + [Environment]::NewLine + $r2.StdErr))
  $git = (Get-Command git.exe -ErrorAction Stop).Source
  $dirty = @(& $git -C $arm status --porcelain)
  $ok2 = (-not $r2.TimedOut) -and ($r2.ExitCode -eq 0) -and $r2.StdOut.Contains('STAGEB_CLAUDE_RESUME_OK') -and ($hits2.Count -eq 0) -and ($dirty.Count -eq 0)
  return [pscustomobject]@{Pass=$ok2;Backend='claude-deepseek';Version=$version;Model=$provider['ANTHROPIC_MODEL'];Effort='provider-default';SessionId=$session;Reason=$(if($ok2){'pass'}else{'resume_or_cleanliness_failed'});ForbiddenHits=@($hits1+$hits2|Select-Object -Unique);Logs=@($l1,$e1,$l2,$e2);Generation=$Generation;ProfileHome=$profileHome;CodexHome=$null}
}

function Save-Freeze($Selected,$Codex,$Claude) {
  $obj = [ordered]@{
    schema_version = 1
    frozen_at = (Get-Date).ToString('o')
    status = $(if($Selected -and $Selected.Pass){'PASS'}else{'BLOCKED'})
    backend = $(if($Selected){$Selected.Backend}else{$null})
    cli_version = $(if($Selected){$Selected.Version}else{$null})
    model = $(if($Selected){$Selected.Model}else{$null})
    effort = $(if($Selected){$Selected.Effort}else{$null})
    runtime_root = $RuntimeRoot
    generation = $(if($Selected -and $Selected.PSObject.Properties['Generation']){$Selected.Generation}else{$null})
    profile_home = $(if($Selected -and $Selected.PSObject.Properties['ProfileHome']){$Selected.ProfileHome}else{$null})
    codex_home = $(if($Selected -and $Selected.PSObject.Properties['CodexHome']){$Selected.CodexHome}else{$null})
    secrets_recorded = $false
    codex_attempt = $(if($Codex){@{pass=[bool]$Codex.Pass;reason=$Codex.Reason;forbidden_hits=@($Codex.ForbiddenHits)}}else{$null})
    claude_attempt = $(if($Claude){@{pass=[bool]$Claude.Pass;reason=$Claude.Reason;model=$Claude.Model;forbidden_hits=@($Claude.ForbiddenHits);first_exit_code=$(if($Claude.PSObject.Properties['FirstExitCode']){$Claude.FirstExitCode}else{$null});first_timed_out=$(if($Claude.PSObject.Properties['FirstTimedOut']){$Claude.FirstTimedOut}else{$null});first_marker=$(if($Claude.PSObject.Properties['FirstMarker']){$Claude.FirstMarker}else{$null})}}else{$null})
  }
  [IO.File]::WriteAllText($FreezeReceipt,($obj|ConvertTo-Json -Depth 6),[Text.UTF8Encoding]::new($false))
  return $obj
}

function Run-Preflight {
  $c = Test-Codex
  if ($c.Pass) { return Save-Freeze $c $c $null }
  $generation=(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+([guid]::NewGuid().ToString('N').Substring(0,8))
  $d = Test-Claude $generation
  if ($d.Pass) { return Save-Freeze $d $c $d }
  Save-Freeze $null $c $d | Out-Null
  throw 'No backend passed Stage-B runtime preflight'
}

function Run-ClaudeFallback {
  $mutex = New-Object System.Threading.Mutex($false,'Local\BioPaperStageBClaudeFallback')
  $owned = $false
  try {
    try { $owned = $mutex.WaitOne(($TimeoutSeconds + 90) * 1000) }
    catch [System.Threading.AbandonedMutexException] { $owned = $true }
    if (-not $owned) { throw 'Timed out waiting for Claude fallback owner' }

    if (Test-Path $FreezeReceipt) {
      $existing = Get-Content $FreezeReceipt -Raw | ConvertFrom-Json
      if ($existing.status -eq 'PASS') { return $existing }
    }

    $codexEvidence = $null
    if (Test-Path $FreezeReceipt) {
      $prior = Get-Content $FreezeReceipt -Raw | ConvertFrom-Json
      if ($prior.codex_attempt) {
        $codexEvidence = [pscustomobject]@{
          Pass = [bool]$prior.codex_attempt.pass
          Reason = [string]$prior.codex_attempt.reason
          ForbiddenHits = @($prior.codex_attempt.forbidden_hits)
        }
      }
    }

    $generation=(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+([guid]::NewGuid().ToString('N').Substring(0,8))
    $d = Test-Claude $generation
    if ($d.Pass) { return Save-Freeze $d $codexEvidence $d }
    Save-Freeze $null $codexEvidence $d | Out-Null
    throw 'Claude Code + DeepSeek did not pass Stage-B runtime preflight'
  } finally {
    if ($owned) { try { $mutex.ReleaseMutex() } catch {} }
    $mutex.Dispose()
  }
}

function Run-Launch {
  if (-not $PromptFile) { throw 'Launch requires PromptFile' }
  if (-not (Test-Path -LiteralPath $FreezeReceipt)) { throw 'No backend freeze receipt; run Preflight first' }

  $mutexName = 'Local\BioPaperStageBLaunch_' + ($ArmName -replace '[^A-Za-z0-9_.-]','_')
  $mutex = New-Object System.Threading.Mutex($false,$mutexName)
  $owned = $false
  try {
    try { $owned = $mutex.WaitOne(0) }
    catch [System.Threading.AbandonedMutexException] { $owned = $true }
    if (-not $owned) { throw "Launch already in progress for arm: $ArmName" }

    $freeze = Get-Content -LiteralPath $FreezeReceipt -Raw | ConvertFrom-Json
    if ($freeze.status -ne 'PASS') { throw 'Frozen backend status is not PASS' }
    $arm = Join-Path $RuntimeRoot ('arms\' + $ArmName)
    $venv = Join-Path $RuntimeRoot ('venvs\' + $ArmName)
    if (-not $SessionId) {
      Initialize-Arm $arm
      $armEnv = Prepare-ArmEnvironment $ArmName $arm
    } else {
      if (-not (Test-Path -LiteralPath $arm)) { throw "Missing arm for resume: $arm" }
      $scripts = Join-Path $venv 'Scripts'
      $pythonExe = Join-Path $scripts 'python.exe'
      if (-not (Test-Path -LiteralPath $pythonExe)) { throw "Missing frozen arm environment for resume: $venv" }
      $armEnv = [pscustomobject]@{ Venv=$venv; Scripts=$scripts; Python=$pythonExe }
    }
    $runtimeExtra = @{
      VIRTUAL_ENV = $armEnv.Venv
      PATH = ($armEnv.Scripts + ';' + [Environment]::GetEnvironmentVariable('PATH'))
      PYTHONNOUSERSITE = '1'
      PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }
    $prompt = Get-Content -LiteralPath ([IO.Path]::GetFullPath($PromptFile)) -Raw
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

    if ($freeze.backend -eq 'codex') {
      $profileHome = Join-Path $RuntimeRoot 'profiles\codex-user'
      $codexHome = Join-Path $RuntimeRoot 'profiles\codex-home'
      $envClean = New-CleanEnvironment $profileHome $codexHome $runtimeExtra
      $exe = Get-NativeCodex
      if ($SessionId) { $argv = @('exec','resume','--json','--ignore-user-config','--ignore-rules','-m','gpt-5.6-sol','-c','model_reasoning_effort="xhigh"',$SessionId) }
      else { $argv = @('exec','--json','--ignore-user-config','--ignore-rules','-m','gpt-5.6-sol','-c','model_reasoning_effort="xhigh"','-s','workspace-write','-C',$arm) }
      $r = Invoke-Process $exe $argv $envClean $arm $prompt $TimeoutSeconds
      $sid = $(if($SessionId){$SessionId}else{Get-CodexThread $r.StdOut})
    } else {
      $profileHome = [string]$freeze.profile_home
      $provider = Get-DeepSeekEnv
      $envClean = New-CleanEnvironment $profileHome '' $runtimeExtra
      foreach ($k in $provider.Keys) { $envClean[$k] = $provider[$k] }
      $envClean['CLAUDE_CODE_SAFE_MODE'] = '1'
      $exe = Get-Claude
      $sid = $(if($SessionId){$SessionId}else{[guid]::NewGuid().ToString()})
      $common = @('-p','--safe-mode','--disable-slash-commands','--model',$provider['ANTHROPIC_MODEL'],'--permission-mode','dontAsk','--allowedTools','Bash,Read,Edit,Write,Glob,Grep','--output-format','stream-json','--input-format','text','--verbose')
      if ($SessionId) { $argv = @($common + @('--resume',$sid)) } else { $argv = @($common + @('--session-id',$sid)) }
      $r = Invoke-Process $exe $argv $envClean $arm $prompt $TimeoutSeconds
    }

    $out = Save-Log ($ArmName + '-' + $freeze.backend + '-' + $stamp + '.stdout.jsonl') $r.StdOut
    $err = Save-Log ($ArmName + '-' + $freeze.backend + '-' + $stamp + '.stderr.log') $r.StdErr
    return [pscustomobject]@{Backend=$freeze.backend;SessionId=$sid;ExitCode=$r.ExitCode;TimedOut=$r.TimedOut;StdOutLog=$out;StdErrLog=$err;Arm=$arm}
  }
  finally {
    if ($owned) { try { $mutex.ReleaseMutex() } catch {} }
    $mutex.Dispose()
  }
}

switch ($Action) {
  'Inspect' {
    $f = if(Test-Path $FreezeReceipt){Get-Content $FreezeReceipt -Raw|ConvertFrom-Json}else{$null}
    [pscustomobject]@{RepoRoot=$RepoRoot;RuntimeRoot=$RuntimeRoot;CodexExe=(Get-NativeCodex);ClaudeExe=(Get-Claude);CodexAuthPresent=(Test-Path $CodexAuth);ClaudeSettingsPresent=(Test-Path $ClaudeSettings);FreezeStatus=$(if($f){$f.status}else{'NONE'});FrozenBackend=$(if($f){$f.backend}else{$null})} | ConvertTo-Json -Depth 4
  }
  'Preflight' { Run-Preflight | ConvertTo-Json -Depth 6 }
  'PreflightClaude' { Run-ClaudeFallback | ConvertTo-Json -Depth 6 }
  'Launch' { Run-Launch | ConvertTo-Json -Depth 6 }
}
