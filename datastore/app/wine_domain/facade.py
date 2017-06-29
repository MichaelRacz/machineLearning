import app.wine_domain.database as database

def create(classified_wine, log):
    wine = database.create(classified_wine)
    log.log_create(wine.id, classified_wine)
    return wine.id

def retrieve(id):
    wine = database.retrieve(id)
    return wine

def delete(id, log):
    database.delete(id)
    log.log_delete(id)
