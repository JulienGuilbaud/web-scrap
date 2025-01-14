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

def fetch(soup, urlsite, brand, vehiculeName, vehiculeYear, driver):
    """
    Gratte les données d'un site web de pièces de moto CF Moto et génère des fichiers CSV pour les informations sur les produits et une nomenclature (BOM).

    Args:
        soup (BeautifulSoup): Un objet BeautifulSoup représentant le contenu HTML analysé du site web.
        urlsite (str): L'URL de base du site web.
        brand (str): La marque de la moto.
        vehiculeName (str): Le nom du véhicule.
        vehiculeYear (str): L'année du véhicule.
        driver (selenium.webdriver.Chrome): Une instance de pilote Selenium WebDriver utilisée pour interagir avec le navigateur.
    """

    # --- En-têtes des fichiers CSV ---

    # En-têtes pour le fichier CSV des produits
    PRODUCT_CSV_HEADERS = [
        'Name', 'Internal Reference', 'Brand', 'Can be Sold', 'Can be Purchased', 'Is Publish',
        'Product Category', 'Product Type', 'Sales Price', 'Detailed Price', 'Cost', 'Unit of Measure',
        'Customer Taxes', 'Vendor Taxes', 'Invoicing Policy', 'Control Policy', 'Routes', 'Tracking',
        'Variant Seller/Vendor', 'Variant Seller/Delivery Lead Time', 'Variant Seller/Quantity',
        'Variant Seller/Price', 'Description_en', 'Description_fr'
    ]

    # En-têtes pour le fichier CSV de la nomenclature (BOM)
    BOM_CSV_HEADERS = ['BoM Internal Reference', 'BoM Reference', 'BoM Lines/Internal Reference', 'BoM Lines/Quantity']

    # --- Génération d'un VIN aléatoire pour la référence interne ---

    # Génère un VIN aléatoire de 7 caractères
    CustomVIN = ''.join(random.choice(LETTERS) for i in range(7))

    # --- Ouverture des fichiers CSV pour l'écriture ---

    # Ouvre les fichiers CSV en mode écriture
    with open(vehiculeName + '.csv', 'w', encoding='UTF8', newline='') as f, \
            open('UnbluidOrder-' + vehiculeName + '.csv', 'w', encoding='UTF8', newline='') as fs:

        # --- Création des écrivains CSV ---

        # Crée des écrivains CSV pour les deux fichiers
        writer_f = csv.writer(f)
        writer_fs = csv.writer(fs)

        # --- Écriture des en-têtes dans les fichiers CSV ---

        # Écrit les en-têtes dans les fichiers CSV
        writer_f.writerow(PRODUCT_CSV_HEADERS)
        writer_fs.writerow(BOM_CSV_HEADERS)

        # --- Écriture des informations sur le véhicule dans le fichier CSV des produits ---

        # Écrit les informations sur le véhicule dans le fichier CSV des produits
        writer_f.writerow([
            vehiculeName + ' (' + vehiculeYear + ')', CustomVIN, brand, 'FALSE', 'TRUE', 'FALSE',
            'Used Vehicules', 'Storable Product', '0,00', '0,00', '0,00', 'Units', 'GST + QST for sales',
            'GST + QST for purchases', 'Delivered quantities', 'On received quantities', 'Buy', 'By Unique Serial Number',
            'Ronnie\'s','0', '0', '0'
        ])

        # --- Listes pour stocker les données de la nomenclature (BOM) ---

        # Listes pour stocker les données de la nomenclature (BOM)
        parts_list_cat_model = []
        parts_list_cat_group = []

        # --- Itération sur les catégories de pièces ---

        # Initialise l'ID de groupe OEM
        OEMGroupID = 0

        # Itère sur les catégories de pièces
        for parts_type in soup.select(".passemname a"):
            # Navigation vers la page de la catégorie de pièces
            print(urlsite + parts_type['href'])
            group_name = parts_type.text.strip()
            print(group_name)
            driver.get(urlsite + parts_type['href'])

            # Attendre que la page soit complètement chargée
            wait = WebDriverWait(driver, 10)  # Attendre jusqu'à 10 secondes
            # Attendre que le tag 'body' soit présent :
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            print(f"La page {driver.current_url} a complètement chargé.")

            content = driver.page_source
            soup = BeautifulSoup(content, 'lxml')

           # --- Extraction des informations sur les pièces ---

            # Liste pour stocker les informations sur les pièces
            parts_list = []

            # Compteur pour les pièces de la catégorie
            qty = 0


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

                # Extraction du reference de la pièce

                parts_reference_element = part.find('span', {"class":["itemnumstrike", "itemnum"]})
                if parts_reference_element:
                        parts_reference = parts_reference_element.text.strip()
                        if parts_reference == "TBA" or parts_reference == "NLA" or parts_reference == "UNA-VAILA-BL-EI" or parts_reference == "XXXX" or parts_reference == "XXX" or parts_reference == "-------": # certaine pieces on XXXX quand la ref n'existe pas 
                            parts_reference = "N/A"
                    
                else:
                    parts_reference = "N/A"
                

                # Condition pour ajouter la pièce à la liste
                if (price and (float(price) >= 45 or float(price) == 0) and "N/A" not in parts_reference and parts_name not in "N/A"):

                    qty += 1

                    # Ajout de la pièce à la liste principale
                    parts_list.append([
                        parts_name.lower(), parts_reference, brand,'TRUE','TRUE','TRUE',
                        'Used Parts','Storable Product','0,00', price,'0,00','Units','Tax Exempt',
                        'Tax - Exempt', 'Delivered quantities', 'On received quantities', 'Buy', 'By Unique Serial Number',
                        'Ronnie\'s','0', '0', '0'
                    ])
                    
                    # Affiche les informations sur la pièce pour le débogage
                    print(parts_name + ' -REF '+ parts_reference + ' -PX ' + price + ' -QTY : ' + str(partsqty))


                    # Ajout de la pièce à la liste des pièces par modèle
                    parts_list_cat_model.append([CustomVIN+'-'+str(OEMGroupID+1), CustomVIN+'-'+str(OEMGroupID+1), parts_reference, partsqty])

            # Si la catégorie contient au moins une pièce, on l'ajoute au fichier CSV
            if qty >= 1:
                OEMGroupID += 1
                writer_f.writerow([
                    group_name.upper(),CustomVIN+'-'+str(OEMGroupID),brand,'FALSE','TRUE','FALSE',
                    'Components','Storable Product','0,00','0,00','0,00','Units','Tax Exempt',
                    'Tax - Exempt', 'Delivered quantities', 'On received quantities', 'Buy', 'By Unique Serial Number',
                    'Ronnie\'s','0', '0', '0'
                ])
                writer_f.writerows(parts_list)
                parts_list_cat_group.append([CustomVIN,CustomVIN,CustomVIN+'-'+str(OEMGroupID),'1'])


        # Écrit les données de la nomenclature (BOM) dans le fichier CSV de la nomenclature (BOM)
        writer_fs.writerows(parts_list_cat_group)
        
        writer_fs.writerows(parts_list_cat_model)