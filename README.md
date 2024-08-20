# Analiza jedrskih reaktorjev in jedrskih nesreč

## Opis

V tej projektni nalogi analiziramo podatke o jedrskih reaktorjih in nesrečah iz [Seznama komercianlnih reaktorejv po državah](https://en.wikipedia.org/wiki/List_of_commercial_nuclear_reactors) in [Seznama jedrskih nesreč po državah](https://en.wikipedia.org/wiki/List_of_nuclear_power_accidents_by_country). Programi, vsebovani v projektu, poskrbijo za zajemanje podatkov, ki jih predelajo in shranijo v pregledno obliko. Analizo pa opravimo v Jupyter Notebooku.

#### Zajemanje podatkov

Koda za pridobivanje podatkov je napisana v datoteki `reaktorji.py` v programerskem jeziku Python. Ob zagonu naloži html kodo spletne strani `podatki/jedrski-reaktorji.html` in `podatki/jedrske-nesrece.html`, prebere podatke v tabelah in jih preoblikuje v ustrezno obliko ter zapiše v csv datoteki `podatki/jedrski-reaktorji.csv` in `podatki/jedrske-nesrece.csv`. Natančnejša navodila so razložena še v [Navodilih za uporabo](https://github.com/aljagombac/jedrski-reaktorji-projektna-uvp/tree/main?tab=readme-ov-file#navodila-za-uporabo).

#### Analiziranje podatkov

Analiza podatkov je zapisana v `analiza/reaktorji_nesrece.ipynb` v formatu Jupyter Notebook, v isti mapi pa se nahajajo še uporabljene zunanje datoteke. Rezultati so postopoma predstavljeni z grafi, tabelami in zemljevidi, ki si jih lahko ogledamo direktno v [`analiza/reaktorji_nesrece.ipynb`](https://github.com/aljagombac/jedrski-reaktorji-projektna-uvp/blob/5dedc32c918fda6e83af7a0f87947f397854f755/analiza/reaktoji_nesrece.ipynb)

## Navodila za uporabo

Najprej si namestimo repozitorij v izbrano mapo, pripravimo virtualno okolje, če je potrebno in naložimo knjižnice.

#### Priprava virtualnega okolja (za Linux uporabnike)
V izbrani mapi izvedemo ukaz 
```console
python -m venv venv
```
in aktiviramo okolje, kjer nalagamo naslednje knjižnice.
```console
source venv/bin/activate
```

#### Knjižnice

Knjižnice naložimo z ukazom `pip` ali `pip3`. 
Najprej naložimo html s knjižnico in iz html-ja pridobimo iskane podatke 
```console
pip install requests
```
```console
pip install beautifulsoup4
```
Da lahko poganjamo Jupyter Notebook naložimo tudi 
```console
pip install jupyter
```
Za urejanje in prikaz podatkov pa uporabimo knjižnice:
```console
pip install pandas
```
```console
pip install geopandas matplotlib
```

#### Zagon
Na koncu še poženemo program z ukazom:
```console
python reaktorji.py
```
Pri analizi podatkov pa v Jupyter Notebook poganjamo celice.






