"""run.py

Starts server to run computational model using "Mesa".
"""
import os
import sys
import getopt

if sys.argv[-1] == "--test":
    os.environ["verification_mode"] = "1"
else:
    os.environ["verification_mode"] = ""

from server import server

server.launch()
