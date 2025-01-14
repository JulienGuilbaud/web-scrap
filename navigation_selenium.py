import random
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrap_fonction import scrape

    # --- fonction a importer ---
def open_browser_window(url):
    """Ouvre une nouvelle session de navigateur pour chaque lien avec la classe 'passemname'.

    Args:
        url: L'URL de la page principale.
    """
    # --- Configuration du pilote web ---
    service = Service(executable_path=r'.\webdriver\chromedriver.exe')
    options = webdriver.ChromeOptions()
   
   

    try:
        print(selenium.__version__)
        driver = webdriver.Chrome(service=service, options=options) # Driver initial pour la page principale
        driver.get(url) # Ouvre l'URL dans le navigateur

        div_elements = driver.find_elements(By.CLASS_NAME, "passemname") # Trouve tous les éléments <div> avec la classe "passemname"
        hrefs = [] # Liste pour stocker les liens (href)
        for div in div_elements: # Boucle sur chaque élément <div> trouvé
            a_tag = div.find_element(By.TAG_NAME, "a") # Trouve l'élément <a> (lien) à l'intérieur du <div>
            href = a_tag.get_attribute("href") # Récupère l'attribut "href" (le lien)
            hrefs.append(href) # Ajoute le lien à la liste


        time.sleep(random.uniform(1, 3)) # Attend un temps aléatoire entre 1 et 3 secondes  

        driver.quit()  # Ferme le driver initial après avoir récupéré les liens

        for href in hrefs: # Boucle sur chaque lien dans la liste
            if href: # Vérifie si le lien existe
                print(href) # Affiche le lien
                new_driver = webdriver.Chrome(service=service, options=options)  # Nouveau driver pour chaque lien (nouvelle session)
                new_driver.get(href) # Ouvre le lien dans une nouvelle session de navigateur
                
                # Traitement de la nouvelle page dans new_driver ici... (code à ajouter pour interagir avec chaque page)
                scrape(new_driver)

                time.sleep(random.uniform(1, 2)) # Attend un temps aléatoire entre 1 et 2 secondes
                new_driver.quit()  # Ferme le driver (la session) après le traitement

    except Exception as e: # Gère les exceptions (erreurs)
        print(f"Error: {e}") # Affiche l'erreur


open_browser_window("https://www.arcticcatpartshouse.com/oemparts/l/arc/5012e053f8700219481d76b3/2012-m-800-153-black-s2012m8h3eusb-parts") # Appelle la fonction avec l'URL cible

