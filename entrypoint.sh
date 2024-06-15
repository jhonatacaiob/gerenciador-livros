#!/bin/sh

hatch run alembic upgrade head

hatch run fastapi run ./src/gerenciador_livros/app.py