import pandas as pd
import ast


def turn_historique_combat_to_list(nom_athlete):#extrait la donnée du csv des combats de nom_athlete et le convertit en liste
    df = pd.read_csv('merged_file.csv', encoding='utf-8')
    athlete_row = df[df['Nom Prenom'] == nom_athlete]

    # Vérifier si l'athlète a été trouvé
    if not athlete_row.empty:
        historique_combat = athlete_row.iloc[0]['historique_combat']
        combats=ast.literal_eval(historique_combat)
 
    else:
        print(f"Aucun athlète trouvé avec le nom {nom_athlete}")
        combats = [["None","None","None"]]

    return combats
#PISTES DE FONCTIONS POUR APPORTER DES DONNEES SUPLEMENTAIRES AVEC L'HISTORIQUE DES COMBATS
def winrate(athlete1,athlete2):#regarde les combats de athlete1 et cherche le nombre de ses victoires sur athlete2
    total_combat=0
    total_victoire=0
    combats=turn_historique_combat_to_list(athlete1)
    
    for combat in combats:
        
        if combat[0]==athlete2 or combat[1]== athlete2:
            print(f"{athlete1} vs {athlete2} : {combat}")
            total_combat+=1

        if (combat[0] == athlete1 and combat[1]==athlete2 and combat[2]==athlete1) or (combat[0]==athlete2 and combat[1]==athlete1 and combat[2]==athlete1):
            total_victoire+=1
        
    ratio = 100*(total_victoire/total_combat)
    return ratio,total_combat,total_victoire


def best_3_ratio(categorie,fichier): #fonction qui prend une catégorie et sors les 3 meilleurs ratio de victoires
    ratio_cate=[]
    best_3_ratios=[]
    df = pd.read_csv(fichier,encoding='utf-8')
    df2 = df[df['Catégorie']== categorie]
    
    for nom_prenom in df2["Nom Prenom"]:
        victoire = 0
        combats=turn_historique_combat_to_list(nom_prenom)
        matchs=len(combats)

        for combat in combats:
            if combat[2] == nom_prenom:
                victoire+=1

        tuples=(nom_prenom,100*(victoire/matchs))
        ratio_cate.append(tuples)
        
    sorted_tuples= sorted(ratio_cate,key=lambda x: x[1],reverse=True)
    best_3_ratios.extend((sorted_tuples[0],sorted_tuples[1],sorted_tuples[2]))

    return best_3_ratios
#FONCTION QUI VA AJOUTER LE RATIO DE VICTOIRE EN DONNEE POUR LES ATHLETES
def Winratio(fichier):
    df=pd.read_csv(fichier,encoding='utf-8')
    win_ratios=[]
    for athlete in df["Nom Prenom"]:
        victoire = 0
        total_fights=0
        combats = turn_historique_combat_to_list(athlete)

        if combats is None:
            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Warning: No combat history found for athlete {athlete}")
            win_ratios.append(60)
            continue

        for combat in combats:
            if combat[2]==athlete:
                victoire+=1
                total_fights+=1
            else:
                total_fights+=1

        ratio = 100*victoire/total_fights
        win_ratios.append(ratio)
        print(athlete,ratio)
    df['WinRatio'] = win_ratios
    df.to_csv(fichier,index=False,encoding='utf-8')
        

Winratio("merged_file.csv")



print(winrate('TASOEV Inal','KIM Minjong'))
fichier = 'dataAthletes.csv'
print(best_3_ratio(-60,fichier))