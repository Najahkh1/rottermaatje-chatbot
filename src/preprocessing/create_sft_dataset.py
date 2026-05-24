import json

INPUT_PATH = "data/evaluations/preference_dataset.jsonl"
OUTPUT_PATH = "data/evaluations/sft_dataset.jsonl"


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as input_file, \
         open(OUTPUT_PATH, "w", encoding="utf-8") as output_file:

        for line in input_file:
            line = line.strip()

            if not line:
                continue

            item = json.loads(line)

            sft_item = {
                "messages": [
                    {
                        "role": "user",
                        "content": item["prompt"]
                    },
                    {
                        "role": "assistant",
                        "content": item["chosen"]
                    }
                ]
            }

            output_file.write(
                json.dumps(sft_item, ensure_ascii=False) + "\n"
            )

    print("SFT dataset gemaakt.")
    print(f"Opgeslagen als: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()