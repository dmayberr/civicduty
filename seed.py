from app import app
from models import User, db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db.drop_all()
db.create_all()

password = '123123'
hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

u1 = User(username="Darrell",password=hashed_pwd,email="darrell@gmail.com",
    residentState="Georgia",residentCity="Norcross",residentStreetAddress="1405 Beaver Ruin Road",
    residentZipCode=30093)
db.session.add(u1)
db.session.commit()