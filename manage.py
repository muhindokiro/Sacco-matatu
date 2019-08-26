from app import create_app,db
from flask_script import Manager,Server
from app.models import Owners, Assets, Staffs,Routes
from flask_migrate import Migrate, MigrateCommand



# Creating app instance
app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,Owners = Owners,Assets = Assets, Staffs=Staffs, Routes=Routes)

if __name__ == '__main__':
    manager.run()