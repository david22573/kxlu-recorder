#!/bin/sh

activate(){
	. ./.venv/bin/activate
}

activate()

nohup python3 main.py > /dev/null 2>&1 &
