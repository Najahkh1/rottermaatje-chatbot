from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments
)

from peft import (
    LoraConfig,
    get_peft_model
)

from trl import SFTTrainer


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

DATASET_PATH = "data/evaluations/sft_dataset.jsonl"


def main():

    dataset = load_dataset(
        "json",
        data_files=DATASET_PATH,
        split="train"
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM"
    )

    model = get_peft_model(
        model,
        peft_config
    )

    training_args = TrainingArguments(
        output_dir="models/rottermaatje-sft",

        per_device_train_batch_size=1,

        num_train_epochs=3,

        learning_rate=2e-4,

        logging_steps=1,

        save_strategy="epoch"
    )

    trainer = SFTTrainer(
        model=model,

        train_dataset=dataset,

        args=training_args
    )

    trainer.train()

    trainer.save_model(
        "models/rottermaatje-sft"
    )

    print("Training klaar.")


if __name__ == "__main__":
    main()