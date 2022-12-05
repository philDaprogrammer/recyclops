from DAO.database import db
import sqlalchemy as sa


""" 
model classes used for database actions. 
A model class inherits from a sub-class 
of the instantiated database to declare 
it as a database model. Each class is used 
to represent a table within the database. 
It can be used to create a table, insert data into 
a table, and retrieve data from a table. 

The name of the class needs to match the name
of the table precisely if the table already 
exists. With that, all defined columns also 
need to be declared as class variables. 
"""

class centers(db.Model):
    name = sa.Column(sa.String, primary_key=True)
    lat  = sa.Column(sa.FLOAT)
    lng  = sa.Column(sa.FLOAT)

    def __init__(self, name, lat, lng):
        self.name = name
        self.lat  = lat
        self.lng  = lng
