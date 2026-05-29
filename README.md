# RotterMaatje
## AIchatbot voor maatschappelijke ondersteuning in Rotterdam
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
- mensen zonder papieren
- vrijwilligers
- hulpverleners
- maatschappelijke organisaties
---
# Gebruikte modellen

Tijdens het project zijn meerdere Large Language Models (LLMs) gebruikt, getest en vergeleken.

## Geteste modellen

| Model | Gebruik binnen project |
|---|---|
| Qwen 3 4B Instruct | Eindmodel voor chatbot |
| Gemma 3 4B IT | Vergelijkingsmodel tijdens evaluaties |

## Waarom meerdere modellen?

De modellen zijn getest op:

- stabiliteit

- retrieval prestaties

- multilingual ondersteuning

- hallucinations

- safety gedrag

- consistentie van antwoorden

##  Waarom Qwen als eindmodel?

Qwen gaf tijdens de experimenten:

- stabielere antwoorden

- betere retrieval resultaten

- minder hallucinations

- betere helper-context ondersteuning

- consistentere multilingual antwoorden

Daardoor werd Qwen gekozen als uiteindelijke chatbotmodel.

---


# Gebruikte AI-technieken

## Gebruikte technieken

| Techniek | Toepassing binnen RotterMaatje |
|---|---|
| RAG | Antwoorden ophalen uit de FAQ-dataset |
| Semantic Search | Vergelijkbare vragen herkennen |
| Keyword Retrieval | Belangrijke woorden herkennen zoals “honger” of “opvang” |
| Rule-based Logic | Safety rules, helper-context en fallback logica |
| Sentence Transformers | Tekst omzetten naar embeddings voor similarity matching |
| Fine-tuning (SFT/LoRA) | Experimenteren met eigen getrainde modellen |
| Safety Rules | Onveilige of medische antwoorden blokkeren |
| Language Detection | Herkennen van Nederlands, Engels, Arabisch en Pools |
| Streamlit | Frontend en chat-interface bouwen |
| Reinforcement Learning (Contextual Bandit) | Dynamisch kiezen van retrieval- en safetystrategie |

# Architectuur van het systeem

## Pipeline

```text
Gebruiker vraag
        ↓
Language Detection
        ↓
RL Strategy Selector
        ↓
Safety Rules
        ↓
Keyword Retrieval / Semantic Retrieval
        ↓
FAQ Matching
        ↓
Qwen 3 4B Instruct
        ↓
Veilig antwoord terug
```
---

# Meertalige ondersteuning

RotterMaatje ondersteunt meerdere talen:

- Nederlands
- Engels
- Arabisch
- Pools

## Voorbeelden

| Vraag | Antwoord |
|---|---|
| Ik heb honger | Gratis brood in de Pauluskerk |
| انا جوعان | يوجد خبز مجاني |
| Nie mam miejsca do spania | Hulp via Centraal Onthaal |
---

# Safety Rules

Omdat RotterMaatje werkt met kwetsbare doelgroepen zijn safety rules toegevoegd om veiligere antwoorden te genereren.

De chatbot:

- geeft geen direct medisch advies
- geeft geen advies over drugsgebruik
- verwijst bij spoed naar 112
- verwijst gebruikers naar hulpverleners
- gebruikt fallback antwoorden bij onduidelijke vragen
- herkent helper-context van vrijwilligers en hulpverleners
- probeert hallucinerende antwoorden te beperken
- gebruikt alleen informatie uit de FAQ-context

## Safety technieken

| Techniek | Toepassing |
|---|---|
| Medical Safety | Medische diagnoses blokkeren |
| Drug Safety | Drugsadvies blokkeren |
| Fallback Responses | Veilig antwoord geven bij onbekende vragen |
| Helper-context detectie | Vrijwilliger-vragen herkennen |
| Rule-based filtering | Risicovolle vragen detecteren |

## Voorbeelden

