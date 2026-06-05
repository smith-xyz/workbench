# Uninstall __SERVICE__ Windows service. Run as Administrator.

$ServiceName = "__SERVICE__"

nssm stop $ServiceName
nssm remove $ServiceName confirm

Write-Host "Service '$ServiceName' removed."
