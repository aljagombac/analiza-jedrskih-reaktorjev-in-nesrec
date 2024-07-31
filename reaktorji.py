import requests
import os
from bs4 import BeautifulSoup
import re
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

def poisci_tabele(vsebina_strani, soup):
    """Iz spletne strani izlušči tabele s podatki o jedrskih reaktorjih za posamezno državo."""    
    sez_tabel = soup.select("table.wikitable.sortable")
    return sez_tabel

def poisci_drzave(vsebina_strani, soup):
    """Iz spletne strani izlušči imena državz z jedrskimi reaktorji."""
    nepotrebni_headers = ["Contents", "Overview", "Nuclear safety"]
    sez_drzav = []
    for header in soup.select("h2"):
        if not header.get_text() in nepotrebni_headers:
            sez_drzav.append(header.get_text())    
    return sez_drzav

def preimenovanje_stolpcev(tabela, sez_novih_imen):
    """Preimenuje stolpce tabele."""
    df = pd.read_html(StringIO(str(tabela)))        
    df = pd.concat(df)
    sez_imen_stolpcev = df.columns.tolist() 

    preimenovati = {}
    for i, stolpec in enumerate(sez_imen_stolpcev):
        if stolpec == "Unnamed: 9":
            continue
        preimenovati[stolpec] = sez_novih_imen[i]

    df.rename(columns=(preimenovati), inplace=True)   
    return df

def dodaj_stolpec(df, drzava):
    """doda en stolpec tabeli."""
    stevilo_vrstic = len(df)
    stolpec = (stevilo_vrstic)*[drzava]

    if "Lokacija" in df.columns.tolist():
        return df
    else:
        df.insert(1, column="Lokacija", value=stolpec)
        return df

def pocisti_podatke(df):
    vzorec = "(\\[\\d+\\])?"
    pociscen_df = df.replace(vzorec, '', regex=True)
    return pociscen_df

def uredi_tabele(tabele, drzave, sez_imen):
    """Vsaki tabeli preimenuje stolpce in doda en nov stolpec ter vrne seznam Dataframe-ov tabel."""
    tabela_drzava = zip(tabele, drzave) 

    sez_df = []   
    for i, (tabela, drzava) in enumerate(tabela_drzava):
        df = preimenovanje_stolpcev(tabela, sez_imen)
        df = dodaj_stolpec(df, drzava)
        df = pocisti_podatke(df)
        sez_df.append(df)
    return sez_df

def zdruzi_in_zapisi_v_csv(sez_df, dat_csv, mapa):
    """Združi tabele v en Dataframe in iz njega naredi csv.S"""
    pot = os.path.join(mapa,dat_csv)
    df_vse_tabele = pd.concat(sez_df)
    if 'Unnamed: 9' in df_vse_tabele.columns.tolist():
        df_vse_tabele.drop('Unnamed: 9', axis=1, inplace=True)

    df_vse_tabele.to_csv(pot, mode="w", index=False)

def main():
    
    vsebina1 = preberi_dat_v_niz(reaktorji_mapa, reaktorji_html)
    vsebina2 = preberi_dat_v_niz(reaktorji_mapa, nesrece_html)
    print("Shranil vsebino obeh html-jev v niz.")

    soup1 = BeautifulSoup(vsebina1, "html.parser")
    soup2 = BeautifulSoup(vsebina2, "html.parser")

    tabele1 = poisci_tabele(vsebina1, soup1)
    tabele2 = poisci_tabele(vsebina2, soup2)
    print("Uspešno poiskal tabele.")

    drzave1 = poisci_drzave(vsebina1, soup1)
    drzave2 = poisci_drzave(vsebina2, soup2)
    print("Uspešno poiskal imena držav.")

    sez_imen1 = ["Ime elektrarne", "Številka reaktorja", "Tip", "Model", "Status", "Moč (MW)", "Začetek gradnje", "Začetek delovanja", "Datum zaprtja"]
    sez_imen2 = ["Datum", "Lokacija", "Opis", "Smrti", "Strošek", "INES ocena"]

    sez_df1 = uredi_tabele(tabele1, drzave1, sez_imen1)
    sez_df2 = uredi_tabele(tabele2, drzave2, sez_imen2)
    print("Uspešno uredil tabele.")

    zdruzi_in_zapisi_v_csv(sez_df1, reaktorji_csv, reaktorji_mapa)
    zdruzi_in_zapisi_v_csv(sez_df2, nesrece_csv, reaktorji_mapa)

    print("Konec!")

#if __name__ == "__main__":
#    main()





