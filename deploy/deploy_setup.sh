set -e

python3 -m venv deploy/venv
source deploy/venv/bin/activate
pip install -U pip
pip install -r requirements-with-dev.txt
pip install -U .
