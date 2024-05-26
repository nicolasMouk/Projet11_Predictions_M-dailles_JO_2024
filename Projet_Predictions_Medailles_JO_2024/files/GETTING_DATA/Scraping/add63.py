from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import csv
import os

qualifieList78More=[]
qualifieList63=[]

#set up
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

def extract_info_and_append_v3(qualifie_list):#fonction d'ajout la plus au point pour l'instant

    for element in elements:
        athlete_info = []
        try:
            text = element.text
            segments = text.split(" ")
                
            if len(segments)==5:#Pattern (nom[1 mot] prenom[1 mot] , pays[1 mot])
                nom_prenom=segments[0].split('\n')[1] + " " + segments[1].split('\n')[0]
                pays=segments[1].split('\n')[1]
                points=int(segments[2])
                status = "Qualified"
                more_data=access_to_more_data(nom_prenom)
                athlete_info.extend([nom_prenom, pays, points, status,more_data[0],more_data[1],more_data[2],more_data[3],more_data[4],more_data[5],more_data[6],more_data[7],more_data[8],more_data[9]])
                qualifie_list.append(athlete_info) 
                ecrire_donnees_comp("donnees_comp.csv",more_data[10])

            elif len(segments)==7:
                if '\n' in segments[1]: #Pattern (nom[1 mot] prenom[1 mot] , pays[3 mot])
                    nom_prenom = segments[0].split('\n')[1] + " " + segments[1].split('\n')[0]
                    pays = segments[1].split('\n')[1] + " " + segments[2] + " " + segments[3]

                elif '\n' in segments[2]:#pattern (nom[2 mots] prenom[1mot] pays[2mots])
                    nom_prenom = segments[0].split('\n')[1]+' '+segments[1]+" "+segments[2].split('\n')[0]
                    pays = segments[2].split('\n')[1] +' ' +segments[3]

                elif '\n' in segments[3]: # pattern (nom[2 mots] prenom[2 mots] pays[1 mot])
                    nom_prenom=segments[0].split('\n')[1] +' '+segments[1]+' '+segments[2]+' '+segments[3].split('\n')[0]
                    pays=segments[3].split('\n')[1]
                    
                points = int(segments[4])
                status = "Qualified"
                more_data=access_to_more_data(nom_prenom)
                athlete_info.extend([nom_prenom, pays, points, status,more_data[0],more_data[1],more_data[2],more_data[3],more_data[4],more_data[5],more_data[6],more_data[7],more_data[8],more_data[9]])
                qualifie_list.append(athlete_info)
                ecrire_donnees_comp("donnees_comp.csv",more_data[10])
            
            elif len(segments)==6:#Plusieurs paterns de segments on la longueure 6

                if '\n' in segments[1]: #Patern nom[1 mot] Prenom[1 mot] pays[2 mots]
                    nom_prenom=segments[0].split('\n')[1] + " " + segments[1].split('\n')[0]
                    pays = segments[1].split('\n')[1]+' '+segments[2]

                
                else:#Patern nom[2 mot] Prenom[1 mot] pays[1 mots]
                    nom_prenom = segments[0].split('\n')[1] + " " + segments[1] + " " + segments[2].split('\n')[0]
                    pays = segments[2].split('\n')[1]
                points = int(segments[3])
                status = "Qualified"
                more_data=access_to_more_data(nom_prenom)
                athlete_info.extend([nom_prenom, pays, points, status,more_data[0],more_data[1],more_data[2],more_data[3],more_data[4],more_data[5],more_data[6],more_data[7],more_data[8],more_data[9]])
                qualifie_list.append(athlete_info)
                ecrire_donnees_comp("donnees_comp.csv",more_data[10])

            elif len(segments)==8:
                if '\n' in segments[1]:#pattern (nom[1 mot] prenom[1 mot] pays[4mots])
                    nom_prenom=segments[0].split('\n')[1]+ ' '+ segments[1].split('\n')[0]
                    pays=segments[1].split('\n')[1]+' '+ segments[2] +' '+ segments[3] +' '+segments[4]
                    
                elif '\n' in segments[2]: #Patterne nom[1mot] prenom[2 mots] pays [3 mots]
                    nom_prenom=segments[0].split('\n')[1]+' '+segments[1]+' '+segments[2].split('\n')[0]
                    pays=segments[2].split('\n')[1]+' '+segments[3]+' '+segments[4]
                
                points=segments[5]
                status="Qualified"
                more_data=access_to_more_data(nom_prenom)
                athlete_info.extend([nom_prenom, pays, points, status,more_data[0],more_data[1],more_data[2],more_data[3],more_data[4],more_data[5],more_data[6],more_data[7],more_data[8],more_data[9]])
                qualifie_list.append(athlete_info)
                ecrire_donnees_comp("donnees_comp.csv",more_data[10])

            elif len(segments)==9:#patern nom [1 mot] prenom[2 mot] pays [4 mots]
                nom_prenom = segments[0].split('\n')[1]+' '+segments[1]+' '+segments[2].split('\n')[0]
                pays = segments[2].split('\n')[1]+' '+segments[3]+' '+segments[4]+' '+segments[5]
                points= segments[6]
                status="Qualified"
                more_data=access_to_more_data(nom_prenom)
                athlete_info.extend([nom_prenom, pays, points, status,more_data[0],more_data[1],more_data[2],more_data[3],more_data[4],more_data[5],more_data[6],more_data[7],more_data[8],more_data[9]])
                qualifie_list.append(athlete_info)
                ecrire_donnees_comp("donnees_comp.csv",more_data[10])

        except StaleElementReferenceException:
            pass

