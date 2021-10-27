__author__ = 'Javier_Orti__Ekaitz_Arriola'

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



    javi = Person(
            name = 'Javi',
            last_name ='Orti',
            gender = 'm',
            national_id = 123,
            age=1, 
            city = 'Huelva',
            studies = 'TODO'
        )

    javi.save()

    print(javi.cache.hgetall('p:123'))
    print(javi.cache.keys())

    # modelos = []

    # javi = Person(
    #     name = 'Javi',
    #     last_name ='Orti',
    #     gender = 'm',
    #     national_id = 123,
    #     age=1, 
    #     city = 'Huelva',
    #     studies = [{'university':'Utad','final':'ISODate("2018-04-02T01:23:40Z'}]
    # )
    # modelos.append(javi)

    # juan = Person(
    #     name = 'Juan',
    #     last_name ='Manuel',
    #     national_id = 12321,
    #     age=3, 
    #     city = 'Huelva',
    #     studies = [{'university':'Utad','final':'ISODate("2014-03-02T01:23:40Z'}]
    # )
    # modelos.append(juan)

    # pepito = Person(
    #     name = 'pepito',
    #     last_name ='jose',
    #     national_id = 44,
    #     age=30, 
    #     city = 'vigo',
    #     studies = [{'university':'Utad','final':'ISODate("2015-04-02T01:23:40Z'}]
    # )
    # modelos.append(pepito)

    # josefa = Person(
    #     name = 'josefa',
    #     last_name ='garcia',
    #     national_id = 453,
    #     age=43, 
    #     city = 'malaga',
    #     jobs = [{'name':'Drogeria Encarni'}],
    #     studies = [{'university':'Utad','final':'ISODate("2016-04-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2020-01-02T01:23:40Z'}]
    # )
    # modelos.append(josefa)
    
    # bernardo = Person(
    #     name = 'bernardo',
    #     last_name ='lorca',
    #     national_id = 693,
    #     age=12, 
    #     city = 'gijon',
    #     studies = [{'university':'TBU','final':'ISODate("2021-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2021-08-02T01:23:40Z'}]
    # )
    # modelos.append(bernardo)

    # alba = Person(
    #     name = 'alba',
    #     last_name ='olabarrieta',
    #     national_id = 23,
    #     age=54, 
    #     city = 'Huelva',
    #     jobs = [{'name':'UPM'},{'name':'Peluqueria Paquita'}],
    #     studies = [{'university':'Utad','final':'ISODate("2018-07-02T01:23:40Z'}]
    # )
    # modelos.append(alba)

    # magdalena = Person(
    #     name = 'magdalena',
    #     last_name ='hidalgo',
    #     national_id = 412,
    #     age=95, 
    #     city = 'malaga',
    #     jobs = [{'name':'UAM'}],
    #     studies = [{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UPM','final':'ISODate("2018-07-02T01:23:40Z'},{'university':'UAM','final':'ISODate("2018-07-02T01:23:40Z'}]
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

    