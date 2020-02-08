from app import app, db
from app.models import User, Company, Task

""" 
def create_app(test_config=None):
    # create and configure the app

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


    
    
    
    
    #from . import auth
    #app.register_blueprint(auth.bp)

    return app     """

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Company': Company, 'Task': Task}
if __name__ == "__main__":
    app.run(debug=True)