import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Charger les données depuis un fichier CSV
data = pd.read_csv('/Users/bodeloison/Documents/projet JO/csv/+100.csv')

# Fonction pour rechercher le placement d'un athlète dans le fichier CSV
def find_placement(athlete_name):
    athlete_row = data.loc[data['Nom Prenom'] == athlete_name]
    if not athlete_row.empty:
        return athlete_row.iloc[0]['Medailles d\'Or ALL']
    else:
        print(f"Athlète {athlete_name} non trouvé dans les données.")
        return None

# Exemple de transformation pour créer des paires de combats
def create_pairs(data):
    pairs = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            athlete1 = data.iloc[i]
            athlete2 = data.iloc[j]
            pairs.append({
                'athlete1_name': athlete1['Nom Prenom'],
                'athlete2_name': athlete2['Nom Prenom'],
                'athlete1_placement': athlete1['Medailles d\'Or ALL'],
                'athlete2_placement': athlete2['Medailles d\'Or ALL'],
                'winner': 1 if athlete1['Medailles d\'Or ALL'] > athlete2['Medailles d\'Or ALL'] else 0
            })
            pairs.append({
                'athlete1_name': athlete2['Nom Prenom'],
                'athlete2_name': athlete1['Nom Prenom'],
                'athlete1_placement': athlete2['Medailles d\'Or ALL'],
                'athlete2_placement': athlete1['Medailles d\'Or ALL'],
                'winner': 1 if athlete2['Medailles d\'Or ALL'] > athlete1['Medailles d\'Or ALL'] else 0
            })
    return pd.DataFrame(pairs)

combat_data = create_pairs(data)

# Séparation des données en ensembles d'entraînement et de test
X = combat_data[['athlete1_placement', 'athlete2_placement']]
y = combat_data['winner']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisation et entraînement du modèle de régression logistique
model = LogisticRegression()
model.fit(X_train, y_train)

# Fonction pour prédire le gagnant entre deux athlètes
def predict_winner(athlete1_name, athlete2_name):
    athlete1_placement = find_placement(athlete1_name)
    athlete2_placement = find_placement(athlete2_name)
    
    if athlete1_placement is None or athlete2_placement is None:
        print("Les placements des athlètes ne sont pas disponibles.")
        return
    
    prediction = model.predict([[athlete1_placement, athlete2_placement]])
    if prediction == 1:
        print(f"{athlete1_name} va sûrement gagner contre {athlete2_name}")
    else:
        print(f"{athlete2_name} va sûrement gagner contre {athlete1_name}")

# Exemple d'utilisation
predict_winner("RINER Teddy", "GRANDA Andy")

