# Create Environment "Virtual Environment file path", "Deploy Flag file path"
VENV=./.venv

# Check if not exists VENV, -> create VENV
if [ ! -d $VENV ]; then
    `which python3` -m venv $VENV
fi
`which python3` -m venv $VENV


# install dependencies
$VENV/bin/python -m pip install -r requirements.txt

# run scrapers
$VENV/bin/python src/manage.py dialog
