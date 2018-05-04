import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from vms import create_app, db, models

config_name = os.getenv('PYTHON_ENV', 'development')
app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
