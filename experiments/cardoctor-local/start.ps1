$ErrorActionPreference = 'Stop'
$protoRoot = $PSScriptRoot
$protoRuntime = Join-Path $protoRoot '.runtime'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:CARDOCTOR_RUNTIME = $protoRuntime
$env:TEMP = Join-Path $protoRuntime 'tmp'
$env:TMP = $env:TEMP
$env:TORCH_HOME = Join-Path $protoRuntime 'cache/torch'
$env:PIP_CACHE_DIR = Join-Path $protoRuntime 'cache/pip'
Set-Location -LiteralPath $protoRoot
& 'D:\hakathon_wiut\.venv\Scripts\python.exe' server.py
