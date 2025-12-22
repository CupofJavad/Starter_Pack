import platform
import sys
import subprocess


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return "n/a"


print("python_version:", sys.version.replace("\n", " "))
print("platform:", platform.platform())
print("pip:", run([sys.executable, "-m", "pip", "--version"]))
print("ruff:", run(["ruff", "--version"]))
print("pytest:", run(["pytest", "--version"]))
print("pyright:", run(["pyright", "--version"]))
print("node:", run(["node", "--version"]))
print("pnpm:", run(["pnpm", "--version"]))
print("git:", run(["git", "--version"]))
