import json
from dbco import db


def insertJokes(db, validJokes):
    for joke in validJokes:
        jokeJson = joke.createJson()
        db.jokes.update({'guid': joke.guid}, {'$set': jokeJson}, upsert=True)


def saveJokes(foundJokes):
    """Add valid articles to the database."""
    validJokes = [joke for joke in foundJokes if joke.isValid()]

    # TODO: Remove this mock of validJokes
    validJokes = foundJokes

    if len(validJokes) > 0:
        insertJokes(db, validJokes)
    else:
        print("Jokes all invalid")
