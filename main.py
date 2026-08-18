import sys
from parsing import func_demonstration
import json


def test():
    file = sys.argv[1]
    with open(file, "r") as f:
        jfile = json.load(f)
        for data in jfile:
            func_demonstration(**data)


test()
