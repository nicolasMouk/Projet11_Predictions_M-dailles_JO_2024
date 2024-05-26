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
import pandas as pd

#set up
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.ijf.org/wrl_olympic?category=14") 

#nnoms=["MOSAKHLISHVILI Tristani","USTOPIRIYON Komronshokh","MATHIEU Alexis"]
xpath_expression = ["//td[normalize-space(text())='-100']","//td[normalize-space(text())='-90']","//td[normalize-space(text())='-81']","//td[normalize-space(text())='-73']","//td[normalize-space(text())='-66']","//td[normalize-space(text())='-60']","//td[normalize-space(text())='-48']","//td[normalize-space(text())='-52']","//td[normalize-space(text())='-57']","//td[normalize-space(text())='-63']","//td[normalize-space(text())='-70']","//td[normalize-space(text())='-78']","//td[normalize-space(text())='+78']"]
fichiers=["-60.csv","+100.csv","-100.csv","-90.csv","-81.csv","-73.csv","-66.csv","-48.csv","-52.csv","-57.csv","-63.csv","-70.csv","-78.csv","+78.csv"]
drivers=["https://www.ijf.org/wrl_olympic?category=3","https://www.ijf.org/wrl_olympic?category=4","https://www.ijf.org/wrl_olympic?category=5","https://www.ijf.org/wrl_olympic?category=6"]
def importer_csv(nom_fichier):
    liste_elements = []
    with open(nom_fichier, newline='',encoding='latin1') as csvfile:
        lecteur_csv = csv.reader(csvfile)
        for ligne in lecteur_csv:
            liste_elements.append(ligne[0])
    liste_elements.pop(0)

    return liste_elements

def get_oponents_name():#Fonction qui donne le noms des combatants pour un match
    versus_name=[]
    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".contest-tile.contest-tile--is-not-selected.contest-tile--has-media")))
    contest_tiles = driver.find_elements(By.CSS_SELECTOR, ".contest-tile.contest-tile--is-not-selected.contest-tile--has-media")
    
    for contest_tile in contest_tiles:
        athletes_divs = contest_tile.find_elements(By.CLASS_NAME, "athlete")
        noms_versus = []
        for athlete_div in athletes_divs:
            judoka_info_div = athlete_div.find_element(By.CLASS_NAME, "judoka-info")          
            family_name = judoka_info_div.find_element(By.CLASS_NAME, "family-name").text
            given_name = judoka_info_div.find_element(By.CLASS_NAME, "given-name").text
            nom_prenom = f"{family_name} {given_name}"
            noms_versus.append(nom_prenom)
            
        versus_name.append(noms_versus)

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.contest-tile.contest-tile--is-not-selected')))
    contest_tiles2 = driver.find_elements(By.CSS_SELECTOR, '.contest-tile.contest-tile--is-not-selected')

    for contest_tile in contest_tiles2:
        athletes_divs = contest_tile.find_elements(By.CLASS_NAME, "athlete")
        noms_versus = []
        for athlete_div in athletes_divs:
            judoka_info_div = athlete_div.find_element(By.CLASS_NAME, "judoka-info")          
            family_name = judoka_info_div.find_element(By.CLASS_NAME, "family-name").text
            given_name = judoka_info_div.find_element(By.CLASS_NAME, "given-name").text
            nom_prenom = f"{family_name} {given_name}"
            noms_versus.append(nom_prenom)
            
        versus_name.append(noms_versus)


    return versus_name

def get_winner_name(): #Fonction qui donne le nom du gagnant

    wait = WebDriverWait(driver, 60)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".contest-tile.contest-tile--is-not-selected.contest-tile--has-media")))
    contest_tiles = driver.find_elements(By.CSS_SELECTOR, ".contest-tile.contest-tile--is-not-selected.contest-tile--has-media")

    match_winner=[]

    for contest_tile in contest_tiles:   
        winner_divs = contest_tile.find_elements(By.CLASS_NAME,"is-winner") 
        for winner_div in winner_divs:
                judoka_info_div = winner_div.find_element(By.XPATH, "../../..")
                side_div = judoka_info_div.find_element(By.XPATH, ".//*[contains(@class, 'side')]")
                winner_family_name = side_div.find_element(By.CLASS_NAME, "family-name").text
                winner_given_name = side_div.find_element(By.CLASS_NAME, "given-name").text 
                vainqueur = f"{winner_family_name} {winner_given_name}"
                match_winner.append(vainqueur)

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.contest-tile.contest-tile--is-not-selected')))
    contest_tiles2 = driver.find_elements(By.CSS_SELECTOR, '.contest-tile.contest-tile--is-not-selected')


    for contest_tile in contest_tiles2:   
        winner_divs = contest_tile.find_elements(By.CLASS_NAME,"is-winner") 
        for winner_div in winner_divs:
                judoka_info_div = winner_div.find_element(By.XPATH, "../../..")
                side_div = judoka_info_div.find_element(By.XPATH, ".//*[contains(@class, 'side')]")
                winner_family_name = side_div.find_element(By.CLASS_NAME, "family-name").text
                winner_given_name = side_div.find_element(By.CLASS_NAME, "given-name").text 
                vainqueur = f"{winner_family_name} {winner_given_name}"
                match_winner.append(vainqueur)
                
    return match_winner      

def blue_vs_white_who_won(nom_athlete):
    # Attendre que les éléments se chargent (ajuster le temps d'attente selon la vitesse de chargement de la page)
    wait = WebDriverWait(driver, 60)
    wait.until_not(EC.visibility_of_element_located((By.ID, "CybotCookiebotDialogFooter")))  #Attendre que l'élément cookie soit caché ou retiré de la page
    element_athlete = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[@class='name']/a[text()='{nom_athlete}']")))
    element_athlete.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='filter-items']/a[contains(text(),'Contests')]")))# Attendre que les éléments se chargent sur la nouvelle page
    element_results = driver.find_element(By.XPATH, "//div[@class='filter-items']/a[contains(text(),'Contests')]")
    element_results.click()

    versus=get_oponents_name()
    vainqueurs= get_winner_name()
    
    c=0
    for i in versus:
         if c < len(vainqueurs):
            i.append(vainqueurs[c]) 
            c+=1
         else:
            print(f"Pas autant d'éléments dans les listes winner et versus, on mets un unknown")
            i.append("Unknown")
    #print(versus) 

    driver.back() 
    driver.back()
    return versus 

def resultats_combats(combats, nom_combattant, nom_fichier):
    fichier_exists = os.path.isfile(nom_fichier)
    with open(nom_fichier, 'a', newline='',encoding='latin1') as csvfile:
        writer = csv.writer(csvfile)
        if not fichier_exists:
            writer.writerow(['Nom Judoka', 'Resultats_combats'])
        writer.writerow([nom_combattant, combats])




noms=importer_csv("+78.csv")
print(noms)

for nom in noms:
    dataCombats=blue_vs_white_who_won(nom)
    resultats_combats(dataCombats,nom,'dataCombat.csv')
    print(f"dataCombats append dans dataCombat pour le judoka: {nom}")

#resultats_combats(blue_vs_white_who_won("VAN T END Noel"),"VAN T END Noel",'-90.csv')
    
time.sleep(5) 
driver.quit()