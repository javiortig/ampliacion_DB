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
        studies = 'mates',
        #inventao= 2
    )

    juan.save()

    pepito = Person(
        name = 'pepito',
        last_name ='jose',
        national_id = 44,
        age=30, 
        city = 'malaga',
        studies = 'mates',
        #inventao= 2
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
            '$lookup': {
                'from': 'city',
                'localField': 'city',
                'foreignField': 'id',
                'pipeline': [
                    { '$match': {'name':'Huelva'}},
                    # { '$project': {'_id':0, 'name':'$name'}}
                ],
                'as': 'ciudad'
            }
        },
        { "$unwind": "$ciudad" },
        # { '$addFields': {'city':'$ciudad.name'}},
        # { '$project': {'ciudad':0}}
    ]
    pipelineQ2 = [
        { '$unwind': '$studies'},
        {
            '$lookup': {
                'from': 'university',
                'localField': 'studies.university',
                'foreignField': 'id_uni',
                'pipeline': [
                    { 
                        '$match': {
                            'name': {
                                '$in': ['UAM','UPM']
                            }
                        }
                    },
                    # { '$project': {'_id':0, 'name':'$name'}}
                ],
                'as': 'universidad'
            }
        },
        { "$unwind": "$universidad" },
        # { '$addFields': {'studies':'$universidad.name'}},
        # { '$project': {'universidad':0}}
    ]
    pipelineQ3 = [
        {
            '$lookup': {
                'from': 'city',
                'localField': 'city',
                'foreignField': 'id',
                'pipeline': [
                    { '$project': {'_id':0, 'name':'$name'}}
                ],
                'as': 'ciudad'
            }
        },
        { "$unwind": "$ciudad" },
        {
            '$group': {
                '_id':'$ciudad.name'
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
                'spherical': False,
            }
        },
        { '$limit': 10}
    ]
    # Tablas?
    pipelineQ5 = [
        {
            '$studies.final': { '$gte': 'ISODate("2017-01-01T00:00:00Z'}
        },
    ]
    pipelineQ6 = [
        # { '$unwind': '$estudios'},
        # {
        #     '$lookup': {
        #         'from': 'university',
        #         'localField': 'estudios.university',
        #         'foreignField': 'id_uni',
        #         'pipeline': [
        #             { 
        #                 '$match': {
        #                     'name': {
        #                         '$in': ['UAM','UPM']
        #                     }
        #                 }
        #             },
        #             { '$project': {'_id':0, 'name':'$name'}}
        #         ],
        #         'as': 'universidad'
        #     }
        # },
        # { '$unwind': 'universidad'},
        # { 
        #     '$match': {
        #         'universidad.name':'UPM'
        #     }
        # },
        { '$addFields': {'nombreUniversidad':'$estudios.universidad'}},
        {
            '$match': {
                'nombreUniversidad':'UPM'
            }
        },
        # Falta coger solo el primero de las ocurrencias de _id, hay gente que estudio mas de 1 vez en la UPM
        # {
        #     '$group': {
        #         '_id':'$_id',
        #         'trabajo':'$trabajo'
        #     }
        # },
        {
            '$group': {
                '_id': {
                    'nombreUniversidad':'UPM'
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
        {'$unwind': '$estudios'},
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

    # Q1 = db['person'].aggregate(pipelineQ1)
    # Q2 = db['person'].aggregate(pipelineQ2)
    # Q3 = db['person'].aggregate(pipelineQ3)
    # Q4 = db['company'].aggregate(pipelineQ4)
    # Q5 = db['person'].aggregate(pipelineQ5)
    # Q6 = db['person'].aggregate(pipelineQ6)
    # Q7 = db['person'].aggregate(pipelineQ7)
