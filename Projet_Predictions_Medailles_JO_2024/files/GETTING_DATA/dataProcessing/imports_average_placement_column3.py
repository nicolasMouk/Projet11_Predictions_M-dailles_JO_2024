import pandas as pd
#permet d'importer la colonne average placement dans le csv final

df_existing = pd.read_csv('dataAthletes.csv')  # Le fichier CSV existant
df_average_placement = pd.read_csv('average_placements.csv')  # Le fichier CSV des moyennes de placement
df_merged = pd.merge(df_existing, df_average_placement, left_on='Nom Prenom', right_on='nom_prenom', how='left')
df_merged.drop(columns=['nom_prenom'], inplace=True)
print(df_merged.head())
df_merged.to_csv('merged_file.csv', index=False)
