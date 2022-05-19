#!/bin/bash
poetry run pytest
watchmedo shell-command --patterns="*.*" --command="poetry run pytest" -R