# Dependencies
from flask import Flask, jsonify
import numpy as np
from numpy.testing._private.utils import measure
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
    # Gives all routes
    return(f"Welcome to the Surfs Up index!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
		f"/api/v1.0/stations<br>"
		f"/api/v1.0/tobs<br>"
		f"/api/v1.0/(<start>)<br>"
		f"/api/v1.0(<start>/<end>)<br>")
 # Convert the query results to a dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.

    # Create session
    # Store results
@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_results = session.query(measurement.date, measurement.tobs).order_by(measurement.date)

    # Store in dictionary
    date_precip = []
    for row in precip_results:
        dictionary = {}
        dictionary["date"] = row.date
        dictionary["tobs"] = row.tobs
        date_precip.append(dictionary)
    return jsonify(date_precip)     

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    all_stations = session.query(station.station, station.name).all()

    station_list = list(all_stations)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_query = session.query(measurement.date, measurement.tobs).filter(measurement.date >= year_ago).order_by(measurement.date).all()

    tobs_list = list(tobs_query)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_query = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()

    start_query_list = list(start_query)
    return jsonify(start_query_list)

@app.route("/api/v1.0(<start>/<end>)")
def start_end_date(start, end):
    # When given the start and the end date, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_end_query = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()

    start_end_list = list(start_end_query)
    return jsonify(start_query_list)

if __name__ == "__main__":
    app.run(debug=True)