# Install __SERVICE__ as a Windows service using NSSM (https://nssm.cc)
# Run as Administrator.

$ServiceName = "__SERVICE__"
$BinaryPath = "$PSScriptRoot\..\..\bin\__SERVICE__.exe"

if (-not (Get-Command nssm -ErrorAction SilentlyContinue)) {
    Write-Error "NSSM not found. Install from https://nssm.cc or via 'choco install nssm'"
    exit 1
}

nssm install $ServiceName $BinaryPath
nssm set $ServiceName AppDirectory (Split-Path $BinaryPath)
nssm set $ServiceName AppEnvironmentExtra "DAEMON_LOG_JSON=true"
nssm set $ServiceName AppStopMethodSkip 0
nssm set $ServiceName AppStopMethodConsole 5000
nssm set $ServiceName AppExit Default Restart
nssm set $ServiceName AppRestartDelay 5000
nssm set $ServiceName Start SERVICE_AUTO_START

Write-Host "Service '$ServiceName' installed. Start with: nssm start $ServiceName"
