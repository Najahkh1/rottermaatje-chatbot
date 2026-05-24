import json


INPUT_PATH = "data/faq/faq.json"
OUTPUT_PATH = "data/faq/faq_enhanced.json"


CATEGORY_RULES = {
    "opvang": [
        "slaapplaats", "nachtopvang", "opvang", "dakloos", "slapen",
        "opvang geschorst", "winteropvang"
    ],
    "voedsel": [
        "eten", "honger", "brood", "maaltijd", "koffie", "thee"
    ],
    "douchen": [
        "douchen", "douche"
    ],
    "medisch": [
        "huisarts", "medische", "straatdokter", "straatzorg",
        "ziek", "chronisch", "detox", "afkicken"
    ],
    "identiteit": [
        "id", "paspoort", "bsn", "identiteitsbewijs"
    ],
    "juridisch": [
        "bezwaar", "juridisch", "papieren", "documenten",
        "asiel", "ongeldige papieren", "ongedocumenteerden"
    ],
    "gemeente": [
        "gemeente", "postadres", "wmo", "sociale dienst"
    ],
    "kleding": [
        "kleding", "wassen", "schone kleding"
    ],
    "werk": [
        "werk", "inkomen", "uitzendbureau", "ww-uitkering", "bijstand"
    ],
    "veiligheid": [
        "onveilig", "overlast", "politie", "agressief", "straat"
    ]
}


ALIASES = {
    "Ik ben dakloos uit Rotterdam en zoek een slaapplaats.": [
        "Ik heb geen plek om te slapen",
        "Ik zoek een slaapplek",
        "Ik heb geen opvang",
        "Waar kan ik vannacht slapen?",
        "Ik slaap op straat"
    ],
    "Ik heb geen geld waar kan ik eten": [
        "Ik heb honger",
        "Ik wil eten",
        "Waar kan ik gratis eten krijgen?",
        "Ik heb vandaag niks gegeten",
        "Ik zoek eten"
    ],
    "Waar kan ik douchen?": [
        "Ik wil douchen",
        "Waar kan ik mij wassen?",
        "Ik zoek een douche",
        "Kan ik ergens douchen?"
    ],
    "Ik ben niet verzekerd en heb hulp van een huisarts nodig": [
        "Ik heb medische hulp nodig",
        "Ik heb geen huisarts",
        "Ik ben ziek en niet verzekerd",
        "Ik heb een dokter nodig",
        "Waar kan ik naar een arts?"
    ],
    "Ik ben Nederlander en heb geen ID meer en heb geen geld voor paspoort of ID": [
        "Ik ben mijn ID kwijt",
        "Ik heb geen ID",
        "Mijn paspoort is weg",
        "Ik heb geen identiteitsbewijs"
    ],
    "Ik heb geen geldige papieren of documenten en mag daarom niet in Nederland wonen of werken en": [
        "Ik heb geen papieren",
        "Ik heb geen documenten",
        "Ik ben ongedocumenteerd",
        "Ik heb geen verblijfsvergunning",
        "Ik mag niet werken in Nederland"
    ],
    "Ik heb veel problemen en de gemeente Rotterdam wil mij niet helpen": [
        "De gemeente Rotterdam helpt mij niet",
        "Gemeente wil mij niet helpen",
        "Ik krijg geen hulp van de gemeente",
        "Ik heb problemen en weet niet waar ik heen moet"
    ],
    "Ik ben verslaafd en wil afkicken": [
        "Ik wil stoppen met drugs",
        "Ik gebruik drugs en wil hulp",
        "Ik ben verslaafd",
        "Ik wil afkicken",
        "Ik heb hulp nodig met drugs"
    ],
    "Ik ben uit de opvang geschorst, waar kan ik slapen": [
        "Ik ben uit de opvang gezet",
        "Ik mag niet meer naar de opvang",
        "Ik ben geschorst uit de opvang",
        "Waar kan ik slapen als ik uit de opvang ben gezet?"
    ]
}


def clean_answer(answer):
    return " ".join(answer.replace("\xa0", " ").split())


def detect_category(question, answer):
    text = f"{question} {answer}".lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "algemeen"


def enhance_faq():
    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        faq_data = json.load(file)

    enhanced = []

    for index, item in enumerate(faq_data, start=1):
        question = item.get("question", "").strip()
        answer = clean_answer(item.get("answer", ""))

        if not question or not answer:
            continue

        category = item.get("category") or detect_category(question, answer)

        enhanced_item = {
            "id": f"{category}_{index:03d}",
            "category": category,
            "question": question,
            "aliases": ALIASES.get(question, []),
            "answer": answer,
            "source": item.get("source", "FAQ vragen 3 doelgroepen"),
            "target_group": item.get("target_group", "doelgroep 1, 2 en 3")
        }

        enhanced.append(enhanced_item)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(enhanced, file, ensure_ascii=False, indent=2)

    print("FAQ enhanced successfully.")
    print(f"Items saved: {len(enhanced)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    enhance_faq()