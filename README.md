# Diploma

## Lokalna uspostavitev okolja

Celoten sistem lahko poženemo tudi lokalno, tako da sledimo spodnjim navodilom: 

- repozitorij prenesemo na svoj računalnik z ukazom `git clone https://github.com/tilenmiklavic/Diploma`

V mapi website se nahaja izvorna koda za spletni vmesnik, preko katerega lahko spremljamo aktualne cene in napovedi.
- Premaknemo se v delovno mapo projekta z ukazom `cd website/src/app/`.
- Ukaz `npm install` bo poskrbel, da se prenesejo vsi paketi, ki so nujni za delovanje aplikacije. 
- Da bo spetna stran tudi delovala, jo poženemo z ukazom `ng serve --host 0.0.0.0`
- Spletna stran bo po uspešnem zagonu dostopna na `htpp://localhost:4200`

Sedaj je potrebno zagnati še zaledni del aplikacije.

- premaknemo se v korensko mapo projekta. 
- z ukazom `pip install -r requirements.txt` namestimo vse potrebne pakete za delovanje Python zalednega dela aplikacije
- premaknemo se v mapo `server`
- z ukazom `npm install` namestimo vse potrebne pakete za izvajanje Node zaledne aplikacije
- z ukazom `npm run prod` zaženemo zaledni del, ki je sedaj dostopen na naslovu `http://localhost:3000`
