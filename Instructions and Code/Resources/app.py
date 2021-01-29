# Dependencies
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Create engine
engine = create_engine("selite:///Resources/hawaii.sqlite")

# Reflect database
base = automap_base()
base.prepare(engine, reflect = True)

# Save table references
measurement = base.classes.measurement
station = base.classes.station

# Create session
session = Session(engine)

# Start Flask
app = Flask(__name__)

# Flask routes
@app.route("/")
def home():
    return("")