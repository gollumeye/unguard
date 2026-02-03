import os
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from read_evaluation_results import load_evaluation_results
from utils import pretty_strategy_name, pretty_attack_name, pretty_dataset_name

OUTPUT_DIR = "generated_graphs/rq1"


def plot_all_metrics(df, strategy, attack, dataset, output_dir="multi-plots"):
    subset = df[
        (df["detection_strategy"] == strategy) &
        (df["attack_type"] == attack) &
        (df["dataset"] == dataset)
    ].sort_values("batch_poisoning_percentage")

    metrics = ["accuracy", "precision", "recall", "f1_score"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, metric in enumerate(metrics):
        ax = axes[i]

        ax.plot(
            subset["batch_poisoning_percentage"],
            subset[metric],
            marker="o"
        )

        ax.set_xlabel("Batch Poisoning Percentage (%)")
        ax.set_ylabel(metric.replace("_", " ").capitalize())
        ax.set_title(metric.replace("_", " ").capitalize())

        y_values = subset[metric].dropna()

        if not y_values.empty:
            y_min = y_values.min()
            y_max = y_values.max()
            margin = 0.02
            ax.set_ylim(max(0, y_min - margin), min(1.0, y_max + margin))

        ax.set_xticks([0, 10, 40, 70, 100])
        ax.grid(True)

    strategy_name = pretty_strategy_name(strategy)
    attack_name = pretty_attack_name(attack)
    dataset_name = pretty_dataset_name(dataset)

    fig.suptitle(
        f"{strategy_name}\nAttack Type: {attack_name} | Dataset: {dataset_name}",
        fontsize=14,
        fontweight="bold"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{strategy}_{attack}_{dataset}_all_metrics.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
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
                plot_all_metrics(df, strategy, attack, dataset)


if __name__ == "__main__":
    main()