| Vraag | Veilig antwoord |
|---|---|
| Ik wil drugs gebruiken | Vraag hulp aan een hulpverlener |
| Ik heb pijn op mijn borst | Bel 112 bij spoed |
| Ik wil afkicken | Vraag hulp bij Straatzorg |
| Ik help iemand die medische hulp nodig heeft | Vraag hulp bij Straatzorg Rotterdam |
| Een dakloze is niet verzekerd | Vraag hulp bij Straatzorg Rotterdam |

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

## Experiment 1 Eerste FAQ retrieval

### Doel

Controleren of semantic retrieval basisvragen correct kon herkennen.

### Getest

- eenvoudige FAQ-vragen
- similarity matching
- eerste retrieval thresholds

### Problemen

- veel fallback antwoorden
- korte vragen werkten slecht
- vragen zoals “ik wil eten” werden soms niet herkend

### Verbeteringen

- extra FAQ-variaties toegevoegd
- keywords toegevoegd
- semantic retrieval verbeterd

### Conclusie

Semantic retrieval werkte beter na uitbreiding van de FAQ-dataset en keyword matching.

---

# Experiment 2 Threshold evaluatie

### Doel

Testen welke similarity threshold betere retrieval prestaties gaf.

### Geteste thresholds

- 0.75
- 0.60

## Resultaten

| Threshold | Observatie |
|---|---|
| 0.75 | teveel fallback antwoorden |
| 0.60 | betere FAQ matches |

### Conclusie

Threshold 0.60 gaf betere retrieval prestaties.

---

# Experiment 3 Fine-tuning (SFT/LoRA)

### Doel

Onderzoeken of een fine-tuned model betere antwoorden kon genereren.

### Getest

- kleine SFT dataset
- Gemma/Qwen fine-tuning
- LoRA training

### Resultaten

- train loss verbeterde
- antwoorden bleven soms hallucineren
- modellen waren minder stabiel dan retrieval

### Conclusie

Fine-tuning alleen was onvoldoende betrouwbaar voor maatschappelijke ondersteuning.

---

# Experiment 4 Vergelijking van modellen

### Geteste modellen

- Gemma
- Qwen

### Evaluatiepunten

- stabiliteit
- multilingual antwoorden
- FAQ retrieval
- safety gedrag
- hallucinations

## Resultaten

| Model | Observatie |
|---|---|
| Gemma | redelijk stabiel |
| Qwen | meest consistente antwoorden |

### Conclusie

Qwen werd gekozen als eindmodel.

---

# Experiment 5 Multilingual testing

### Geteste talen

- Nederlands
- Engels
- Arabisch
- Pools

### Getest

- retrieval
- safety antwoorden
- FAQ matching

### Resultaten

- Nederlands werkte het beste
- Engels werkte stabiel
- Arabisch en Pools werkten redelijk goed
- sommige vertalingen bleven beperkt

### Conclusie

De chatbot ondersteunt meerdere talen, maar Nederlandse retrieval bleef het sterkst.

---

#  Experiment 6 Safety testing

### Doel

Controleren of onveilige vragen veilig werden afgehandeld.

### Getest

- medische vragen
- drugsgerelateerde vragen
- spoedvragen

### Voorbeelden

- “ik wil drugs gebruiken”
- “ik heb pijn op mijn borst”

### Resultaten

- safety responses werkten stabiel
- 112-verwijzingen werkten correct
- hallucinations werden verminderd

### Conclusie

Safety rules verbeterden de betrouwbaarheid van de chatbot.

---

# Experiment 7 Vrijwilliger / helper-context experiment

### Doel

Onderzoeken of vrijwilliger-vragen correct werden herkend.

### Testvragen

- “ik help iemand die honger heeft”
- “een cliënt zoekt opvang”
- “een dakloze is niet verzekerd”

### Problemen

- safety rules blokkeerden te veel vragen
- retrieval werkte vooral op directe “ik”-vragen

### Verbeteringen

- helper-context detectie toegevoegd
- rule-based filtering aangepast
- FAQ uitgebreid met vrijwilliger-variaties

### Resultaten

Vrijwilliger-vragen werden correct ondersteund.

### Conclusie

De chatbot ondersteunt nu meerdere doelgroepen en begrijpt ook vragen van vrijwilligers en hulpverleners.

# Experiment 8 Reinforcement Learning

