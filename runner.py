import os
import subprocess
import sys
import tempfile


def run_python(code, timeout=5):
    """Run Python code in a separate process. Returns (output, error_text).
    The child process gets an empty environment, so API keys are not exposed."""
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "main.py")
        with open(path, "w") as f:
            f.write(code)
        try:
            p = subprocess.run(
                [sys.executable, "-I", path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=folder,
                env={"PATH": os.environ.get("PATH", "")},
            )
        except subprocess.TimeoutExpired:
            return "", (
                f"TimeoutError: the program ran for more than {timeout} seconds "
                "(maybe an infinite loop?)"
            )
    return p.stdout[:2000], p.stderr[-2000:]
