# Install daemon-template as a Windows service using NSSM (https://nssm.cc)
# Run as Administrator.

$ServiceName = "daemon-template"
$PythonPath = (Get-Command python).Source
$ScriptPath = "$PSScriptRoot\..\..\src\main.py"

if (-not (Get-Command nssm -ErrorAction SilentlyContinue)) {
    Write-Error "NSSM not found. Install from https://nssm.cc or via 'choco install nssm'"
    exit 1
}

nssm install $ServiceName $PythonPath "-m" "src.main"
nssm set $ServiceName AppDirectory (Resolve-Path "$PSScriptRoot\..\..")
nssm set $ServiceName AppEnvironmentExtra "DAEMON_CONFIG=config.toml" "DAEMON_LOG_JSON=true"
nssm set $ServiceName AppStopMethodSkip 0
nssm set $ServiceName AppStopMethodConsole 5000
nssm set $ServiceName AppExit Default Restart
nssm set $ServiceName AppRestartDelay 5000
nssm set $ServiceName Start SERVICE_AUTO_START

Write-Host "Service '$ServiceName' installed. Start with: nssm start $ServiceName"