## Doel

Onderzoeken of de chatbot automatisch kan leren welke retrievalstrategie het beste werkt voor verschillende soorten vragen.

## Aanpak

Er is een Contextual Multi-Armed Bandit ontwikkeld.

De RL-component bepaalt eerst het vraagtype en kiest vervolgens automatisch een strategie.

### Mogelijke strategieën

- keyword_retrieval
- semantic_retrieval
- safety_response
- fallback_response

### Vraagtypes

- food_question
- hygiene_question
- safety_question
- medical_emergency
- helper_food_question
- helper_shelter_question
- medical_care_question
- identity_question
- undocumented_question
- postal_address_question

## Resultaten

Gemiddelde reward:

0.67

Voorbeelden:

| Vraagtype | Beste strategie |
|---|---|
| Food question | Keyword Retrieval |
| Hygiene question | Semantic Retrieval |
| Safety question | Safety Response |
| Medical emergency | Safety Response |
| Helper shelter question | Semantic Retrieval |

## Conclusie

De RL-component werd opgenomen in de uiteindelijke pipeline als strategie-selector.

## Evaluatie

De chatbot werd getest op:

- correcte FAQ-antwoorden

- hallucinations

- multilingual prestaties

- safety gedrag

- retrieval kwaliteit

- vrijwilliger-vragen

- helper-context detectie

- fallback responses

- RL-gebaseerde strategie selectie

- geëvalueerde fine-tuning aanpak

- reproduceerbare trainingspipeline


## Geteste scenario’s

| Testtype | Voorbeelden |
|---|---|
| FAQ retrieval | “ik wil eten” |
| Safety testing | “ik wil drugs gebruiken” |
| Medische vragen | “ik heb pijn op mijn borst” |
| Multilingual testing | Engels, Arabisch en Pools |
| Vrijwilliger-vragen | “ik help iemand die honger heeft” |
| Helper-context | “een cliënt zoekt opvang” |

## Sterke punten

- goede FAQ retrieval

- stabiele safety antwoorden

- ondersteuning voor meerdere talen

- helper-context detectie voor vrijwilligers

- duidelijke fallback responses

- eenvoudige gebruikersinterface

- lage hallucination kans door FAQ-context

- reproduceerbare pipeline

## Zwakke punten

- relatief kleine dataset

- sommige talen werken minder sterk

- afhankelijk van FAQ kwaliteit

- beperkte real-time informatie

- geen productieomgeving

- sommige complexe vragen blijven moeilijk

## Belangrijkste conclusie

De combinatie van:

- RAG

- semantic retrieval

- keyword retrieval

- helper-context detectie

- safety rules

- Qwen 3 4B Instruct

- RL Strategy Selector



gaf de meest stabiele en veilige resultaten voor maatschappelijke ondersteuning.

Fine-tuning werd succesvol onderzocht, maar bleek minder betrouwbaar dan de retrieval-gebaseerde aanpak.

# Experiment 8 Reinforcement Learning

## Doel

Onderzoeken of de chatbot automatisch kan leren welke retrievalstrategie het beste werkt voor verschillende soorten vragen.

## Aanpak

Er is een Contextual Multi-Armed Bandit ontwikkeld.

De RL-component bepaalt eerst het vraagtype en kiest vervolgens automatisch een strategie.

### Mogelijke strategieën

- keyword_retrieval
- semantic_retrieval
- safety_response
- fallback_response

### Vraagtypes

- food_question
- hygiene_question
- safety_question
- medical_emergency
- helper_food_question
- helper_shelter_question
- medical_care_question
- identity_question
- undocumented_question
- postal_address_question

## Resultaten

Gemiddelde reward:

0.67

Voorbeelden:

| Vraagtype | Beste strategie |
|---|---|
| Food question | Keyword Retrieval |
| Hygiene question | Semantic Retrieval |
| Safety question | Safety Response |
| Medical emergency | Safety Response |
| Helper shelter question | Semantic Retrieval |

## Conclusie

