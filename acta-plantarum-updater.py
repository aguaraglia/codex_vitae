import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

def create_search_url(name):
    # Pulisce il nome e lo formatta per la ricerca
    name = re.sub(r'\s+var\.\s+', ' ', name)  # Rimuove "var."
    name = re.sub(r'\s+subsp\.\s+', ' ', name)  # Rimuove "subsp."
    name = name.split(',')[0]  # Rimuove eventuali autori dopo la virgola
    
    # Codifica il nome per l'URL
    encoded_name = requests.utils.quote(name)
    return f"https://www.actaplantarum.org/flora/flora_info.php?id=&nnn={encoded_name}"

def check_acta_plantarum(name):
    url = create_search_url(name)
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Verifica se la pagina contiene informazioni valide sulla specie
            if soup.find('div', {'class': 'scheda'}):
                return url
            
        return None
        
    except Exception as e:
        print(f"Errore durante la ricerca di {name}: {str(e)}")
        return None

def update_acta_plantarum_links():
    # Legge il CSV
    df = pd.read_csv('endemismi.csv')
    
    # Itera sulle righe dove ActaPlantarum è vuoto
    for index, row in df.iterrows():
        if pd.isna(row['ActaPlantarum']):
            print(f"Cercando {row['Name']}...")
            
            # Controlla ActaPlantarum
            acta_link = check_acta_plantarum(row['Name'])
            
            if acta_link:
                print(f"Trovato link per {row['Name']}")
                df.at[index, 'ActaPlantarum'] = acta_link
            
            # Aspetta un po' per non sovraccaricare il server
            time.sleep(2)
    
    # Salva il CSV aggiornato
    df.to_csv('endemismi_updated.csv', index=False)
    print("Aggiornamento completato!")

if __name__ == "__main__":
    update_acta_plantarum_links()
    