def extract_append_host_nation(qualifie_list):#fonction qui rajoute le séléctionner français 
     hostAthlete=[]
     for element in elements:
        athlete_info = []
        text = element.text
        segments = text.split(" ")

        if len(segments)==6:# prenom 1 mot et nom 1 mot
            if '\n' in segments[1]:
                nom_prenom=segments[0].split('\n')[1] + " " + segments[1].split('\n')[0]
                pays=segments[1].split('\n')[1]

            elif '\n' in segments[2]:#prenom 2 mot et nom 1 mot
                nom_prenom=segments[0].split('\n')[1] + " " + segments[1] + " " +segments[2].split('\n')[0]
                pays=segments[2].split('\n')[1]
            points=int(segments[2])
            status = "Qualified"
            more_data=access_to_more_data(nom_prenom)
            athlete_info.extend([nom_prenom, pays, points, status,more_data[0],more_data[1],more_data[2],more_data[3],more_data[4],more_data[5],more_data[6],more_data[7],more_data[8],more_data[9]])
            hostAthlete.append(athlete_info)
            ecrire_donnees_comp("donnees_comp.csv",more_data[10])
       
     qualifie_list.append(hostAthlete[0])
     hostAthlete=[]


def ecrire_donnees_comp(nom_fichier,donnees):
    # Vérifier si le fichier existe
    fichier_existe = os.path.exists(nom_fichier)

    # Ouvrir le fichier CSV en mode ajout (ajoutera s'il existe, créera sinon)
    with open(nom_fichier, 'a', newline='', encoding='utf-8') as fichier_csv:
        # Créer un objet writer seulement si le fichier vient d'être créé
        if not fichier_existe:
            writer = csv.writer(fichier_csv)
            # Ajouter une entête si le fichier vient d'être créé
            entete = ["Date", "Competition", "Placement", "Athlete"]
            writer.writerow(entete)
        else:
            writer = csv.writer(fichier_csv)
        # Ajouter les données à la fin du fichier
        writer.writerow(donnees)
    print(f"Les données des compétition on été ajouter dans '{nom_fichier}' avec succès.")

