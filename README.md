# Programmer's homework


## Usage

### Install package, run cli

    git clone https://github.com/petr-bulusek/species.git
    cd species/
    python3 -m venv env
    . ./env/bin/activate
    pip install -r requirements.txt
    pip install .
    species --help
    species sample_input.xml
    
### Run tests

    . ./env/bin/activate
    pip install pytest
    cd tests/
    pytest