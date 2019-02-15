import os
import subprocess


PROJECT_ROOT_DIR = (
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__))))


def test_flake8():
    p = subprocess.run(['flake8'], cwd=os.path.join(PROJECT_ROOT_DIR, "pyshgp"))
    assert p.returncode == 0
