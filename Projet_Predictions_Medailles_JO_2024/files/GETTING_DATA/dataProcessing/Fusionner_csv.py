#Code qui rassemble les fichier csv en un.
import pandas as pd
fichiers=['+100.csv','-100.csv','-90.csv','-81.csv','-73.csv','-66.csv','-60.csv','+78.csv','-78.csv','-70.csv','-63.csv','-57.csv','-52.csv','-48.csv']

dataframes=[]

for fichier in fichiers:
    df=pd.read_csv(fichier, encoding='utf-8')
    dataframes.append(df)

combiner_df = pd.concat(dataframes,ignore_index=True)

combiner_df.to_csv('dataAthletes.csv',index=False,encoding='utf-8')