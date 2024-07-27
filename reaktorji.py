import requests
import os
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
from io import StringIO

# url spletne strani o jedrskih reaktorjih
reaktorji_url = "https://en.wikipedia.org/wiki/List_of_commercial_nuclear_reactors"
# url spletne strani o jedrskih nesrečah
nesrece_url = "https://en.wikipedia.org/wiki/List_of_nuclear_power_accidents_by_country"
# mapa, kjer sta shranjeni html datoteki
reaktorji_mapa = "podatki"
#datoteka kamor se shrani html o jedrskih reaktorjih
reaktorji_html = "jedrski-reaktorji.html"
#datoteka kamor se shrani html o jedrskih nesrečah
nesrece_html = "jedrske-nesrece.html"
#datoteka, v katero se shrani csv o jedrskih reaktorjih posameznih držav
reaktorji_csv = "jedrski-reaktorji.csv"
#datoteka, v katero se shrani csv o jedrskih nesrečah
nesrece_csv = "jedrske-nesrece.csv"

def shrani_url_v_niz(url):
    """Vrne vsebino strani kot niz."""
    try:
        stran = requests.get(url)        
        vsebina = stran.text
        return vsebina
    except requests.exceptions.RequestException:
        # koda, ki se izvede če pride do napake
        print("Prišlo je do napake pri nalaganju vsebine!")
        return None
    
def shrani_niz_v_datoteko(text, mapa, datoteka):
    """Zapiše niz v novo ustvarjeno datoteko."""
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, datoteka)
    with open(pot, 'w', encoding='utf-8') as dat:
        dat.write(text)
    return None

def shrani_html(url, mapa, datoteka):
    """Shrani niz url-ja v html datoteko."""
    text = shrani_url_v_niz(url)
    shrani_niz_v_datoteko(text, mapa, datoteka)

def main():
    url1 = reaktorji_url
    url2 = nesrece_url

    text1 = shrani_url_v_niz(url1)
    text2 = shrani_url_v_niz(url2)
    print("Shranil oba url-ja v niz.")

    shrani_html(url1, reaktorji_mapa, reaktorji_html)
    shrani_html(url2, reaktorji_mapa, nesrece_html)
    print("Uspesno shranil html-ja.")

    print("Konec!")

#if __name__ == "__main__":
#  main()

def preberi_dat_v_niz(mapa, datoteka):
    """Vrne celotno vsebino datoteke kot niz."""
    pot = os.path.join(mapa, datoteka)
    with open(pot, "r", encoding='utf-8') as dat:
        vsebina = dat.read()
    return vsebina

def podatki_v_csv(vsebina_strani, dat_csv, mapa):
    """Poišče tabele s podatki o potresih posamezne html strani in podatke napiše v csv datoteko."""
    soup = BeautifulSoup(vsebina_strani, "html.parser")
    pot = os.path.join(mapa,dat_csv)
    sez_tabel = soup.select("table.wikitable.sortable")
    nepotrebni_headers = ["Contents", "Overview", "Nuclear safety"]
    sez_drzav = [header.get_text() for header in soup.select("h2") if not header.get_text() in nepotrebni_headers]
    
    tabela_drzava = zip(sez_tabel, sez_drzav)    
    for i, (tabela, drzava) in enumerate(tabela_drzava):
        df = pd.read_html(StringIO(str(tabela)))        
        df = pd.concat(df)
        df.rename(columns=({"Plant name": "Plant name" + " - " + drzava, "Location" : "Location" + " - " + drzava}), inplace=True)   
        if i == 0:     
            df.to_csv(pot, mode="w", index=False)
        else:
            df.to_csv(pot, mode="a", index=False)


def main():
    vsebina1 = preberi_dat_v_niz(reaktorji_mapa, reaktorji_html)
    vsebina2 = preberi_dat_v_niz(reaktorji_mapa, nesrece_html)
    print("Shranil vsebino obeh html-jev v niz.")

    podatki_v_csv(vsebina1, reaktorji_csv, reaktorji_mapa)
    podatki_v_csv(vsebina2, nesrece_csv, reaktorji_mapa)
    print("Uspešno shranil csv-ja.")

    print("Konec!")

if __name__ == "__main__":
    main()



