$ErrorActionPreference='Stop'
$protoRoot=$PSScriptRoot
$pidPath=Join-Path $protoRoot '.runtime/server.pid'
if(-not(Test-Path -LiteralPath $pidPath)){Write-Output 'No recorded background server. Stop a foreground server with Ctrl+C.';exit}
$serverProcessId=[int](Get-Content -LiteralPath $pidPath)
$serverProcess=Get-CimInstance Win32_Process -Filter "ProcessId=$serverProcessId"
if(-not $serverProcess){Write-Output 'Recorded server is no longer running.';exit}
$scriptPath=Join-Path $protoRoot 'server.py'
if($serverProcess.ExecutablePath -ne 'D:\hakathon_wiut\.venv\Scripts\python.exe' -or -not($serverProcess.CommandLine.Contains($scriptPath))){throw 'The recorded process is not this CarDoctor server. No process was stopped.'}
Stop-Process -Id $serverProcessId
Write-Output 'Stopped the recorded local CarDoctor server.'
