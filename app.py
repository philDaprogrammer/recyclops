from flask import Flask
from apps.recyclops.views import recyclopsApp
from DAO import database

# - creating the app object
app = Flask(__name__)

""" 
Main function to perform 
app initialization and 
to start execution
"""

def main():
    # - register all app blue prints
    app.register_blueprint(recyclopsApp)
    # - initialize the database connection
    database.db_init(app, "asap", "A$AP", "recyclops")
    # - run the application
    app.run()


if __name__ == "__main__":
    main()
