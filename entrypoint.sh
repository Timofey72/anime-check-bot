#!/bin/bash
/wait-for-it.sh db:5432 --timeout=30 --strict -- python app.py