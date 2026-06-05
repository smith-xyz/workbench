# Uninstall daemon-template Windows service. Run as Administrator.

$ServiceName = "daemon-template"

nssm stop $ServiceName
nssm remove $ServiceName confirm

Write-Host "Service '$ServiceName' removed."
