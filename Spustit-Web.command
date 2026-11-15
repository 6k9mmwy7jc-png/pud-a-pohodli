#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
echo "Spouštím web Pud a pohodlí..."
open "http://localhost:8080"
python3 app.py
