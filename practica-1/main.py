__author__ = 'Javier_Orti__Ekaitz'

from pymongo import MongoClient, collection, cursor
from pprint import pprint

import constants.database as dbK

from Models.Person import Person
from Models.University import University
from Models.Company import Company

models = [Person, University, Company]

if __name__ == '__main__':
    #TODO
    # primero conectar la base de datos y pasarla a los 3 modelos en el init_class
    # ejecutar los 3 init_class
    # las consultas todas con aggregate

    client = MongoClient(dbK.DB_ADDRESS, dbK.DB_PORT)
    db = client[dbK.DB_NAME]
    
    
    #Initializate the models:
    for m in models:
        m._init_class(db)
    
    datos = {
        'name': 'Javi',
        'last_name': 'Orti',
        'national_id': '12312x'
    }

    javi = Person(
        name = 'Javi',
        last_name ='Orti',
        gender = 'm',
        national_id = 22333123,
        age=1, 
        city = 'Huelva',
        studies = 'mates',
        #inventao= 2
    )

    javi.save()

    #javi.print()



# Comprobamos que funcionó
    # for m in models:
    #     print(m.required_vars)
    #     print(m.admissible_vars)

    # print("Empieza aca\n")
    # javi = Person()
    # javi.set()

    # # print(javi.admissible_vars)

    pipelineQ1 = [
        {
            '$match': {
                'address':'Huelva'
            }
        }
    ]
    pipelineQ2 = [
        {
            '$match': { 
                'studies': { 
                '$in': ['UPM','UAM'] 
                } 
            }
        }
    ]
    pipelineQ3 = [
        {
            '$group': {
                '_id':'$address'
            }
        }
    ]
    pipelineQ4 = [
        {
            '$geoNear': {
                'near': {
                    'type': 'Point',
                    'coordinates': [35.7040744,139.5577317]
                },
                'distanceField': "distance",
                'includeLocs':"location",
                'spherical': False,
            }
        }
    ]
    pipelineQ5 = []
    pipelineQ6 = [
        {
            '$group': {
                '_id': {
                    'jobs':'UPM'
                },
                'avg_job_cant': {
                    '$avg': {
                        '$size': {
                            '$ifNull': [ '$studies', [] ] 
                        }
                    }
                }
            }
        }
    ]
    pipelineQ7 = [
        {
            '$group': {
                '_id':'$studies',
                'numApariciones': {'$sum':1},

            }
        },
        {
            '$limit':3
        }
    ]
    Q1 = db['person'].aggregate(pipelineQ1)
    Q2 = db['person'].aggregate(pipelineQ2)
    Q3 = db['person'].aggregate(pipelineQ3)
    Q4 = db['person'].aggregate(pipelineQ4)
    Q5 = db['person'].aggregate(pipelineQ5)
    Q6 = db['person'].aggregate(pipelineQ6)
    Q7 = db['person'].aggregate(pipelineQ7)

