import pandas as pd

#CE CODE VA PERMETTRE D'OBTENIR LA PLACE MOYENNE DE L'ATHLETE EN REGARDANT LE PLACEMENT DE TOUTE SES ANCIENNES COMPETITIONS
#IL UTILISE LE CSV CLEAN_DATA_COMP QUI REPREND L'historique des compétitions d'un athlète 
df = pd.read_csv('clean_data_comp.csv')

# Remplacer les valeurs '-' par 8 et 'DSQ' par -1
df['Placement'] = df['Placement'].replace('-', 8)
df['Placement'] = df['Placement'].replace('DSQ', -1)

# Convertir la colonne 'Placement' en int
df['Placement'] = df['Placement'].astype(int)

# Calculer la moyenne 
average_placement = df.groupby('Athlete')['Placement'].mean().reset_index()

# Renommer les colonnes pour que cela coressponde aux données
average_placement.columns = ['nom_prenom', 'average placement']
print(average_placement.head())

#on aura plus qu'a importer cette colonne
average_placement.to_csv('average_placements.csv', index=False)
