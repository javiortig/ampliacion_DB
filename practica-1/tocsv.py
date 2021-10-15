import pandas as pd
import json


with open('redES.json') as json_file:
    data = json.load(json_file)
    df = pd.DataFrame(data=data)

    #df.to_csv("redES.csv")

    # Comprobamos que los num de telef no se repiten
    l = [x[0] for x in df['telefonos']]

    print(len(list(l)))
    print(len(set(l)))
