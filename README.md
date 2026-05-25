# RotterMaatje
## AI-chatbot voor maatschappelijke ondersteuning in Rotterdam
RotterMaatje is een AI-chatbot ontwikkeld voor dakloze personen die hulp zoeken rondom dakloosheid, opvang, eten, douchen en maatschappelijke dienstverlening in Rotterdam.
---
# Probleemstelling
Mensen die dakloos zijn of maatschappelijke hulp nodig hebben ervaren vaak problemen bij:
- het vinden van betrouwbare informatie
- het begrijpen van regels en procedures
- het zoeken van opvang of medische hulp
- digitale toegankelijkheid
- taalbarrières
Veel informatie is verspreid over verschillende websites en instanties. Hierdoor is het lastig om snel de juiste hulp of ondersteuning te vinden.
---
# Doel van het project
Het doel van RotterMaatje is:
- snelle toegang bieden tot maatschappelijke informatie
- meertalige ondersteuning aanbieden
- veilige antwoorden genereren
- gebruikers doorverwijzen naar hulpinstanties
- hallucinerende AI-antwoorden beperken
- een reproduceerbare AI-pipeline ontwikkelen
---
# Doelgroep
De chatbot richt zich op:
- dak- en thuisloze personen
- EU-arbeidsmigranten
- mensen zonder papieren
- vrijwilligers
- hulpverleners
- maatschappelijke organisaties
---
# Gebruikte AI-technieken
## Gebruikte technieken
| Techniek | Toepassing |
|---|---|
| RAG | FAQ retrieval |
| Semantic Search | Similarity matching |
| Keyword Retrieval | Keyword matching |
| Sentence Transformers | Embeddings |
| Fine-tuning (SFT/LoRA) | Experimenteel |
| Safety Rules | Veilige antwoorden |
| Streamlit | Gebruikersinterface |

# Architectuur van het systeem
## Pipeline
```text
Gebruiker vraag
        ↓
Safety Rules
        ↓
Keyword Retrieval
        ↓
Semantic Retrieval
        ↓
FAQ Matching
        ↓
LLM generatie
        ↓
Veilig antwoord terug
---

# Meertalige ondersteuning

## RotterMaatje ondersteunt meerdere talen:

- Nederlands

- Engels

- Arabisch

- Pools

## Voorbeelden

| Vraag | Antwoord |

|---|---|

| Ik heb honger | Gratis brood in de Pauluskerk |

| Where can I shower? | You can shower at the Pauluskerk |

| انا جوعان | يوجد خبز مجاني |

| Nie mam miejsca do spania | Hulp via Centraal Onthaal |

---

# Safety Rules

Omdat het project werkt met kwetsbare doelgroepen zijn safety rules toegevoegd.

De chatbot:

- geeft geen medisch advies

- geeft geen drugsadvies

- verwijst bij spoed naar 112

- verwijst naar hulpverleners

- voorkomt hallucinerende antwoorden

## Voorbeelden

| Vraag | Veilig antwoord |

|---|---|

| Ik wil drugs gebruiken | Vraag hulp aan een hulpverlener |

| Ik heb pijn op mijn borst | Bel 112 bij spoed |

| Ik wil afkicken | Vraag hulp bij Straatzorg |

---

# Dataset en FAQ

De FAQ-dataset bestaat uit maatschappelijke vragen en antwoorden gebaseerd op:

- Pauluskerk

- Straatzorg Rotterdam

- Centraal Onthaal

- maatschappelijke hulpinstanties

- handmatig samengestelde safety voorbeelden

## Dataset bevat

- Nederlandse vragen

- meertalige vragen

- safety voorbeelden

- keyword variaties

- opvang- en zorginformatie

---

# Experimenten

## Experiment 1 Fine-tuning

Een SFT/LoRA model werd getraind op een kleine dataset.

### Resultaat

- hallucinerende antwoorden

- inconsistente antwoorden

- beperkte stabiliteit

### Conclusie

Fine-tuning alleen was onvoldoende betrouwbaar voor maatschappelijke ondersteuning.

---

# Experiment 2 Threshold evaluatie

Verschillende retrieval thresholds werden getest.

| Threshold | Resultaat |

|---|---|

| 0.75 | teveel fallback antwoorden |

| 0.60 | betere retrieval prestaties |

### Conclusie

Threshold 0.60 gaf betere resultaten.

---

# Experiment 3 Vergelijking van modellen

De volgende modellen zijn getest:

| Model | Observatie |

|---|---|

| Gemma | redelijk stabiel |

| Qwen | meest consistente antwoorden |

### Eindkeuze

Qwen werd gekozen als eindmodel.

---

# Evaluatie

De chatbot werd getest op:

- correcte antwoorden

- hallucinations

- multilingual prestaties

- safety gedrag

- retrieval kwaliteit

## Sterke punten

- goede FAQ retrieval

- stabiele safety antwoorden

- eenvoudige gebruikersinterface

- meertalige ondersteuning

## Zwakke punten

- kleine dataset

- sommige talen minder sterk

- afhankelijk van FAQ kwaliteit

- geen live koppeling met gemeentelijke systemen

---

# Functionaliteiten

De applicatie ondersteunt:

- chat-interface

- semantic retrieval

- keyword retrieval

- multilingual vragen

- safety rules

- FAQ matching

- Streamlit UI

- evaluatie pipeline

---

# Gebruikersinterface

De gebruikersinterface is ontwikkeld met Streamlit.

## Eigenschappen

- eenvoudige interface

- duidelijke invoervelden

- toegankelijk ontwerp

- geschikt voor kwetsbare doelgroepen

- veilige meldingen

---

# Projectstructuur

```text
rottermaatje-chatbot/
│
├── data/
├── docs/
├── frontend/
├── prompts/
├── results/
├── src/
│   ├── evaluation/
│   ├── preprocessing/
│   ├── retrieval/
│   ├── safety/
│   ├── services/
│   └── training/
├── tests/
├── visuals/
├── requirements.txt
└── README.md

