"""HF-only bootstrap. Durable output volume is mounted before installation/training."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import time


def run(command, log_path, timeout):
    # Child processes write directly to durable logs: a blocked line read cannot bypass the timeout.
    with log_path.open('w', encoding='utf-8') as log:
        child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        try:
            return child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            child.terminate()
            try:
                child.wait(timeout=30)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=10)
            return 124


def main():
    if os.name != 'posix' or not Path('/run-input/manifest.json').exists():
        raise RuntimeError('This bootstrap runs only in the configured HF Linux job.')
    out = Path('/output')
    out.mkdir(parents=True, exist_ok=True)
    if (out / 'RUN-STATUS.json').exists():
        raise RuntimeError('Use a new run output directory, preserving previous runs.')
    start = time.monotonic()
    state = {'stage': 'installing', 'completed_training': False}
    def save():
        state['elapsed_seconds'] = round(time.monotonic() - start, 2)
        (out / 'RUN-STATUS.json').write_text(json.dumps(state, indent=2), encoding='utf-8')
        print(json.dumps(state), flush=True)
    save()
    # Runtime image lacks GCC, required by Triton's CUDA driver extension.
    if shutil.which('gcc') is None:
        state['stage'] = 'installing_compiler'
        save()
        code = run(['apt-get', 'update'], out / 'compiler-update.log', timeout=300)
        if not code:
            code = run(['apt-get', 'install', '-y', '--no-install-recommends', 'gcc', 'g++', 'libc6-dev'],
                       out / 'compiler-install.log', timeout=300)
        if code or shutil.which('gcc') is None:
            state.update(stage='compiler_install_failed', exit_code=code or 1)
            save()
            return code or 1
    os.environ['CC'] = shutil.which('gcc')
    code = run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check',
                '-r', '/run-input/requirements-remote.txt'], out / 'installation.log', timeout=900)
    if code:
        state.update(stage='installation_failed', exit_code=code)
        save()
        return code
    with (out / 'ENVIRONMENT.txt').open('w', encoding='utf-8') as f:
        subprocess.run([sys.executable, '-m', 'pip', 'freeze'], stdout=f, check=True)
    # Installed dependencies remain in the cloud; no desktop C: download occurs.
    state['stage'] = 'training'
    save()
    code = run([sys.executable, '-u', '/run-input/continuation-worker.py'], out / 'training.log', timeout=max(1, min(2100, int(2280 - (time.monotonic() - start)))))
    state.update(stage='completed' if code == 0 else 'training_failed_or_timed_out',
                 completed_training=code == 0, exit_code=code)
    save()
    return code


if __name__ == '__main__':
    raise SystemExit(main())
