$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:PYTHONDONTWRITEBYTECODE = '1'
& 'D:\hakathon_wiut\.venv\Scripts\python.exe' -B src\app.py @args
