import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

out_dir = Path("results/visuals")
out_dir.mkdir(parents=True, exist_ok=True)


# 1. Model + threshold vergelijking
scores = pd.DataFrame({
    "Experiment": [
        "Gemma\nthreshold 0.75",
        "Qwen\nthreshold 0.75",
        "Gemma\nthreshold 0.60",
        "Qwen\nthreshold 0.60"
    ],
    "Score": [75, 75, 80, 82]
})

plt.figure(figsize=(9, 5))
plt.bar(scores["Experiment"], scores["Score"])
plt.title("Preference-score per model en threshold")
plt.ylabel("Totale preference-score")
plt.ylim(0, 100)

for i, v in enumerate(scores["Score"]):
    plt.text(i, v + 1, str(v), ha="center")

plt.tight_layout()
plt.savefig(out_dir / "01_model_threshold_scores.png", dpi=200)
plt.close()


# 2. Threshold effect
threshold_scores = pd.DataFrame({
    "Threshold": ["0.75", "0.60"],
    "Beste score": [75, 82]
})

plt.figure(figsize=(7, 5))
plt.plot(
    threshold_scores["Threshold"],
    threshold_scores["Beste score"],
    marker="o"
)
plt.title("Effect van threshold-verlaging op preference-score")
plt.xlabel("Retrieval threshold")
plt.ylabel("Beste preference-score")
plt.ylim(60, 90)

for i, v in enumerate(threshold_scores["Beste score"]):
    plt.text(i, v + 1, str(v), ha="center")

plt.tight_layout()
plt.savefig(out_dir / "02_threshold_effect.png", dpi=200)
plt.close()


# 3. Methodevergelijking
methods = pd.DataFrame({
    "Methode": [
        "Baseline LLM",
        "System prompt",
        "RAG + FAQ",
        "Multilingual embeddings",
        "Syntax/keyword rules",
        "Safety rules",
        "RAG + web sources",
        "SFT/LoRA"
    ],
    "Betrouwbaarheid": [1, 2, 4, 4, 3, 5, 4, 2]
})

plt.figure(figsize=(9, 5))
plt.barh(methods["Methode"], methods["Betrouwbaarheid"])
plt.title("Vergelijking van methoden binnen RotterMaatje")
plt.xlabel("Bijdrage aan betrouwbaarheid (1-5)")
plt.xlim(0, 5)

for i, v in enumerate(methods["Betrouwbaarheid"]):
    plt.text(v + 0.05, i, str(v), va="center")

plt.tight_layout()
plt.savefig(out_dir / "03_method_comparison.png", dpi=200)
plt.close()


# 4. SFT training resultaat
sft = pd.DataFrame({
    "Dataset": [
        "SFT 15 voorbeelden",
        "SFT 51 voorbeelden"
    ],
    "Train loss": [3.09, 1.91]
})

plt.figure(figsize=(7, 5))
plt.bar(sft["Dataset"], sft["Train loss"])
plt.title("SFT/LoRA training: effect van grotere dataset")
plt.ylabel("Train loss")
plt.ylim(0, 4)

for i, v in enumerate(sft["Train loss"]):
    plt.text(i, v + 0.08, str(v), ha="center")

plt.tight_layout()
plt.savefig(out_dir / "04_sft_loss_comparison.png", dpi=200)
plt.close()


# 5. Eindarchitectuur als simpele pipeline
fig, ax = plt.subplots(figsize=(12, 5))
ax.axis("off")

steps = [
    ("Gebruiker", 0.08, 0.6),
    ("Safety rules\nmedisch/drugs/112", 0.26, 0.6),
    ("Semantic retrieval\nMiniLM-L12-v2", 0.46, 0.6),
    ("FAQ + web\nbronnen", 0.64, 0.6),
    ("Qwen 3 4B\nantwoordmodel", 0.82, 0.6),
]

for label, x, y in steps:
    ax.text(
        x, y, label,
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", linewidth=1),
        fontsize=10
    )

for x1, x2 in [(0.14, 0.20), (0.33, 0.39), (0.53, 0.58), (0.70, 0.76)]:
    ax.annotate(
        "",
        xy=(x2, 0.6),
        xytext=(x1, 0.6),
        arrowprops=dict(arrowstyle="->", lw=1.5)
    )

plt.title("Eindpipeline RotterMaatje")
plt.tight_layout()
plt.savefig(out_dir / "05_final_pipeline.png", dpi=200)
plt.close()


# 6. Experimentoverzicht tabel
experiment_table = pd.DataFrame({
    "Experiment": [
        "Baseline",
        "RAG",
        "Multilingual MiniLM",
        "Threshold 0.60",
        "Syntax rules",
        "Safety rules",
        "SFT/LoRA"
    ],
    "Resultaat": [
        "Veel hallucinations",
        "Meer grounded antwoorden",
        "Betere meertalige matching",
        "Score stijgt naar 82",
        "Goed voor kritieke woorden",
        "Beste effect op veiligheid",
        "Training gelukt, output nog zwak"
    ],
    "Conclusie": [
        "Niet geschikt",
        "Behouden",
        "Behouden",
        "Beste instelling",
        "Als guardrail gebruiken",
        "Essentieel",
        "Alleen experiment"
    ]
})

fig, ax = plt.subplots(figsize=(12, 5))
ax.axis("off")

table = ax.table(
    cellText=experiment_table.values,
    colLabels=experiment_table.columns,
    cellLoc="left",
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(8.5)
table.scale(1, 1.6)

plt.title("Experimentoverzicht en conclusies", pad=20)
plt.tight_layout()
plt.savefig(out_dir / "06_experiment_table.png", dpi=200, bbox_inches="tight")
plt.close()


print("Visualisaties opgeslagen in results/visuals")