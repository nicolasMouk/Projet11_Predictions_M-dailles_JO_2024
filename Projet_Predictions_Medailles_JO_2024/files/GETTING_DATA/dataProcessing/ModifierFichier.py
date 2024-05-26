import pandas as pd

#CODE POUR RAJOUTER LES CATEGORIE ET LE GENRE DANS LES DONNEES ATHLETES
#au debut on avait un csv par catégorie (14 au total), le but est de préciser le genre et la catégorie pour quand on rassemblera,
#on conaitra la catégorie de l'athlète.

file_path = '+100.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='+100'
df["Genre"] = 'Homme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-100.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-100'
df["Genre"] = 'Homme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-90.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-90'
df["Genre"] = 'Homme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-81.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-81'
df["Genre"] = 'Homme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-73.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-73'
df["Genre"] = 'Homme'

df.to_csv(file_path,index=False,encoding='utf-8')


file_path = '-66.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-66'
df["Genre"] = 'Homme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-60.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-60'
df["Genre"] = 'Homme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '+78.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='+78'
df["Genre"] = 'Femme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-78.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-78'
df["Genre"] = 'Femme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-70.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-70'
df["Genre"] = 'Femme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-63.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-63'
df["Genre"] = 'Femme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-57.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-57'
df["Genre"] = 'Femme'

df.to_csv(file_path,index=False,encoding='utf-8')


file_path = '-52.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-52'
df["Genre"] = 'Femme'

df.to_csv(file_path,index=False,encoding='utf-8')

file_path = '-48.csv'

df = pd.read_csv(file_path, encoding='latin1')
df['Catégorie']='-48'
df["Genre"] = 'Femme'

df.to_csv(file_path,index=False,encoding='utf-8')