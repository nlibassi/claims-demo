from app import app

"""
try to get this working in future - allows for easy access to 
app's shell env using command 'flask shell'
may be easier with Flask 0.12, using 0.10 for now


from app import db
from app.models import Insured, Claim
#since using older version of Flask (0.10.1), have to import
# flask command line interface
from flask_cli import FlaskCLI

FlaskCLI(app)

@app.shell_context_processor
def ctx():
    return {'db': db, 'Insured': Insured, 'Claim': Claim}

"""