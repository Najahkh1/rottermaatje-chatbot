import json
from docx import Document


INPUT_PATH = "data/raw/faq_vragen_3_doelgroepen.docx"
OUTPUT_PATH = "data/faq/faq.json"


def clean_text(text):
    return " ".join(text.replace("\xa0", " ").split())


def extract_faq_from_docx(filepath):
    document = Document(filepath)
    faq_items = []

    for table in document.tables:
        for row in table.rows[1:]:
            cells = row.cells

            if len(cells) < 2:
                continue

            question = clean_text(cells[0].text)
            answer = clean_text(cells[1].text)

            if question and answer:
                faq_items.append({
                    "question": question,
                    "answer": answer,
                    "source": "FAQ vragen 3 doelgroepen",
                    "target_group": "doelgroep 1, 2 en 3"
                })

    return faq_items


def main():
    faq_items = extract_faq_from_docx(INPUT_PATH)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(faq_items, file, ensure_ascii=False, indent=2)

    print(f"FAQ conversion completed.")
    print(f"Items saved: {len(faq_items)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()