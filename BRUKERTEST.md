### Brukertestrapport for TerminalPoker (Blackjack)

**Produkt:** TerminalPoker

**Testdeltakere:** Mine foreldre

### Introduksjon

Som en del av en kontinuerlig prosess for å forbedre TerminalPoker, en tekstbasert Blackjack-variant kjørt i terminalen, organiserte jeg en brukertest med mine foreldre som deltakere. Målet med testen var å identifisere områder for forbedring i brukerdialogen, responsiviteten i spillet, og det generelle brukergrensesnittet. Her er en oversikt over de viktigste funnene og de tiltakene som ble implementert som respons på tilbakemeldingene.

### Forberedelser

Jeg valgte å teste den nyeste versjonen av TerminalPoker, et spill som benytter SQLite for å lagre spillets tilstand, og JSON for å lagre en virtuell kortstokk. Mine foreldre, som har moderat erfaring med kortspill og en god grad av teknisk kompetanse, valgte jeg som testdeltagere

### Testmetode

Testen ble gjennomført ved å observere mine foreldre mens de spilte flere runder av spillet. Jeg noterte hvordan de interagerte med spillet, deres reaksjoner på brukergrensesnittet og spillets mekanikker, samt eventuelle utfordringer de møtte underveis. Jeg noterte også eventuelle feilmeldinger underveis, så jeg kunne fikse opp i de.

### Gjennomføring av Testen

Jeg introduserte spillet og dets grunnleggende funksjoner før de begynte å spille. Jeg observerte deres evne til å navigere i brukergrensesnittet, og hvordan de reagerte på spillmekanikken. Spesielt fokuserte jeg på deres opplevelser med brukerdialogen og spillresponsiviteten.

### Oppdaterte Anbefalinger og Implementeringer

1. **Forbedret Brukerdialog:**
    - Jeg la til flere interaktive og informative dialoger i spillet for å gi tydeligere instruksjoner og bedre feedback. Dette hjalp mine foreldre til å forstå spillets status og mulige handlinger bedre. Samtidig så merket jeg at med dårligere syn, var det vanskelig å finne ut av hvilke kort de hadde, så da farget jeg de blå i senere versjoner.
2. **Responsivitetsforbedringer:**
    - Jeg optimaliserte spillkoden for å øke ventetid mellom handlingene, noe som skapte en mer ekte spillopplevelse for mine foreldre.
3. **Intuitivt Brukergrensesnitt:**
    - Jeg redesignet brukergrensesnittet for å gjøre det mer brukervennlig. Det nye designet gjorde det enklere for mine foreldre å navigere i spillet og forstå hvordan de skulle utføre forskjellige spillhandlinger.

### Konklusjon

Gjennom denne brukertesten med mine foreldre, fikk jeg verdifulle innsikter som førte til flere betydelige forbedringer i TerminalPoker. Disse endringene har forbedret brukeropplevelsen mye, og jeg planlegger å fortsette å evaluere og forbedre spillet basert på ytterligere tilbakemeldinger fra andre utenfor brukertester.