#!/bin/sh

activate(){
	. ./.venv/bin/activate
	nohup python3 main.py >/dev/null 2>&1 &
}

activate
