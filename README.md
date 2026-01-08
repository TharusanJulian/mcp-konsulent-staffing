
## Hvordan kjøre prosjektet

For å kjøre dette prosjektet trenger man  Docker Desktop.


### Altså forutsetninger
- Docker Desktop må være installert og kjørende


### Steg 1: Klon repository
Klon prosjektet fra GitHub og gå inn i prosjektmappen:

git clone https://github.com/TharusanJulian/mcp-konsulent-staffing.git
cd mcp-konsulent-staffing




Steg 2:Start tjenestene

Start begge mikrotjenestene med Docker Compose:

docker compose up --build


Docker bygger nødvendige images og starter containerne automatisk.




Steg 3: Tjenester som startes

konsulent-api kjører på http://localhost:8001

llm-verktoy-api kjører på http://localhost:8002

Steg 4: Testing at løsningen fungerer

Hent listen med konsulenter:

curl http://localhost:8001/konsulenter


Hent et menneskeleselig sammendrag basert på behov:

curl "http://localhost:8002/tilgjengelige-konsulenter/sammendrag?min_tilgjengelighet_prosent=50&paakrevd_ferdighet=python"





Steg 6: Stoppe prosjektet

Trykk Ctrl + C i terminalen der prosjektet kjører.







# MCP Konsulent-Staffing – Case for Append Consulting

Dette prosjektet er en løsning på case-oppgaven gitt av Append Consulting.  
Caset handler ikke bare om å skrive kode, men om å vise hvordan jeg tenker rundt struktur, ansvar og samarbeid 
mellom ulike deler av et system.

Løsningen er bygget som to små tjenester som samarbeider:
én tjeneste som kun leverer konsulentdata, og én tjeneste som henter dataene,
filtrerer dem basert på behov, og returnerer et menneskeleselig sammendrag.



## Kort forklart

- Prosjektet består av to mikrotjenester som kjører i hver sin Docker-container
- `konsulent-api` fungerer som et enkelt register som returnerer konsulentdata
- `llm-verktoy-api` henter disse dataene, filtrerer dem basert på behov og lager et ferdig sammendrag
- Hele løsningen kan startes lokalt med én kommando: `docker compose up --build`
- Løsningen er ment å fungere som et verktøy en AI-assistent kan bruke direkte



## Hvordan jeg gikk frem for å løse caset
Da jeg fikk case-oppgaven fra Append Consulting, startet jeg med å roe helt ned og lese oppgaven flere ganger før jeg begynte å kode. 
For meg er det viktig å forstå hva som faktisk blir spurt om, før jeg hopper rett inn i tekniske detaljer.
Jeg brukte derfor tid på å kartlegge hva oppgaven egentlig går ut på, hvilke krav som er absolutte, og hva som eventuelt bare er rammer 
rundt løsningen. Grunnen til at jeg bevisst har dokumentert tankegangen min underveis, er at jeg selv liker
å kunne se tilbake på hvordan jeg resonnerte, og fordi det gjør det lettere å forklare valgene mine i etterkant, for eksempel i et intervju.
Når jeg brøt oppgaven ned til noe mer konkret, tolket jeg den som: hente konsulentdata, filtrere dem basert på noen kriterier, og forklare 
resultatet på en enkel og menneskelig måte.


## Overordnet idé

For å gjøre løsningen lettere å forstå både for meg selv og for andre  valgte jeg å se på caset som to tydelige roller.

Den første rollen er veldig enkel. Dette er i praksis et arkiv. Den gjør ingenting annet enn å gi fra seg en liste med 
konsulenter når den blir spurt. Den tar ingen avgjørelser, vurderer ingen krav og inneholder ingen logikk utover å returnere data. 
Denne rollen er implementert som `konsulent-api`.

Den andre rollen er der den faktiske “jobben” skjer. Denne tjenesten henter konsulentlisten fra arkivet,
regner ut hvor tilgjengelig hver konsulent er basert på belastning, filtrerer listen basert på minimum tilgjengelighet 
og ønsket ferdighet, og setter deretter sammen et ferdig sammendrag i naturlig språk. Dette er den delen en AI-assistent 
i praksis ville kalt for å få et svar den kan bruke direkte. Denne rollen er implementert som `llm-verktoy-api`.

