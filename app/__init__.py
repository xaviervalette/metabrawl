from flask import Flask, render_template, request, redirect, url_for, abort
import sys
import os
from dotenv import load_dotenv

load_dotenv()

dataPath=os.environ["BRAWL_COACH_DATAPATH"]
backPath=os.environ["BRAWL_COACH_BACKPATH"]
frontPath=os.environ["BRAWL_COACH_FRONTPATH"]
token=os.environ["BRAWL_COACH_TOKEN"]


from app.functions import *

app = Flask(__name__)

from app import views
