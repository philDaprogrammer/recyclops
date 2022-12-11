import logging

from flask import Blueprint, request, Response
from apps.recyclops.models import centers, locations
from DAO.database import db
import json
import csv

""""
Views file: 

module handles all functionality associated 
with the blueprint. Where a blueprint 
is simply a part of the app that 
is responsible for certain tasks/functionality. 
It is essentially a method to scale apps as 
they grow more complex. All blueprint endpoints 
are exposed here. 
"""

recyclopsApp = Blueprint("recyclopsApp", __name__)

"""
base route to serve HTML, CSS, JS, etc .... 
Subject to change if frontend wants 
to serve up static files from different 
server and call API indirectly 
"""

""" 
HTTP GET request to return list 
of recycling centers for a given 
material. 
"""


@recyclopsApp.get("/getLocations")
def getLocations():
    queryParams = request.args.to_dict()

    if "material" not in queryParams.keys():
        print("ERROR, materials param not provided")
        return Response(json.dumps(constructError("Query param 'material' was not provided", 400)),
                        status=400,
                        mimetype="application/json")

    try:
        print(f"Querying for: {queryParams['material']}")
        filtered = {"locations": []}

        # - perform the database query. Please search for 'sqlalchemy queries' for more info
        # - on how the queries operate.
        recyclingCenters = db.session.query(centers.name) \
            .filter(centers.mat == queryParams["material"]).all()

        if len(recyclingCenters) == 0:
            return Response(constructError(f"Could not find any centers for material: {queryParams['material']}", 400),
                            status=400,
                            mimetype="application/json")

        loc = []
        for center in recyclingCenters:
            res = db.session.query(locations.name, locations.lat, locations.lng)\
                .filter(locations.name == center[0]).one()

            loc.append(res)

        for rc in loc:
            filtered["locations"].append({"center name": rc[0], "latitude": rc[1], "longitude": rc[2]})
            
        res = Response(json.dumps(filtered), status=200, mimetype="application=/json")
        return res

    except:
        logging.exception('')
        return Response(json.dumps(constructError("Exception occurred during processing", 500)),
                        status=500,
                        mimetype="application/json")

""" 
HTTP post request to insert data into the 
'centers' table. This will be used to insert 
all database data when recycling center compilation 
is complete
"""


@recyclopsApp.post("/insertLocations")
def createLocations():
    with open("location.csv") as f:
        reader = csv.reader(f)
        next(reader)

        for line in reader:
            db.session.add(locations(line[0], float(line[1]), float(line[1])))
            db.session.commit()

    return Response(json.dumps({"message": "Insertions successful!"}), status=200, mimetype="application/json")


@recyclopsApp.post("/insertCenters")
def createCenters():
    with open("/home/phil/PycharmProjects/442/recyclops/apps/recyclops/centers.csv") as f:
        reader = csv.reader(f)
        next(reader)

        for line in reader:
            db.session.add(centers(int(line[0]), line[1], line[2]))
            db.session.commit()

    return Response(json.dumps({"message": "Insertions successful!"}), status=200, mimetype="application/json")


"""
helper method to construct error messages
"""


def constructError(errorMsg, errorCode):
    return {"Error Message": errorMsg, "error code": errorCode}
