# Import the dependencies.

import numpy as np
import datetime as dt
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
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station                  # Station and Measurement are python Objects.
Measurement = Base.classes.measurement

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)                           # Instantaneous event --> its a sequence which we will put . basically it tells our app to run everything in the middle. Lookout for the end (if __name__) as well.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB

    """Return a list of all precipitations"""
    # Query all 
    previous_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()

    session.close()

    # Convert into dict with date as the key and the value as the precipitation 
    prcp = {date: prcp for date, prcp in precipitation_scores}

    return jsonify(prcp)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(*****************************).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


#################################################
# START, START/END Route
#################################################
@app.route("/api/v1.0/<start>")                       # No end date
@app.route("/api/v1.0/<start>/<end>")                   # we have an end date
def stats(start = None, end = None):
    # Create our session (link) from Python to the DB
    select_stats = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")               # Format start time, end date using strptime function.
        results = session.query(*select_stats).filter(Measurement.date >= start).all()
        session.close()
        stats = list(np.ravel(results))
        return jsonify(stats)

       
    # This is all in --> if end (basically else)
    # Format start time, end date               using strptime function.
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*select_stats).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    stats = list(np.ravel(results))
    return jsonify(stats)
    
#################################################
# Flask Routes
#################################################

if __name__ == '__main__':
    app.run(debug=True)