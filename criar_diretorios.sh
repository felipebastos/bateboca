#!/bin/bash

# Ativando o Python virtual do projeto
. .venv/bin/activate

# Preparando as variáveis do sistema para saber
# qual flask rodar e em que modo.
# "development" deixa o servidor rodando em
# modo debug e etc.
export FLASK_APP=bateboca
export FLASK_ENV=development

flask init-dirs

