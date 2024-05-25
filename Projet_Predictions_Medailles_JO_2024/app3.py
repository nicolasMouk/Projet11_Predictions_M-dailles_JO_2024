from flask import Flask, render_template, request, redirect, url_for,jsonify
import csv
import ast
import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, make_scorer, mean_absolute_percentage_error, explained_variance_score, median_absolute_error
import numpy as np
import joblib
import os

#PARTIE ML GRADIENT BOOST
df=pd.read_csv('static/data/dataJudoka.csv')
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
#gradBoost
gb_model = GradientBoostingRegressor(n_estimators=100,random_state=42)
gb_model.fit(X_train_scaled,y_train)
joblib.dump(gb_model,'trained_model.pkl') #on save le model entrainé

#PARTIE FLASK et FONCTIONS

app = Flask(__name__, template_folder='templates',static_folder='static')

# Fonction pour lire les données du CSV
def lire_donnees_csv(nom_fichier):
    donnees = []
    with open(nom_fichier, 'r', encoding='utf-8') as fichier_csv:
        lecteur_csv = csv.DictReader(fichier_csv)
        for ligne in lecteur_csv:
            donnees.append(ligne)
    return donnees

def turn_historique_combat_to_list(nom_athlete):#extrait la donnée du csv des combats de nom_athlete et le convertit en liste
    df = pd.read_csv('static/data/dataJudoka.csv', encoding='utf-8')
    athlete_row = df[df['Nom Prenom'] == nom_athlete]

    # Vérifier si l'athlète a été trouvé
    if not athlete_row.empty:
        historique_combat = athlete_row.iloc[0]['historique_combat']
        combats=ast.literal_eval(historique_combat)
 
    else:
        print(f"Aucun athlète trouvé avec le nom {nom_athlete}")
        combats = [["None","None","None"]]

    return combats

def winrate(athlete1,athlete2):#regarde les combats de athlete1 et cherche le nombre de ses victoires sur athlete2
    total_combat=0
    total_victoire=0
    combats=turn_historique_combat_to_list(athlete1)

    if combats ==[["None","None","None"]]:
        return None
    
    for combat in combats:
        
        if combat[0]==athlete2 or combat[1]== athlete2:
            #print(f"{athlete1} vs {athlete2} : {combat}")
            total_combat+=1

        if (combat[0] == athlete1 and combat[1]==athlete2 and combat[2]==athlete1) or (combat[0]==athlete2 and combat[1]==athlete1 and combat[2]==athlete1):
            total_victoire+=1
        
    ratio = 100*(total_victoire/total_combat)
    return ratio


def predire_gagnant(athlete1, athlete2):

    df=pd.read_csv('static/data/dataJudoka.csv',encoding='utf-8')
    df1=df.loc[df['Nom Prenom']== athlete1]
    df2=df.loc[df['Nom Prenom']== athlete2]
    # Comparaison des attributs et attribution de scores
    score_athlete1 = 0
    score_athlete2 = 0

    win1 = winrate(athlete1,athlete2) 
    win2 = winrate(athlete2,athlete1)
    if win1 == None or win2 == None:
        score_athlete1+=0
        score_athlete2+=0

    if win1 > win2:
        score_athlete1 +=2
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if win1 < win2:
        score_athlete2 +=2
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if win1 == win2:
        pass
    if win1 == 0 and win2== 0: #pas d'afrontement enregistré
        pass
    # Comparaison des ratios de victoire globaux
    if df1["Age"].iloc[0] > df2["Age"].iloc[0]:
        score_athlete2 += 1
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Age"].iloc[0] < df2["Age"].iloc[0]:
        score_athlete1 += 1
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    # Comparaison des médailles remportées
    if df1["Medailles d'Or Olympiques"].iloc[0] > df2["Medailles d'Or Olympiques"].iloc[0]:
        score_athlete1 += 2.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles d'Or Olympiques"].iloc[0] < df2["Medailles d'Or Olympiques"].iloc[0]:
        score_athlete2 += 2.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles d'Or Worlds"].iloc[0] > df2["Medailles d'Or Worlds"].iloc[0]:
        score_athlete1 += 2.25
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles d'Or Worlds"].iloc[0] < df2["Medailles d'Or Worlds"].iloc[0]:
        score_athlete2 += 2.25
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles d'Or ALL"].iloc[0] > df2["Medailles d'Or ALL"].iloc[0]:
        score_athlete1 += 1
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles d'Or ALL"].iloc[0] < df2["Medailles d'Or ALL"].iloc[0]:
        score_athlete2 += 1
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles d'Argent Olympiques"].iloc[0] > df2["Medailles d'Argent Olympiques"].iloc[0]:
        score_athlete1 += 2
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles d'Argent Olympiques"].iloc[0] < df2["Medailles d'Argent Olympiques"].iloc[0]:
        score_athlete2 += 2
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles d'Argent Worlds"].iloc[0] > df2["Medailles d'Argent Worlds"].iloc[0]:
        score_athlete1 += 1.25
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles d'Argent Worlds"].iloc[0] < df2["Medailles d'Argent Worlds"].iloc[0]:
        score_athlete2 += 1.25
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles d'Argent ALL"].iloc[0] > df2["Medailles d'Argent ALL"].iloc[0]:
        score_athlete1 += 0.75
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles d'Argent ALL"].iloc[0] < df2["Medailles d'Argent ALL"].iloc[0]:
        score_athlete2 += 0.75
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles de Bronze Olympiques"].iloc[0] > df2["Medailles de Bronze Olympiques"].iloc[0]:
        score_athlete1 += 1.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles de Bronze Olympiques"].iloc[0] < df2["Medailles de Bronze Olympiques"].iloc[0]:
        score_athlete2 += 1.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles de Bronze Worlds"].iloc[0] > df2["Medailles de Bronze Worlds"].iloc[0]:
        score_athlete1 += 1
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles de Bronze Worlds"].iloc[0] < df2["Medailles de Bronze Worlds"].iloc[0]:
        score_athlete2 += 1
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    if df1["Medailles de Bronze ALL"].iloc[0] > df2["Medailles de Bronze ALL"].iloc[0]:
        score_athlete1 += 0.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["Medailles de Bronze ALL"].iloc[0] < df2["Medailles de Bronze ALL"].iloc[0]:
        score_athlete2 += 0.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    # Comparaison des ratios de victoire globaux
    if df1["WinRatio"].iloc[0] > df2["WinRatio"].iloc[0]:
        score_athlete1 += 2
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["WinRatio"].iloc[0] < df2["WinRatio"].iloc[0]:
        score_athlete2 += 2
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    # Comparaison des placements moyens en compétition
    if df1["average placement"].iloc[0] < df2["average placement"].iloc[0]:
        score_athlete1 += 2.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete1} prends des points")
    if df1["average placement"].iloc[0] > df2["average placement"].iloc[0]:
        score_athlete2 += 2.5
        print(f"score1 {score_athlete1}, score2 {score_athlete2}, {athlete2} prends des points")
    # Comparaison des scores globaux et prédiction du gagnant
    if score_athlete1 > score_athlete2:
        return athlete1
    elif score_athlete1 < score_athlete2:
        return athlete2
    else:
        return "Match nul"

