import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, make_scorer, mean_absolute_percentage_error, explained_variance_score, median_absolute_error
import numpy as np
import joblib

df=pd.read_csv('dataJudoka.csv')
features = df.drop(['Nom Prenom', 'Genre', 'Pays', 'Statut', 'historique_combat'], axis=1)
#identification variable cible et fetures
X=features
y=df['average placement']


# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#NORMALISATION
scaler= StandardScaler()
X_train_scaled= scaler.fit_transform(X_train)
X_tested_scaled = scaler.transform(X_test)


gb_model = GradientBoostingRegressor(n_estimators=100,random_state=42)
gb_model.fit(X_train_scaled,y_train)


joblib.dump(gb_model,'trained_model.pkl')

def predict_podium(df_file,category):
    df = pd.read_csv(df_file)
    model = joblib.load('trained_model.pkl')

    filtered_df = df[df['Catégorie'] == category]

    features = filtered_df.drop(['Nom Prenom', 'Genre', 'Pays', 'Statut', 'historique_combat'], axis=1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    predictions = model.predict(X_scaled)

    filtered_df['predictions'] = predictions
    sorted_df= filtered_df.sort_values(by='predictions',ascending=True)
    sorted_df.reset_index(drop=True, inplace=True)  # Réinitialiser l'index pour l'affichage
    sorted_df['place fictive'] = sorted_df.index + 1  # Ajouter une colonne de place fictive
    podium_df = sorted_df[['Nom Prenom','Pays', 'predictions', 'average placement', 'place fictive']].head(3)
    print(f"Podium pour la catégorie {category}:")
    print(podium_df)

predict_podium('dataJudoka.csv',100)