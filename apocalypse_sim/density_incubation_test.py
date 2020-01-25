from model import Apocalypse
import numpy as np
import random
import sys
import os
import json
import signal

width = 50
height = 50

with open("output.json", "r+") as json_file:
    experiments_json = json.load(json_file)

    print(experiments_json)
