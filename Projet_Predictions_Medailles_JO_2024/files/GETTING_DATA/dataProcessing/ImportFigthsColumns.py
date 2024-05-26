import pandas as pd

# Chemin des fichiers CSV
athletes = 'dataAthletes.csv'
combats = 'dataCombat.csv'

# Lire les fichiers CSV
athletes_df = pd.read_csv(athletes, encoding='utf-8')
combats_df = pd.read_csv(combats, encoding='utf-8')

# Renommer la colonne 'Nom Judoka' pour correspondre à 'Nom Prenom' pour le merge
combats_df.rename(columns={'Nom Judoka': 'Nom Prenom'}, inplace=True)

# Merge des deux DataFrames sur 'Nom Prenom'
merged_df = pd.merge(athletes_df, combats_df, on='Nom Prenom', how='left')

# Renommer la colonne 'Résultats_combats' en 'historique_combat'
merged_df.rename(columns={'Résultats_combats': 'historique_combat'}, inplace=True)

# Sauvegarder le DataFrame mis à jour dans le fichier 'dataAthletes.csv'
merged_df.to_csv(athletes, index=False, encoding='utf-8')

print(f"La colonne 'historique_combat' a été ajoutée au fichier {athletes}")
