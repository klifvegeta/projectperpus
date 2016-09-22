from main import *
from models import *

def dbinit():
    db.drop_all()
    db.create_all()
    db.session.add(User(username='singgih', firstname='klif',
                         lastname='singgih', password='usaha',
                         email='klifvegeta@gmail.com',
                         active=True))
    db.session.commit()

if __name__ == "__main__":
    dbinit()