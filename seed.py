from app import db
from models import User

db.drop_all()
db.create_all()

CREATE TABLE "Users" (
    "id" int   NOT NULL,
    "username" string   NOT NULL,
    "password" string   NOT NULL,
    "email" string   NOT NULL,
    "residentState" string   NOT NULL,
    "residentCity" string   NOT NULL,
    "residentAddress" string   NOT NULL,
    CONSTRAINT "pk_Users" PRIMARY KEY (
        "id"
     )
);

db.session.commit()