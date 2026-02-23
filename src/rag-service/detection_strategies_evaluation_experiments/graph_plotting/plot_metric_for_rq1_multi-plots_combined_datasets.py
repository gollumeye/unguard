import os
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from read_evaluation_results import load_evaluation_results
from utils import pretty_strategy_name, pretty_attack_name, pretty_dataset_name, full_dataset_name

OUTPUT_DIR = "generated_graphs/rq1"

DATASET_DISPLAY_NAMES = {
    "Deysi_Spam_Detection": "Spam Detection Dataset",
    "ENRON": "Enron Spam Dataset",
    "Sms_Spam": "SMS Spam Collection Dataset",
    "Spam_Assassin": "Spam Assassin Dataset",
}

def plot_all_metrics_combined(df, strategy, attack, output_dir="multi-plots-combined-datasets"):
    subset = df[
        (df["detection_strategy"] == strategy) &
        (df["attack_type"] == attack)
    ]

    metrics = ["accuracy", "precision", "recall", "f1_score"]
    datasets = sorted(subset["dataset"].unique())

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, metric in enumerate(metrics):
        ax = axes[i]

        for dataset in datasets:
            dataset_subset = subset[
                subset["dataset"] == dataset
            ].sort_values("batch_poisoning_percentage")

            ax.plot(
                dataset_subset["batch_poisoning_percentage"],
                dataset_subset[metric],
                marker="o",
                label=full_dataset_name(dataset)
            )

        ax.set_xlabel("Batch Poisoning Percentage (%)")
        ax.set_ylabel(metric.replace("_", " ").capitalize())
        ax.set_title(
            metric.replace("_", " ").capitalize(),
            fontweight="bold"
        )

        ax.set_ylim(0, 1.02) # ensures lines at 1 are still visible
        ax.margins(y=0.02)  # ensures lines at 0 are still visible


        ax.set_xticks([0, 10, 40, 70, 100])
        ax.grid(True)

    strategy_name = pretty_strategy_name(strategy)
    attack_name = pretty_attack_name(attack)

    fig.suptitle(
        f"Detection Strategy: {strategy_name}\nAttack Type: {attack_name}",
        fontsize=14,
        fontweight="bold"
    )

    # One shared legend for all subplots
    handles, labels = axes[0].get_legend_handles_labels()
    legend = fig.legend(
        handles,
        labels,
        title="Datasets",
        loc="upper right"
    )

    legend.get_title().set_fontweight("bold")

    plt.tight_layout(rect=[0, 0, 0.9, 0.95])

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{strategy}_{attack}_all_datasets.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = load_evaluation_results()

    strategies = df["detection_strategy"].unique()
    attacks = df["attack_type"].unique()

    for strategy in strategies:
        for attack in attacks:
            plot_all_metrics_combined(df, strategy, attack, OUTPUT_DIR)


if __name__ == "__main__":
    main()
