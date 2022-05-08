import pandas as pd
import numpy as np
import re

import json
import collections
import time
from nltk.tokenize import word_tokenize

lista_chetada = list()
lista_long = list()
    
class recomendador:
     
    def recomendador(recipes):
        
        recipes_final = pd.read_csv('./data/recipes_final.csv')
        recipes_final
        
        with open('./data.json') as file:
            data = json.load(file)

        for i in range(len(data)):
            cat = (data[i]['category'])
            ingr = (data[i]['ingredients'])

        start = time.time()
        recipes_final["tokenized_ingr"] = recipes_final["ingredients"].apply(word_tokenize)
        ("series.apply", (time.time() - start))

        recipes_final['tokenized_ingr'] = recipes_final['tokenized_ingr'].fillna('')
        recipes_final['ingredients'] = recipes_final['ingredients'].fillna('')


        for row in recipes_final['tokenized_ingr']:

            lst = row
            search = ingr

            pn = ([(w) for w in set(lst) if w in search])
            lista_chetada.append(pn)

        recipes_final['ingr_json'] = lista_chetada

        recipes_jon_sin_nan = recipes_final[recipes_final['ingr_json'].astype(bool)]

        #Define a new movies variable to store the preferred movies. Copy the contents of gen_df to movies
        recipes_rec = recipes_jon_sin_nan.copy() 


        #filter based on the condition
        recipes_rec = recipes_rec[(recipes_rec['Category'] == cat)]


        for i in recipes_rec['ingr_json']:
            lenth = len(i)
            lista_long.append(lenth)

        recipes_rec['json_count']= lista_long

        recipes_rec  = recipes_rec.sort_values(by = 'json_count', ascending=False)
        recipes_rec = recipes_rec.reset_index()
        recipes_rec = recipes_rec.drop(recipes_rec.columns[0],axis=1)
        recipes_rec = recipes_rec[(recipes_rec['json_count'] >= 3)]

        #Exportamos el csv:
        recipes_rec.to_csv('./data/recomendado.csv', index=False)



        return recipes_rec
