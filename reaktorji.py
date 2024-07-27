import requests
import os
from bs4 import BeautifulSoup
import re
import csv
import calendar
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
  print("Shranil oba url-ja v niz")

  shrani_html(url1, reaktorji_mapa, reaktorji_html)
  shrani_html(url2, reaktorji_mapa, nesrece_html)
  print("Uspesno shranil html-ja")

  print("Konec")

#if __name__ == "__main__":
#  main()
