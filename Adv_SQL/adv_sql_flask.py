import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///OneDrive/Documents/GitHub/Adv_SQL/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement 
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# @app.route("/")
# def home_page():
#     """List all available api routes."""
#     return (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/names<br/>"
#         f"/api/v1.0/passengers"
#     )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all passenger names"""
    # Query all passengers
    precipitation_results = (session.query(Measurement.date, Measurement.prcp)
         .order_by(Measurement.date.desc())
         .all())

    # Convert list of tuples into normal list
    precipitation_list = list(precipitation_results)

    return jsonify(precipitation_results)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    station_results = session.query(Station.station, Station.name, 
              Station.latitude,Station.longitude,Station.elevation).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station, name, latitude, longitude, elevation in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation


        all_stations.append(station_dic)

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)