def access_to_more_data(nom_athlete):
    
    # Attendre que les éléments se chargent (ajuster le temps d'attente selon la vitesse de chargement de la page)
    wait = WebDriverWait(driver, 60)

    # Attendre que l'élément cookie soit caché ou retiré de la page
    wait.until_not(EC.visibility_of_element_located((By.ID, "CybotCookiebotDialogFooter")))

    element_athlete = wait.until(EC.presence_of_element_located((By.XPATH, f"//td[@class='name']/a[text()='{nom_athlete}']")))
    element_athlete.click()
   
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='filter-items']/a[contains(text(),'Results')]")))# Attendre que les éléments se chargent sur la nouvelle page
    # Trouver le lien "Results" dans la div de classe "filter-items" cela permat d'accéder aux informations croustillantes pour le machine learning
    element_results = driver.find_element(By.XPATH, "//div[@class='filter-items']/a[contains(text(),'Results')]")
    element_results.click()
    
    #RECUPERATION AGE
    selected_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "selected")))
    try:
        age_element = selected_element.find_element(By.XPATH, "//div[@class='age-info']")# Trouver l'élément <div> avec la classe "age-info"
        age_text = age_element.text # Récupérer le texte de l'élément
        age_number = int(age_text.split(":")[1].split()[0]) #traitement pour chopper le chiffre de l'age
    except NoSuchElementException:
        age_number=0

    #Récupération MEDAILLES le but est de récupérer pour jeux olympiques, worlds et total

    #initié les variables à 0 et les mettre à jour si on détècte une présence ensuite
    all_gold_olympics = all_silver_olympics = all_bronze_olympics = all_gold_worlds = all_silver_worlds = all_bronze_worlds = all_gold_medals = all_silver_medals = all_bronze_medals = 0
    table=driver.find_element(By.XPATH,"//table[contains(@class, 'table--athlete_results')]") #TABLE CONTENANT LE BODY (qui a nos infos)
    body = table.find_element(By.XPATH, "./tbody")# Trouver le body qui est un descendant de la table
    rows = body.find_elements(By.TAG_NAME, "tr") # Trouver toutes les lignes dans le body

    #ceci récupère toutes les balise td concernant les info des médailles
    for row in rows:
        elems=row.find_elements(By.TAG_NAME,"td")
        content_row=[cell.text for cell in elems]

        if  "Olympic Games" in content_row:
            all_gold_olympics= int(content_row[1]) #récupération médailles or olympics
            all_silver_olympics=int(content_row[2])
            all_bronze_olympics=int(content_row[3])

        elif "World Championships" in content_row:
            all_gold_worlds= int(content_row[1]) #récupération médailles or worlds
            all_silver_worlds=int(content_row[2])
            all_bronze_worlds=int(content_row[3])
        else:
            pass

    #récupérer le palmares de toutes les médailles en dernière ligne à chaque fois
    elem_last_row= rows[-1].find_elements(By.TAG_NAME,"td")
    content_last_row= [cell.text for cell in elem_last_row]
    all_gold_medals=int(content_last_row[1])
    all_silver_medals=int(content_last_row[2])
    all_bronze_medals=int(content_last_row[3])

    #Récupérer les résultats des dernières comp
    #et créer un csv avec le nom de l'athlète en 1er dans les listes
    result_comp=[] #liste de listes au format ["nom","date","nom","placement"]
   # div_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "athlete-title-hero")))
    #nom_prenom = driver.execute_script("return arguments[0].firstChild.textContent.trim()", div_name)
    body_comp=driver.find_element(By.XPATH, "//table[contains(@class, 'table') and not(contains(@class, 'table--athlete_results'))]/tbody")
    rows_in_body =body_comp.find_elements(By.TAG_NAME, "tr")

    for row in rows_in_body:
        elems=row.find_elements(By.TAG_NAME,"td")
        content_row=[cell.text for cell in elems]      
        content_row.append(nom_athlete)
        print(content_row)
        result_comp.append(content_row)

    #retour sur les autres pages (2 en arrière)
    driver.back() 
    driver.back()
    more_data=[age_number,all_gold_olympics,all_silver_olympics,all_bronze_olympics,all_gold_worlds,all_silver_worlds,all_bronze_worlds,all_gold_medals,all_silver_medals,all_bronze_medals,result_comp] 
    return more_data

def ecrire_donnees_csv(donnees, nom_fichier):
    chemin_fichier = os.path.join(os.getcwd(), nom_fichier)  # Chemin vers le fichier CSV
    # Création du fichier CSV et écriture des données
    with open(chemin_fichier, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        # Écriture de l'en-tête
        writer.writerow(["Nom Prenom", "Pays", "Points", "Statut","Age","Medailles d'Or Olympiques","Medailles d'Argent Olympiques","Medailles de Bronze Olympiques","Medailles d'Or Worlds","Medailles d'Argent Worlds","Medailles de Bronze Worlds","Medailles d'Or ALL","Medailles d'Argent ALL","Medailles de Bronze ALL"])
        writer.writerows(donnees)# Écriture des données

    print(f"Les données ont été écrites dans le fichier CSV '{nom_fichier}' avec succès.")


#pour le stockage des données

#partie du site à scrapper
driver.get("https://www.ijf.org/wrl_olympic?category=11") 

elements=WebDriverWait(driver,10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME,"qualified"))
)
extract_info_and_append_v3(qualifieList63)

#ajout des semis qualifiés
elements=WebDriverWait(driver,10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME,"semi-qualified"))
)
extract_info_and_append_v3(qualifieList63)

#ajout de l'athlète français
elements=WebDriverWait(driver,10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME,"host-nation"))
)
extract_append_host_nation(qualifieList63)
ecrire_donnees_csv(qualifieList63,"-63.csv")


time.sleep(5)
driver.quit()
