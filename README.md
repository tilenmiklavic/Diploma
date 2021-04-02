# Diploma
## ANALIZA IN PREDVIDEVANJE VPLIVA OMEMB KRIPTOVALUT NA NJIHOVO CENO 

Repozitorij hrani podatke za analizo v sklopu diplomske naloge, izvorno kodo za analizo podatkov, ter izvorno kodo za spletnega agenta za obveščanje. 

Glavni deli diplomske naloge: 
- pridobivanje zgodovinskih podatkov s socialnega omrežja Twitter, kjer so se omenjale posamezne kriptovalute, časovna razporeditev teh “twittov” 
- iskanje korelacije med količino twittov in rastjo/padanjem cene posamezne kriptovalute
- izgradnja sistema za napovedovanje trenutnih/prihodnjih rasti kriptovalut glede na dogajanje na Twitterju “v živo”

### DEL 1
Opredelitev nabora opazovanih kriptovalut. Pridobivanje zgodovinskih podatkov, ki prikazujejo, kolikšna količina čivkov je v določenem časovnem okvirju omenjala izbrano kriptovaluto. Ta del bo izveden s pomočjo Twitter API-ja, oziroma drugih spletnih orodij zaradi določenih omejitev. 
Za podatke o trenutni popularnosti bi analiziral tudi objave s socialnega omrežja Reddit. 

### DEL 2
V drugem delu bi vizualiziral količino čivkov o posamezni kriptovaluti ter ceno te iste kriptovalute na isti časovni osi, ter poiskal korelacije med količinama. Predpostavka bi lahko bila: “Zaradi povečane količine čivkov o kriptovaluti ETH, je cena le te začela nihati bolj kot pa v obdobju zadnjega meseca”.  

### DEL 3
Iz ugotovitev 2. dela bi izdelal model, ki bi lahko v živo predvidel ponavljanje zgodovinskega dogajanja na trgu in o tem obvestil uporabnika. Ravno tako bi spremljal novice in čivke “vplivnežev”, kar bi posebej klasificiral kot izreden dogodek. 
Model bi nato preizkusil na trenutnem obnašanju trga in simuliral njegovo obnašanja in uspešnost napovedovanja. 

## REFERENCE
[**tweets_data**](tweets_data) Vsebuje datoteke s številom čivkov skozi čas
