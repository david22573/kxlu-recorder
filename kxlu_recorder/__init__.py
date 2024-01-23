from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent.as_posix()

DATA = {}


def read_file(category, file):
    with open(f'{PROJECT_ROOT}/data/{category}/{file}', 'r') as f:
        return f.read()


sub_dirs = [x[0] for x in os.walk(f'{PROJECT_ROOT}/data/')][1:]
print(sub_dirs)
