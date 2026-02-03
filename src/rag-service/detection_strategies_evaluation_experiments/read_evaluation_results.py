import os
import json
import pandas as pd
import numpy as np


def load_evaluation_results(base_dir="evaluation_results"):
    rows = []

    for detection_strategy in os.listdir(base_dir):
        strategy_path = os.path.join(base_dir, detection_strategy)
        if not os.path.isdir(strategy_path):
            continue

        for attack_type in os.listdir(strategy_path):
            attack_path = os.path.join(strategy_path, attack_type)
            if not os.path.isdir(attack_path):
                continue

            for file in os.listdir(attack_path):
                if file.endswith(".json"):
                    file_path = os.path.join(attack_path, file)

                    with open(file_path, "r") as f:
                        data = json.load(f)


                    if "experiment_configuration" not in data:
                        print(f"Skipping file without experiment_configuration: {file_path}")
                        continue

                    config = data["experiment_configuration"]
                    batch_percentage = config["batch_poisoning_percentage"]

                    accuracy = data["accuracy"]
                    precision = data["precision"]
                    recall = data["recall"]
                    f1_score = data["f1_score"]

                    if batch_percentage == 0:
                        precision = np.nan
                        recall = np.nan
                        f1_score = np.nan

                    rows.append({
                        "detection_strategy": config["detection_strategy"],
                        "attack_type": config["attack_type"],
                        "dataset": config["dataset_name"],
                        "batch_poisoning_percentage": batch_percentage,
                        "accuracy": accuracy,
                        "precision": precision,
                        "recall": recall,
                        "f1_score": f1_score,
                        "true_positives": data["true_positives"],
                        "false_positives": data["false_positives"],
                        "true_negatives": data["true_negatives"],
                        "false_negatives": data["false_negatives"],
                    })

    return pd.DataFrame(rows)
