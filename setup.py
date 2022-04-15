from distutils.core import setup
import py2exe
import os
import random
import re
import sqlite3
import time
import glob
from pathlib import Path

setup(zipfile=None,
      options={'py2exe': {"bundle_files": 1}},
      windows=["hackerscript.py"])
