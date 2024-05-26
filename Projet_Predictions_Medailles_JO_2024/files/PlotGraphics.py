import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
df = pd.read_csv('dataJudoka.csv')
features = df.drop(['Nom Prenom', 'Genre', 'Pays', 'Statut', 'historique_combat'], axis=1)
X = features
y = df['average placement']

# Normalisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Entraînement du modèle
gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)

# Sauvegarde du modèle
joblib.dump(gb_model, 'trained_model_gb.pkl')

# Prédictions sur le jeu de test
y_pred = gb_model.predict(X_test)

# Création des graphiques
# 1. Graphique des prédictions par rapport aux valeurs réelles
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, edgecolors=(0, 0, 0))
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
plt.xlabel('Valeurs réelles')
plt.ylabel('Prédictions')
plt.title('Prédictions vs Valeurs réelles')
plt.show()

# 2. Graphique des distributions des erreurs de prédiction
errors = y_test - y_pred
plt.figure(figsize=(10, 6))
sns.histplot(errors, bins=30, kde=True)
plt.xlabel('Erreur de prédiction')
plt.ylabel('Fréquence')
plt.title('Distribution des erreurs de prédiction')
plt.show()

# Fonction de prédiction et affichage du podium
def predict_podium(df_file, category):
    df = pd.read_csv(df_file)
    model = joblib.load('trained_model_gb.pkl')
    filtered_df = df[df['Catégorie'] == category]
    features = filtered_df.drop(['Nom Prenom', 'Genre', 'Pays', 'Statut', 'historique_combat'], axis=1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    predictions = model.predict(X_scaled)
    filtered_df['predictions'] = predictions
    sorted_df = filtered_df.sort_values(by='predictions')
    print(f"Podium pour la catégorie {category}")
    print(sorted_df[['Nom Prenom', 'predictions', 'average placement']].head(3))

# Appel de la fonction de prédiction
predict_podium('dataJudoka.csv', 100)
