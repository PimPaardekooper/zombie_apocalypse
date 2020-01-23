"""run.py

Starts server to run computational model using "Mesa".
"""
import os
import sys
import getopt

help_text = "Choose your mode with --,\n\
            --test: runs test maps,\n\
            --netherland: run the holland map\
            --doorway: doorway tests\
            "

if sys.argv[-1] == "--test":
    os.environ["mode"] = "1"
elif sys.argv[-1] == "--netherland":
    os.environ["mode"] = "2"
elif sys.argv[-1] == "--experiments":
    os.environ["mode"] = "3"
elif sys.argv[-1] == "--doorway":
    os.environ["mode"] = "4"
elif sys.argv[-1] == "--help":
    print(help_text)
    exit(0)
else:
    os.environ["mode"] = "0"

from server import server

server.launch()
