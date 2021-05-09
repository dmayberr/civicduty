-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/DX5cFJ
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


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

