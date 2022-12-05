from flask import Blueprint, request, Response
from apps.recyclops.models import centers
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
@recyclopsApp.route("/")
def root():
    pass


""" 
HTTP GET request to return list 
of recycling centers for a given 
material. 
"""
@recyclopsApp.get("/getLocations")
def getLocations():
    queryParams = request.args.to_dict()

    if "material" not in queryParams.keys():
        return Response(json.dumps(constructError("Query param 'material' was not provided", 400)),
                        status=400,
                        mimetype="application/json")

    try:
        filtered = {"locations": []}

        # - perform the database query. Please search for 'sqlalchemy queries' for more info
        # - on how the queries operate.
        #recyclingCenters = db.session.query(centers.center_name, centers.latitude, centers.longitude)\
        #    .filter(centers.material == queryParams["material"]).all()

        recyclingCenters = []
        for rc in recyclingCenters:
            filtered["locations"].append({"center name": rc[0], "latitude": rc[1], "longitude": rc[2]})

        return Response(json.dumps(filtered),
                        status=200,
                        mimetype="application=/json")

    except Exception:
        """ write better error handling functionality """
        return Response(json.dumps(constructError("Exception occurred during processing", 500)),
                        status=500,
                        mimetype="application/json")


""" 
HTTP post request to insert data into the 
'centers' table. This will be used to insert 
all database data when recycling center compilation 
is complete
"""
@recyclopsApp.post("/insertTable")
def createCenters():
    with open("/home/phil/PycharmProjects/442/recyclops/location.csv") as f:
        reader = csv.reader(f)
        next(reader)

        for line in reader:
            db.session.add(centers(line[0], float(line[1]), float(line[1])))
            db.session.commit()

    return Response(json.dumps({"message": "Insertions successful!"}), status=200, mimetype="application/json")


"""
helper method to construct error messages
"""
def constructError(errorMsg, errorCode):
    return {"Error Message":  errorMsg, "error code": errorCode}
