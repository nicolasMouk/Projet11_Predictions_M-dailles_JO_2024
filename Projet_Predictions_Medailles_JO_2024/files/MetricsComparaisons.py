import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, make_scorer, mean_absolute_percentage_error, explained_variance_score, median_absolute_error
import numpy as np

df = pd.read_csv('dataJudoka.csv')
# Supprimer les colonnes non pertinentes pour l'entraînement du modèle
features = df.drop(['Nom Prenom','Catégorie' ,'Genre', 'Pays', 'Statut', 'historique_combat'], axis=1)

# Diviser les données en variables prédictives et cible
X = features
y = df['average placement']#Variable cible

# Normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


# Définir les métriques pour la validation croisée
scoring = {
    'MAE': make_scorer(mean_absolute_error),
    'RMSE': make_scorer(mean_squared_error, squared=False),
    'R2': make_scorer(r2_score),
    'MAPE': make_scorer(mean_absolute_percentage_error),
    'EVS': make_scorer(explained_variance_score),
    'MedAE': make_scorer(median_absolute_error)
}

# Initialiser les modèles
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
gbr_model = GradientBoostingRegressor(n_estimators=100, random_state=42)

# Effectuer la validation croisée pour le modèle RandomForestRegressor
rf_cv_results = cross_validate(rf_model, X_scaled, y, cv=5, scoring=scoring)
print("RandomForestRegressor - Cross-Validation Metrics:")
print(f"MAE: {np.mean(rf_cv_results['test_MAE'])}")
print(f"RMSE: {np.mean(rf_cv_results['test_RMSE'])}")
print(f"R^2: {np.mean(rf_cv_results['test_R2'])}")
print(f"MAPE: {np.mean(rf_cv_results['test_MAPE'])}")
print(f"EVS: {np.mean(rf_cv_results['test_EVS'])}")
print(f"MedAE: {np.mean(rf_cv_results['test_MedAE'])}")
print('')
print('cross valisation:', rf_cv_results)
# Effectuer la validation croisée pour le modèle Gradient Boosting Regressor
gbr_cv_results = cross_validate(gbr_model, X_scaled, y, cv=5, scoring=scoring)
print("\nGradient Boosting Regressor - Cross-Validation Metrics:")
print(f"MAE: {np.mean(gbr_cv_results['test_MAE'])}")
print(f"RMSE: {np.mean(gbr_cv_results['test_RMSE'])}")
print(f"R^2: {np.mean(gbr_cv_results['test_R2'])}")
print(f"MAPE: {np.mean(gbr_cv_results['test_MAPE'])}")
print(f"EVS: {np.mean(gbr_cv_results['test_EVS'])}")
print(f"MedAE: {np.mean(gbr_cv_results['test_MedAE'])}")
print('')
print('cross valisation:', gbr_cv_results)
