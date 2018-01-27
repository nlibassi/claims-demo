from flask.ext.script import Manager  #version may differ from that of ClaimsAIR
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
import os

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()