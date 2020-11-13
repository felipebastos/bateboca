#!/bin/bash

/bin/bash -c "source .venv/bin/activate"

export FLASK_APP=bateboca
export FLASK_ENV=development

flask run
