import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Charger les données depuis un fichier CSV
data = pd.read_csv('/Users/bodeloison/Documents/projet JO/csv/+100.csv')

# Sélectionner les caractéristiques et la variable cible
X = data[['Points', 'Age', 'Medailles d\'Or Olympiques']]  # Sélectionnez les caractéristiques pertinentes
y = data['Medailles d\'Or ALL']  # Sélectionnez la variable cible

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialiser et entraîner le modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# Fonction pour prédire le résultat des combats entre deux athlètes
def predict_combat(athlete1_name, athlete2_name):
    athlete1_data = data[data['Nom Prenom'] == athlete1_name][['Points', 'Age', 'Medailles d\'Or Olympiques']].values
    athlete2_data = data[data['Nom Prenom'] == athlete2_name][['Points', 'Age', 'Medailles d\'Or Olympiques']].values
    
    if len(athlete1_data) == 0 or len(athlete2_data) == 0:
        print("Athlète non trouvé dans les données.")
        return
    
    athlete1_score = model.predict(athlete1_data)[0]
    athlete2_score = model.predict(athlete2_data)[0]
    
    if athlete1_score > athlete2_score:
        print(f"{athlete1_name} va sûrement gagner contre {athlete2_name}")
    elif athlete1_score < athlete2_score:
        print(f"{athlete2_name} va sûrement gagner contre {athlete1_name}")
    else:
        print("Les deux athlètes ont des chances égales de gagner")

# Exemple d'utilisation
predict_combat("RINER Teddy", "GRANDA Andy")


