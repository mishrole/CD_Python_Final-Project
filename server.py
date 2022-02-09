from peep_app import app
from peep_app.controllers import sharedController, usersController, postsController

if __name__ == '__main__':
    app.run( debug = True, port = 8091 )