import os
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from read_evaluation_results import load_evaluation_results


OUTPUT_DIR = "generated_graphs/rq1"


def plot_metric(df, strategy, attack, dataset, metric):
    subset = df[
        (df["detection_strategy"] == strategy) &
        (df["attack_type"] == attack) &
        (df["dataset"] == dataset)
    ].sort_values("batch_poisoning_percentage")

    if subset.empty:
        return

    plt.figure(figsize=(8, 5))

    plt.plot(
        subset["batch_poisoning_percentage"],
        subset[metric],
        marker="o"
    )

    plt.xlabel("Batch Poisoning Percentage (%)", fontsize=11)
    plt.ylabel(metric.replace("_", " ").capitalize(), fontsize=11)
    plt.title(
        f"{metric.replace('_', ' ').capitalize()} vs Batch Poisoning\n"
        f"{strategy} | {attack} | {dataset}",
        fontsize=12
    )

    plt.xticks([0, 10, 40, 70, 100])

    y_values = subset[metric].dropna()

    if not y_values.empty:
        y_min = y_values.min()
        y_max = y_values.max()

        margin = 0.02
        plt.ylim(max(0, y_min - margin), min(1.0, y_max + margin))

        plt.yticks(np.linspace(
                round(y_min - margin, 2),
                round(y_max + margin, 2),
                5
            ))


    plt.grid(True)
    plt.tight_layout()

    strategy_dir = os.path.join(OUTPUT_DIR, strategy)
    os.makedirs(strategy_dir, exist_ok=True)

    filename = f"{metric}_{attack}_{dataset}.png"
    filepath = os.path.join(strategy_dir, filename)

    plt.savefig(filepath, dpi=300)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = load_evaluation_results()

    strategies = df["detection_strategy"].unique()
    attacks = df["attack_type"].unique()
    datasets = df["dataset"].unique()
    metrics = ["accuracy", "precision", "recall", "f1_score"]

    for strategy in strategies:
        for attack in attacks:
            for dataset in datasets:
                for metric in metrics:
                    plot_metric(df, strategy, attack, dataset, metric)


if __name__ == "__main__":
    main()
