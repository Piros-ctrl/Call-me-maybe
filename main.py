import sys
from pprint import pprint
# from .parsing import func_demonstration
import json

def test():
    file = sys.argv[1]
    with open(file, "r") as f:
        jfile = json.load(f)
        for data in jfile:
            print(**data)
            print("\n\n\n\n")
            # func_demonstration()


test() 