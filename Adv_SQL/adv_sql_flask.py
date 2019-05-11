import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

@app.route("/")
def home_page():
    """List all available api routes."""
    return (
       '<a href="http://127.0.01:5000/api/v1.0/stations">Stations</a><br/>'
       '<a href="http://127.0.01:5000/api/v1.0/precipitation">Precipitation</a><br/>'
       '<a href="http://127.0.01:5000/api/v1.0/tobs">Temperature</a><br/>'
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precipitation_results = (session.query(Measurement.date, Measurement.prcp)
         .order_by(Measurement.date.desc())
         .all())

    # Convert list of tuples into normal list
    precipitation_list = list(precipitation_results)

    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
  
 
    station_results = session.query(Station.station, Station.name, 
              Station.latitude,Station.longitude,Station.elevation).all()

  
    all_stations = []
    for station, name, latitude, longitude, elevation in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation


        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all passenger names"""
    # Query all Temperature Observations for the most recent year of recorded data. 
    latest_temp_data = (session.query(Measurement.date, Measurement.tobs)
         .filter(Measurement.date <= '2017-08-23', Measurement.date >= '2016-08-23')
         .all())

    # Convert list of tuples into normal list
    latest_temp_list = list(latest_temp_data)

    return jsonify(latest_temp_list)


if __name__ == '__main__':
    app.run(debug=True)