DEL 5: Hvordan kjøre prosjektet (praktisk guide)

Denne delen skal være helt konkret og kjørbar, uten refleksjon eller forklaring. Den er ment for noen som faktisk vil teste løsningen.



## Prosjektstruktur og forklaring av filene

Den endelige løsningen har følgende struktur:

mcp-konsulent-staffing/
├── README.md
├── docker-compose.yml
├── konsulent-api/
│ ├── Dockerfile
│ ├── requirements.txt
│ └── app/main.py
└── llm-verktoy-api/
├── Dockerfile
├── requirements.txt
└── app/
├── models.py
├── client.py
└── main.py

markdown
Kopier kode

Jeg har bevisst holdt strukturen enkel og oversiktlig, slik at det er lett å se hvilken del som gjør hva.

### docker-compose.yml
Denne filen fungerer som limet som holder alt sammen. Den beskriver hvilke tjenester som finnes, hvordan de startes, 
og hvordan de kan kommunisere med hverandre. Når man kjører `docker compose up --build`, er det denne filen Docker bruker 
for å starte hele løsningen.

### konsulent-api
Dette er datakilden i systemet.

- `app/main.py`  
  Inneholder en hardkodet liste med konsulenter og ett endepunkt (`GET /konsulenter`) som returnerer denne listen.
  Tjenesten gjør ingen filtrering eller vurderinger, men gir kun fra seg rå data.

- `requirements.txt`  
  Lister hvilke avhengigheter tjenesten trenger for å kjøre.

- `Dockerfile`  
  Beskriver hvordan Docker skal bygge og starte denne tjenesten.

### llm-verktoy-api
Dette er tjenesten som inneholder logikken og er ment å brukes av en AI-assistent.

- `models.py`  
  Inneholder datamodeller som beskriver hvordan en konsulent og et sammendrag ser ut. Dette gjør koden mer lesbar og trygg.

- `client.py`  
  Har ansvar for å hente konsulentdata fra `konsulent-api`. Denne logikken er skilt ut for å holde koden ryddig.

- `main.py`  
  Dette er hjertet i løsningen. Her hentes konsulentene, tilgjengelighet beregnes, konsulenter filtreres basert på krav,
   og et ferdig, menneskeleselig sammendrag genereres.

- `requirements.txt` og `Dockerfile`  
  Brukes til å definere avhengigheter og hvordan Docker bygger og starter tjenesten.



  ## MCP og forholdet til AI-assistent

Oppgaven bruker begrepet MCP, Model Context Protocol. Min forståelse av dette er at det i praksis handler om å bygge 
et verktøy som en språkmodell kan bruke, for eksempel via function calling eller tool use.

I denne løsningen fungerer `konsulent-api` som en ren datakilde, mens `llm-verktoy-api` fungerer som et mellomlag som kombinerer
data og forretningslogikk og returnerer et ferdig strukturert svar. En AI-assistent trenger dermed ikke å vite hvordan dataene er 
lagret eller hvordan filtreringen fungerer, men kan nøye seg med å kalle ett endepunkt og bruke svaret direkte.

Sammendraget genereres deterministisk i denne versjonen av løsningen. Koden er likevel lagt opp slik at det enkelt kan utvides med 
en faktisk språkmodell, for eksempel via OpenRouter, dersom man ønsker det i en videreutvikling.



## Avsluttende refleksjon

Denne løsningen er bevisst holdt enkel. Målet har ikke vært å lage noe unødvendig avansert, men å vise at jeg forstår problemet
, kan dele det opp i riktige ansvarsområder, og levere en løsning som er lett å forklare og lett å bygge videre på.

Jeg har prioritert tydelig struktur, enkel kommunikasjon mellom tjenester og forutsigbar oppførsel fremfor å legge inn flere tekniske 
lag enn det oppgaven faktisk krever. Løsningen er samtidig lagt opp slik at den enkelt kan utvides videre, for eksempel med faktisk
språkmodell-integrasjon, dersom behovet skulle oppstå.







