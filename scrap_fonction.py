import csv
from bs4 import BeautifulSoup
import re
import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Constantes ---

# Facteur de conversion de devise (par exemple, USD vers CAD)
CURRENCY_CONVERSION_FACTOR = 1.3 

# Lettres pour générer un VIN aléatoire
LETTERS = string.ascii_uppercase  

# --- Fonction principale ---


def scrape(driver):
    
# Attendre que la page soit complètement chargée
    wait = WebDriverWait(driver, 10)  # Attendre jusqu'à 10 secondes
# Attendre que le tag 'body' soit présent :
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    print(f"La page {driver.current_url} a complètement chargé.")

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    
            # --- Extraction des informations sur les pièces ---

            # Boucle sur les pièces de la catégorie
    for part in soup.select(".partlistrow"):

                # Extraction du prix de la pièce
                if part.find('span', attrs={'class':'sellprice'}) is None:
                    if part.find('span', attrs={'class':'dbl'}) is None:
                        price = "0.00"
                    else:
                        price = part.find('span', attrs={'class':'dbl'}).text.replace(',', '')
                else:
                    price = part.find('span', attrs={'class':'sellprice'}).text.replace(',', '')

                # Nettoyage et conversion du prix
                price = re.sub(r'(\$)', '',price)
                price = float(price) * CURRENCY_CONVERSION_FACTOR
                price = format(price, '.2f')


                # Extraction de la quantité de la pièce
                partsqty_element = part.find('div', attrs={'class':'c3'})
                if partsqty_element is not None:
                    partsqty = partsqty_element.find('input').get('value')
                    try:
                        partsqty = int(partsqty)  # Convertir en entier si possible
                        if partsqty < 1:
                            partsqty = 1  # Définir au minimum à 1
                    except (ValueError, TypeError):  # Gérer les erreurs de conversion
                        partsqty = 1       # Définir à 1 si la conversion échoue
                else:
                    partsqty = 1




                # Extraction du nom de la pièce
                
                parts_name_element = part.find('div', attrs={'class': 'c1a'}).find("span") 
                parts_name_element_2 = part.find('span', {"class":"itemnumnew"})
                if parts_name_element:
                    if parts_name_element_2:  # contole si l'élément complémentaire existe
                        parts_name = "(New ref. " + parts_name_element_2.text.strip() + ") " + parts_name_element.text.strip()
                    else:
                        parts_name = parts_name_element.text.strip()  # si l'éément complémentaire est NONE


                    parts_name = re.sub(r"(\sInc?ludes.*|Was\s\d+\s|\s\[.*\])", '', parts_name) # Cette regex va chercher et supprimer :
                    #Les parties de la chaîne qui commencent par "Includes" ou "Include" et qui sont suivies de n'importe quoi.
                    # Les parties de la chaîne qui commencent par "Was", suivi d'un nombre et d'un espace.
                    # Les parties de la chaîne qui sont entourées de crochets.

                    if "Not Available" in parts_name:
                        parts_name = "N/A"
                else:
                    parts_name = "N/A"

                    # Affiche les informations sur la pièce pour le débogage
                    print(parts_name + ' -REF '+ parts_reference + ' -PX ' + price + ' -QTY : ' + str(partsqty))



                # Extraction du reference de la pièce

                parts_reference_element = part.find('span', {"class":["itemnumstrike", "itemnum"]})
                if parts_reference_element:
                        parts_reference = parts_reference_element.text.strip()
                        if parts_reference == "TBA" or parts_reference == "NLA" or parts_reference == "UNA-VAILA-BL-EI" or parts_reference == "XXXX" or parts_reference == "XXX" or parts_reference == "-------": # certaine pieces on XXXX quand la ref n'existe pas 
                            parts_reference = "N/A"
                    
                else:
                    parts_reference = "N/A"


                # Affiche les informations sur la pièce pour le débogage
                print(parts_name + ' -REF '+ parts_reference + ' -PX ' + price + ' -QTY : ' + str(partsqty))

    pause_execution() # Appelle la fonction pour mettre en pause l'exécution



def pause_execution():
    """Met en pause l'exécution du script jusqu'à ce que l'utilisateur appuie sur Entrée."""
    input("Appuyez sur Entrée pour continuer...")