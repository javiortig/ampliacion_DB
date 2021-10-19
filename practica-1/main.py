__author__ = 'Javier_Orti__Ekaitz'

from pymongo import MongoClient, collection, cursor, GEOSPHERE
from pprint import pprint

import constants.database as dbK

from Models.Person import Person
from Models.University import University
from Models.Company import Company
from Models.ModelCursor import ModelCursor

models = [Person, University, Company]

def initialize_models(db):
    # Initialize city collection
    city_collection = db[dbK.DB_CITY_KEY]
    city_collection.create_index(dbK.DB_CITY_NAME_STR, unique=True)   
    city_collection.create_index([(dbK.DB_CITY_LOCATION_STR, GEOSPHERE)])

    #Initializate the models:
    for m in models:
        m._init_class(db)

if __name__ == '__main__':

    client = MongoClient(dbK.DB_ADDRESS, dbK.DB_PORT)
    db = client[dbK.DB_NAME]
    
    initialize_models(db)

    datos = {
        'name': 'Javi',
        'last_name': 'Orti',
        'national_id': '12312x'
    }

    javi = Person(
        name = 'Javi',
        last_name ='Orti',
        gender = 'm',
        national_id = 123,
        age=1, 
        city = 'Huelva',
        studies = 'mates',
        #inventao= 2
    )

    juan = Person(
        name = 'Juan',
        last_name ='Manuel',
        national_id = 12321,
        age=3, 
        city = 'Huelva',
        studies = "pato"
        #inventao= 2
    )

    juan.save()

    pepito = Person(
        name = 'pepito',
        last_name ='jose',
        national_id = 44,
        age=30, 
        city = 'malaga',
        jobs = [{'name':'UPM'},{'name':'a'}],
        studies = [{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'}]
    )

    pepito.save()
    juan.save()
    javi.save()

    per = Person.load(44)

    per.print()

    # cursor = Person.find([{'$match':{'studies':'mates'}}])

    # personita = cursor.next()
    # personita = cursor.next()

    # personita.print()

    # model_cursor_nuestro = Person.find("Personas de huelva")
    # model_cursor_nuestro.next()
    # while True:
    #     r =  model_cursor_nuestro.next()
    #     if (r is None):
    #         break
    #     else:
    #         r.print()

    # # print(javi.admissible_vars)

    # # col = db['person']
    # # colFind = col.find({'author':'Juan'})
    # # for x in colFind:
    # #     print(x)
    # #     type(x)
    
    # # print(colFind)

    # Q1 = db['person'].find({'address':'Huelva'})
    # for x in Q1:
    #     print(x)
    #     type(x)

    pipelineQ1 = [
        { 
            '$match': {
                'city': 'Huelva'
            }
        }
    ]
    pipelineQ2 = [
        # { 
        #     '$match': {
        #         'estudios.universidad': {
        #             '$in': ['UAM','UPM']
        #         }
        #     }
        # }
        { 
            '$match': {
                'studies': {
                    '$elemMatch': {
                        'university': {
                            '$in': ['UAM','UPM']
                        }
                    }
                }
            }
        }
    ]
    pipelineQ3 = [
        {
            '$group': {
                '_id':'$city'
            }
        },
        { '$project': {'_id':0, 'city':'$_id'}}
    ]
    pipelineQ4 = [
        {
            '$geoNear': {
                'near': {
                    'type': 'Point',
                    'coordinates': [35.7040744,139.5577317]
                },
                'distanceField': "dist.calculated",
                'includeLocs':"dist.location",
                'spherical': 'true',
            }
        },
        { '$limit': 10}
    ]
    # Tablas?
    pipelineQ5 = [
        {
            '$match': {
                'studies.final': { '$gte': 'ISODate("2017-01-01T00:00:00Z'}
            }
        },
    ]
    pipelineQ6 = [
        { '$addFields': {'nombreUniversidad':'$studies.university'}},
        {
            '$match': {
                'jobs.name':'UPM'
            }
        },
        {
            '$group': {
                '_id': {
                    'nombreUniversidad':'$nombreUniversidad',
                },
                'avg_studies_cant': {
                    '$avg': {
                        '$size': {
                            '$ifNull': [ '$nombreUniversidad', [] ] 
                        }
                    }
                }
            }
        }
    ]
    pipelineQ7 = [
        {
            '$group': {
                '_id':'$estudios.universidad',
                'numApariciones': {'$sum':1},

            }
        },
        { '$sort': {'numApariciones':-1}},
        {
            '$limit':3
        }
    ]

    Q1 = db['person'].aggregate(pipelineQ1)
    Q2 = db['person'].aggregate(pipelineQ2)
    Q3 = db['person'].aggregate(pipelineQ3)
    Q4 = db['city'].aggregate(pipelineQ4)
    Q5 = db['person'].aggregate(pipelineQ5)
    Q6 = db['person'].aggregate(pipelineQ6)
    Q7 = db['person'].aggregate(pipelineQ7)


# Comprobamos que funcionó
    # for m in models:
    #     print(m.required_vars)
    #     print(m.admissible_vars)

    # print("Empieza aca\n")
    # javi = Person()
    # javi.set()

    # # print(javi.admissible_vars)

    # # col = db['person']
    # # colFind = col.find({'author':'Juan'})
    # # for x in colFind:
    # #     print(x)
    # #     type(x)
    
    # # print(colFind)

    # Q1 = db['person'].find({'address':'Huelva'})
    print("pato")
    for x in Q4:
        print(x)
        type(x)