# Installatie
## 1. Clone repository
```bash
git clone https://github.com/Najahkh1/rottermaatje-chatbot.git
cd rottermaatje-chatbot

2. Maak virtual environment

python3 -m venv .venv

3. Activeer virtual environment

Mac/Linux

source .venv/bin/activate

Windows

.venv\\Scripts\\activate

4. Installeer dependencies

pip install -r requirements.txt

⸻

Applicatie starten

Start Streamlit applicatie

streamlit run frontend/app.py

⸻
Reproduceerbaarheid

Het project is reproduceerbaar door:

* duidelijke mappenstructuur
* requirements.txt
* GitHub versiebeheer
* experiment logging
* vaste retrieval pipeline
* opgeslagen evaluatiescripts

⸻

Visualisaties

Visualisaties zijn gemaakt voor:

* threshold vergelijking
* modelvergelijking
* train loss
* evaluatie resultaten
* SFT datasetgroei

Locatie

results/visuals/

⸻

Toekomstig werk

Mogelijke uitbreidingen:

* grotere knowledge base
* live gemeentelijke koppelingen
* voice input
* mobiele applicatie
* uitgebreidere evaluatie datasets
* betere Arabische ondersteuning

⸻

Ethische overwegingen

Omdat het project werkt met kwetsbare groepen is extra aandacht besteed aan:

* veiligheid
* transparantie
* betrouwbaarheid
* privacy
* beperking van hallucinations
* duidelijke doorverwijzingen

De chatbot probeert geen vervanging te zijn voor hulpverleners, maar een ondersteunend hulpmiddel.

⸻

Conclusie

RotterMaatje laat zien hoe AI gebruikt kan worden binnen maatschappelijke ondersteuning.

Tijdens het project zijn meerdere AI-methoden onderzocht, geëvalueerd en verbeterd. Uiteindelijk bleek een combinatie van:

* RAG
* keyword retrieval
* semantic retrieval
* safety rules

het meest stabiel en betrouwbaar voor deze toepassing.

⸻

Ontwikkeld met

* Python
* Streamlit
* Sentence Transformers
* Hugging Face Transformers
* Scikit-learn
* Pandas
* Matplotlib

⸻

Bronnen

* Pauluskerk Rotterdam
* Straatzorg Rotterdam
* Hugging Face
* Sentence Transformers documentatie
* Streamlit documentatie
* Hogeschool Rotterdam