# Route pour la page d'accueil
@app.route('/')
def accueil():
    categories_men = ['100', '-100', '-90', '-81', '-73', '-66', '-60']
    categories_women = ['+78', '-78', '-70', '-63', '-57', '-52', '-48']
    return render_template('accueil.html', categories_men=categories_men, categories_women=categories_women)


# Fonction pour prédire le podium
def predict_podium(category):
    df=pd.read_csv('static/data/dataJudoka.csv')
    model = joblib.load('trained_model.pkl') # Charger le modèle entraîné
    
    # Filtrer les données pour la catégorie sélectionnée
    filtered_df = df[df['Catégorie'] == category].copy()
    
    features = filtered_df.drop(['Nom Prenom', 'Genre', 'Pays', 'Statut', 'historique_combat'], axis=1)
    
    # Normaliser les données
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    predictions = model.predict(X_scaled)# Faire les prédictions
    
    # Ajouter les prédictions aux données filtrées
    filtered_df.loc[:, 'predictions'] = predictions
    sorted_df = filtered_df.sort_values(by='predictions', ascending=True)# Trier les données par prédictions ascendantes
    sorted_df.reset_index(drop=True, inplace=True) # Réinitialiser l'index pour l'affichage
    sorted_df['place fictive'] = sorted_df.index + 1 # Ajouter une colonne de place fictive sur le podium (1,2,3)
    podium_df = sorted_df[['Nom Prenom', 'Pays', 'predictions', 'place fictive']].head(3) # Extraire le podium
    
    return podium_df

# Route pour afficher les judokas d'une catégorie donnée
@app.route('/categorie/<categorie>')
def afficher_judokas_par_categorie(categorie):
    judokas_categorie = df[df['Catégorie'] == int(categorie)].to_dict(orient='records')
    
    # Trier les athlètes français en premier
    french_athletes = [athlete for athlete in judokas_categorie if athlete['Pays'] == 'France']
    other_athletes = [athlete for athlete in judokas_categorie if athlete['Pays'] != 'France']
    
    # Concaténer les listes d'athlètes
    judokas_categorie_sorted = french_athletes + other_athletes
    
    podium = predict_podium(int(categorie))
    return render_template('judokas_categorie.html', judokas=judokas_categorie_sorted, categorie=categorie, podium=podium.to_dict(orient='records'))

# Route pour gérer la prédiction de l'issue du combat
@app.route('/predict', methods=['POST'])
def predict():
    athlete1 = request.form.get('athlete1')
    athlete2 = request.form.get('athlete2')
    #category = request.json.get('category')
    winner = predire_gagnant(athlete1,athlete2)
    return jsonify(winner=winner)

if __name__ == '__main__':
    app.run(debug=True)