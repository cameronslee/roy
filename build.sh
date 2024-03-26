#!/usr/bin/env bash

pyinstaller -F roy.py

pip3 freeze > requirements.txt
