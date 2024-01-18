#!/bin/sh

activate(){
	. ../venv/bin/activate
	python3 ../main.py
}

activate