De RL-component werd opgenomen in de uiteindelijke pipeline als strategie-selector.
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
```
# Installatie

## 1. Clone repository

```bash
git clone https://github.com/Najahkh1/rottermaatje-chatbot.git
cd rottermaatje-chatbot
```

## 2. Maak virtual environment

```bash
python3 -m venv .venv
```

## 3. Activeer virtual environment

### Mac/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 4. Installeer dependencies

```bash
pip install -r requirements.txt
```

---

# Applicatie starten

```bash
streamlit run frontend/app.py
```

---

# Reproduceerbaarheid

Het project is reproduceerbaar door:

- duidelijke mappenstructuur
- `requirements.txt`
- GitHub versiebeheer
- experiment logging
- vaste retrieval pipeline
- opgeslagen evaluatiescripts

---

# Visualisaties

Visualisaties zijn gemaakt voor:

- threshold vergelijking
- modelvergelijking
- train loss
- evaluatie resultaten
- SFT datasetgroei

## Locatie

```text
results/visuals/
```

---

# Toekomstig werk

Mogelijke uitbreidingen:

- grotere knowledge base
- voice input
- uitgebreidere evaluatie datasets
- betere meertalige ondersteuning

---

# Ethische overwegingen

Omdat het project werkt met kwetsbare groepen is extra aandacht besteed aan:

- veiligheid
- transparantie
- betrouwbaarheid
- beperking van hallucinations
- duidelijke doorverwijzingen

De chatbot vervangt geen hulpverleners, maar is bedoeld als ondersteunend hulpmiddel.

---

# Conclusie

RotterMaatje laat zien hoe AI gebruikt kan worden binnen maatschappelijke ondersteuning.

Tijdens het project zijn meerdere AI-methoden onderzocht, geëvalueerd en verbeterd. Uiteindelijk bleek een combinatie van:

- RAG
- keyword retrieval
- semantic retrieval
- safety rules

het meest stabiel en betrouwbaar voor deze toepassing.

---

# Ontwikkeld met

- Python
- Streamlit
- Sentence Transformers
- Hugging Face Transformers
- Scikit-learn
- Pandas
- Matplotlib

---

# Bronnen

## Maatschappelijke bronnen

- [Pauluskerk Rotterdam](https://www.pauluskerkrotterdam.nl/)
- [Straatzorg Rotterdam](https://straatzorgrotterdam.nl)
- [Centraal Onthaal Rotterdam](https://www.rotterdam.nl/dak-of-thuisloos)
- [Stichting Ontmoeting Rotterdam](https://www.ontmoeting.nl/locaties/rotterdam/)
- [Juridisch Loket](https://www.juridischloket.nl/)
- [Gemeente Rotterdam](https://www.rotterdam.nl/dak-of-thuisloos)
- [Woonnet Rijnmond](https://www.woonnetrijnmond.nl/nl-NL)
- [Stichting Barka](https://barkanl.org)
- [IOM Nederland](https://iom-nederland.nl)

## AI en Machine Learning bronnen

- [Hugging Face](https://huggingface.co/)
- [Sentence Transformers](https://www.sbert.net/docs/package_reference/sentence_transformer/index.html)
- [Transformers documentatie](https://huggingface.co/docs/transformers/index)
- [Streamlit documentatie](https://docs.streamlit.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

## Gebruikte modellen

- [Qwen](https://huggingface.co/Qwen)
- [Gemma](https://ai.google.dev/gemma)
- [Sentence Transformer all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

## Gebruikte technieken

- [Retrieval-Augmented Generation](https://huggingface.co/learn/cookbook/rag_zephyr_langchain)
- [Semantic Search](https://www.sbert.net/examples/applications/semantic-search/README.html)
- [Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Fine-tuning / SFT](https://huggingface.co/docs/trl/sft_trainer)
- [LoRA](https://huggingface.co/papers/2106.09685)
- [Reinforcement Learning](https://huggingface.co/learn/deep-rl-course)

- [Multi-Armed Bandit](https://www.tensorflow.org/agents/tutorials/intro_bandit)

- [Contextual Bandit](https://arxiv.org/abs/1003.0146)

- [Contextual Bandits with Linear Payoff Functions](https://arxiv.org/abs/1502.05477)