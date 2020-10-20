from flask import Flask
from flask_pymongo import PyMongo
import  click

mongo = PyMongo()


def init_db(app:Flask):
    app.cli.add_command(init_db_command)


@click.command('init-db')
def init_db_command():
    mongo.db.fphone.insert_many(
        [
            {   
                # "id": "03363e5a9d9c4f1ca7a8dc465116c370",
                "uname": "user1",
                "fname": "fuser1",
                "lname": "luser1",
                "dep": "dep1",
                "pos": "pos1",
                "phones": [
                    {"phone": 1111},
                    {"phone": 2222},
                    {"phone": 3333},
                ],
            },
            {
                # "id": "37ab474c0d3c4ed0ba2b08ac99a738b5",
                "uname": "user2",
                "fname": "fuser2",
                "lname": "luser2",
                "dep": "dep1",
                "pos": "pos2",
                "phones": [
                    {"phone": 4444},
                ]
            },
            {
                # "id": "92c962e9587e45218707c38f1cc143e3",
                "uname": "user3",
                "fname": "fuser3",
                "lname": "luser3",
                "dep": "dep1",
                "pos": "pos3",
                "phones": [
                    {"phone": 5555},
                    {"phone": 6666},
                ]
            },
            {
                # "id": "f34ebced615e41e9bca5ca09039f5254",
                "uname": "user4",
                "fname": "fuser4",
                "lname": "luser4",
                "dep": "dep1",
                "pos": "pos4",
                "phones": [
                    {"phone": 7777},
                ]
            },
        ]
    )
    click.echo('initialized test db, name: fphone')


