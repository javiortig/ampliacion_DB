__author__ = 'Javier_Orti__Ekaitz_Arriola'

from pymongo import MongoClient, collection, cursor, GEOSPHERE
from pprint import pprint
from datetime import datetime
import json

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



    javi = Person(
            name = 'Juan',
            last_name ='Manuel',
            gender = 'm',
            national_id = 312321,
            age=35, 
            city = 'Huelva',
            studies = [{'university':'Utad','final':datetime.strptime('19/04/2000', "%d/%m/%Y")},
                {'university':'UPM','final':datetime.strptime('24/11/1998', "%d/%m/%Y")}],
            jobs = [{'company': 'Amazon','final':datetime.strptime('17/07/2005', "%d/%m/%Y")},
                {'company': 'Google','final': None}]
    )

    javi.save()

    print(javi.cache.keys())
    
    persona = Person.load(312321)
    print(persona) 
    modelos = []

    # javi = Person(
    #     name = 'Javi',
    #     last_name ='Orti',
    #     gender = 'm',
    #     national_id = 123,
    #     age=1, 
    #     city = 'Huelva',
    #     studies = [{'university':'Utad','final':datetime.strptime('24/11/1998', "%d/%m/%Y")}]
    # )
    # modelos.append(javi)

    # juan = Person(
    #     name = 'Juan',
    #     last_name ='Manuel',
    #     national_id = 12321,
    #     age=3, 
    #     city = 'Huelva',
    #     studies = [{'university':'Utad','final':datetime.strptime('02/03/2014', "%d/%m/%Y")}]
    # )
    # modelos.append(juan)

    # pepito = Person(
    #     name = 'pepito',
    #     last_name ='jose',
    #     national_id = 44,
    #     age=30, 
    #     city = 'vigo',
    #     studies = [{'university':'Utad','final':datetime.strptime('02/04/2015', "%d/%m/%Y")}]
    # )
    # modelos.append(pepito)
    
    # josefa = Person(
    #     name = 'josefa',
    #     last_name ='garcia',
    #     national_id = 453,
    #     age=43, 
    #     city = 'malaga',
    #     jobs = [{'name':'Drogeria Encarni'}],
    #     studies = [{'university':'Utad','final':datetime.strptime('02/04/2014', "%d/%m/%Y")},
    #     {'university':'UPM','final':datetime.strptime('30/12/2018', "%d/%m/%Y")}]
    # )
    # modelos.append(josefa)
    
    # bernardo = Person(
    #     name = 'bernardo',
    #     last_name ='lorca',
    #     national_id = 693,
    #     age=12, 
    #     city = 'gijon',
    #     jobs = [{'name':'DrogueriaEncarni'}],
    #     studies = [{'university':'TBU','final':datetime.strptime('14/11/2012', "%d/%m/%Y")},{'university':'UAM','final':datetime.strptime('02/07/2019', "%d/%m/%Y")}]
    # )
    # modelos.append(bernardo)

    # alba = Person(
    #     name = 'alba',
    #     last_name ='olabarrieta',
    #     national_id = 23,
    #     age=54, 
    #     city = 'Huelva',
    #     jobs = [{'name':'UPM'},{'name':'Peluqueria Paquita'}],
    #     studies = [{'university':'Utad','final':datetime.strptime('02/01/2017', "%d/%m/%Y")}]
    # )
    # modelos.append(alba)

    # magdalena = Person(
    #     name = 'magdalena',
    #     last_name ='hidalgo',
    #     national_id = 412,
    #     age=95, 
    #     city = 'malaga',
    #     jobs = [{'name':'UAM'}],
    #     studies = [{'university':'UPM','final':datetime.strptime('02/02/2011', "%d/%m/%Y")},{'university':'UAM','final':datetime.strptime('02/02/2012', "%d/%m/%Y")},{'university':'UPM','final':datetime.strptime('02/02/2013', "%d/%m/%Y")},{'university':'UAM','final':datetime.strptime('02/02/2014', "%d/%m/%Y")},{'university':'UPM','final':datetime.strptime('02/02/2015', "%d/%m/%Y")},{'university':'UAM','final':datetime.strptime('02/02/2016', "%d/%m/%Y")},{'university':'UPM','final':datetime.strptime('02/02/2017', "%d/%m/%Y")},{'university':'UAM','final':datetime.strptime('02/02/2018', "%d/%m/%Y")},{'university':'UPM','final':datetime.strptime('02/02/2019', "%d/%m/%Y")},{'university':'UAM','final':datetime.strptime('02/02/2020', "%d/%m/%Y")}]
    # )
    # modelos.append(magdalena)

    # droEncarni = Company(
    #     cif = '3432432G',
    #     name = 'DrogueriaEncarni',
    #     city = 'malaga',
    # )
    # modelos.append(droEncarni)

    # peluPaquita = Company(
    #     cif = '4342112L',
    #     name = 'PeluqueriaPaquita',
    #     city = 'vigo',
    # )
    # modelos.append(peluPaquita)

    # UAM = University(
    #     cif = '2334210F',
    #     name = 'UAM',
    #     city = 'madrid',
    # )
    # modelos.append(UAM)

    # UPM = University(
    #     cif = '7433931A',
    #     name = 'UAM',
    #     city = 'madrid',
    # )
    # modelos.append(UPM)

    # Utad = University(
    #     cif = '5434531K',
    #     name = 'Utad',
    #     city = 'madrid',
    # )
    # modelos.append(Utad)

    # TBU = University(
    #     cif = '3272591Y',
    #     name = 'TBU',
    #     city = 'gijon'
    # )
    # modelos.append(TBU)

    # for x in modelos:
    #     x.save()

    # pipelineQ1 = [
    #     { 
    #         '$match': {
    #             'city': 'Huelva'
    #         }
    #     }
    # ]
    # pipelineQ2 = [
    #     # { 
    #     #     '$match': {
    #     #         'estudios.universidad': {
    #     #             '$in': ['UAM','UPM']
    #     #         }
    #     #     }
    #     # }
    #     { 
    #         '$match': {
    #             'studies': {
    #                 '$elemMatch': {
    #                     'university': {
    #                         '$in': ['UAM','UPM']
    #                     }
    #                 }
    #             }
    #         }
    #     }
    # ]
    # pipelineQ3 = [
    #     {
    #         '$group': {
    #             '_id':'$city'
    #         }
    #     },
    #     { '$project': {'_id':0, 'city':'$_id'}}
    # ]
    # pipelineQ4 = [
    #     {
    #         '$geoNear': {
    #             'near': { 'type': "Point", 'coordinates': [ -73.98142 , 40.71782 ] },
    #             'key': "location",
    #             'distanceField': "dist.calculated"
    #         }
    #     },
    #     { '$limit': 10 },
    #     {
    #         '$lookup': {
    #             'from': 'person',
    #             'localField': 'name',
    #             'foreignField': 'city',
    #             'as': 'persona'
    #         }
    #     },
    #     { '$project': {'_id':0, 'persona':1}},
    #     { "$unwind": "$persona" },
    #     { '$limit': 10 },
    # ]
    # pipelineQ5 = [
    #     {
    #         '$match': {
    #             'studies.final': { '$gte': datetime.strptime('01/01/2017', "%d/%m/%Y")}
    #         }
    #     },
    # ]
    # pipelineQ6 = [
    #     { "$unwind": "$jobs" },
    #     { '$addFields': {'nombreUniversidad':'$studies.university'}},
    #     { '$addFields': {'nombreTrabajo':'$jobs.name'}},
    #     {
    #         '$match': {
    #             'nombreTrabajo':'UPM'
    #         }
    #     },
    #     {
    #         '$group': {
    #             '_id': {
    #                 'nombreTrabajo':'$nombreTrabajo',
    #             },
    #             'avg_studies_cant': {
    #                 '$avg': {
    #                     '$size': {
    #                         '$ifNull': [ '$nombreUniversidad', [] ] 
    #                     }
    #                 }
    #             }
    #         }
    #     },
    #     { '$project': {'_id':0}}
    # ]
    # pipelineQ7 = [
    #     { "$unwind": "$studies" },
    #     {
    #         '$group': {
    #             '_id':'$studies.university',
    #             'numApariciones': {'$sum':1},

    #         }
    #     },
    #     { '$sort': {'numApariciones':-1}},
    #     {
    #         '$limit':3
    #     }
    # ]

    # # Q1 = db['person'].aggregate(pipelineQ1)
    # # Q2 = db['person'].aggregate(pipelineQ2)
    # Q1 = Person.find(pipelineQ1)
    # Q2 = Person.find(pipelineQ2)
    # Q3 = db['person'].aggregate(pipelineQ3)
    # Q4 = db['city'].aggregate(pipelineQ4)
    # # Q5 = db['person'].aggregate(pipelineQ5)
    # Q5 = Person.find(pipelineQ5)
    # Q6 = db['person'].aggregate(pipelineQ6)
    # Q7 = db['person'].aggregate(pipelineQ7)


    # print("\n\nQueries: \nQ1")
    # while True:
    #     x = Q1.next()
    #     if not x:
    #         print("\nQ2")
    #         break;
    #     x.print()
    
    # while True:
    #     x = Q2.next()
    #     if not x:
    #         print("\nQ3")
    #         break;
    #     x.print()
    
    # for x in Q3:
    #     print(x)
    # print("\nQ4")

    # for x in Q4:
    #     print(x)
    # print("\nQ5")

    # while True:
    #     x = Q5.next()
    #     if not x:
    #         print("\nQ6")
    #         break;
    #     x.print()
    #     # db['tabla'].insert_one(x.data)

    # for x in Q6:
    #     print(x)
    # print("\nQ7")

    # for x in Q7:
    #     print(x)
    # print("\n")


    
