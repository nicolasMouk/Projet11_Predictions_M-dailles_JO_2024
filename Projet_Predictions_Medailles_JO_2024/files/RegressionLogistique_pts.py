import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score

# Charger les données depuis un fichier CSV
data = pd.read_csv('/Users/bodeloison/Documents/projet JO/csv/+100.csv')

# Transformation pour créer des paires de combats
def create_pairs(data):
    pairs = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            athlete1 = data.iloc[i]
            athlete2 = data.iloc[j]
            pairs.append({
                'athlete1_points': athlete1['Points'],
                'athlete2_points': athlete2['Points'],
                'winner': 1 if athlete1['Points'] > athlete2['Points'] else 0
            })
            pairs.append({
                'athlete1_points': athlete2['Points'],
                'athlete2_points': athlete1['Points'],
                'winner': 1 if athlete2['Points'] > athlete1['Points'] else 0
            })
    return pd.DataFrame(pairs)

# Créer les paires de combats
combat_data = create_pairs(data)

# Séparation des données en ensembles d'entraînement et de test
X = combat_data[['athlete1_points', 'athlete2_points']]
y = combat_data['winner']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisation et entraînement du modèle de régression logistique
model = LogisticRegression()
model.fit(X_train, y_train)

# Prédiction sur l'ensemble de test
y_pred = model.predict(X_test)

# Calcul des métriques
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
print(f"Exactitude : {accuracy}")
print(f"Précision : {precision}")

# Validation croisée pour évaluer la performance du modèle
cv_scores = cross_val_score(model, X, y, cv=5)
print(f"Scores de validation croisée : {cv_scores}")
print(f"Moyenne des scores de validation croisée : {cv_scores.mean()}")

# Fonction pour prédire le gagnant entre deux athlètes
def predict_winner(athlete1_name, athlete2_name):
    athlete1 = data[data['Nom Prenom'] == athlete1_name]
    athlete2 = data[data['Nom Prenom'] == athlete2_name]
    
    if athlete1.empty or athlete2.empty:
        print("Athlète non trouvé dans les données.")
        return

    athlete1_points = athlete1['Points'].values[0]
    athlete2_points = athlete2['Points'].values[0]
    
    prediction = model.predict(pd.DataFrame([[athlete1_points, athlete2_points]], columns=['athlete1_points', 'athlete2_points']))
    probability = model.predict_proba(pd.DataFrame([[athlete1_points, athlete2_points]], columns=['athlete1_points', 'athlete2_points']))[0]
    
    if prediction == 1:
        print(f"{athlete1_name} a {probability[1] * 100:.2f}% de chances de gagner contre {athlete2_name}")
    else:
        print(f"{athlete2_name} a {probability[0] * 100:.2f}% de chances de gagner contre {athlete1_name}")

# Exemple d'utilisation de la fonction predict_winner
predict_winner("RINER Teddy", "GRANDA Andy")
