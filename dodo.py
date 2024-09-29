import os
from pathlib import Path
import shutil
import subprocess
import tempfile


DOIT_CONFIG = {"backend": "sqlite3", "default_tasks": ["dist"], "verbosity": 2}

repo_path = Path(__file__).parent
os.environ["PYTHONPATH"] = str(repo_path)


def task_test():
    """Run all tests"""

    def run(args):
        args = args or []
        subprocess.run(
            ["python", "-m", "pytest", "-s", "-p", "no:cacheprovider", *args],
            cwd="test",
            check=True,
        )

    return {"actions": [run], "pos_arg": "args"}


def task_lint():
    """Check linting"""

    def run(args):
        args = args or []
        subprocess.run(
            ["flake8", "ruly", "test", "setup.py", "dodo.py", *args]
        )

    return {"actions": [run], "pos_arg": "args"}


def task_check():
    """Pre-deployment check"""
    return {"actions": [], "task_dep": ["test", "lint"]}


def task_docs():
    """Build docs"""

    def run(args):
        args = args or []
        subprocess.run(["sphinx-build", "docs", "build/docs", *args])

    return {"actions": [run], "pos_arg": "args"}


def task_dist():
    """Create dist"""

    def run(args):
        dist_path = repo_path / "dist"
        if dist_path.exists():
            shutil.rmtree(dist_path)
        subprocess.run(["python", "-m", "build", "-sw"])

    return {"actions": [run], "pos_arg": "args"}


def task_plat_test():
    """Run platform tests. Specify platforms in args, otherwise all >=3.6
    python versions will be tested."""

    def run(args):
        ruly_wheel: Path = list((repo_path / "dist").glob("*.whl"))[0]
        tmp_dir = Path(tempfile.gettempdir()) / "ruly-plat-tests"
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        for version in args or [f"3.{version}" for version in range(6, 13)]:

            test_path = tmp_dir / f"test-{version}"
            test_path.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ruly_wheel, test_path / ruly_wheel.name)
            shutil.copytree(repo_path / "test", test_path / "test")
            with open(test_path / "Dockerfile", "w") as f:
                f.write(
                    _dockerfile.format(
                        python_version=version,
                        ruly_wheel_filename=ruly_wheel.name,
                    )
                )

            print("testing on Python", version)
            image = (
                subprocess.run(
                    ["docker", "build", "--quiet", str(test_path)],
                    capture_output=True,
                )
                .stdout.decode("utf-8")
                .strip()
            )
            try:
                subprocess.run(["docker", "run", "-it", "--rm", image])
            finally:
                subprocess.run(["docker", "image", "rm", image])

    return {"actions": [run], "task_dep": ["dist"], "pos_arg": "args"}


_dockerfile = """
FROM python:{python_version}

WORKDIR app

COPY ./{ruly_wheel_filename} ./{ruly_wheel_filename}
RUN pip install ./{ruly_wheel_filename}

COPY test ./test

RUN pip install pytest

CMD ["pytest"]
"""
