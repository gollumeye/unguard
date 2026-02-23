def pretty_strategy_name(name):
    mapping = {
        "embedding_similarity_batch_level": "Embedding Similarity (Batch-Level)",
        "embedding_similarity_entry_level": "Embedding Similarity (Entry-Level)",
        "embeddings_cluster_analysis": "Embedding Cluster Analysis",
        "ann_label_consistency": "ANN Label Consistency",
        "knn_label_consistency": "KNN Label Consistency",
    }
    return mapping.get(name, name.replace("_", " ").title())


def pretty_attack_name(name):
    mapping = {
        "label_flipping": "General Label Flipping",
        "targeted_label_flipping": "Targeted Label Flipping",
        "keyword_injection": "Keyword Injection",
    }
    return mapping.get(name, name.replace("_", " ").title())

DATASET_DISPLAY_NAMES = {
    "deysi_spam_detection": "Spam Detection Dataset",
    "enron": "Enron Spam Dataset",
    "sms_spam": "SMS Spam Collection Dataset",
    "spam_assassin": "Spam Assassin Dataset",
}

def full_dataset_name(name):
    return DATASET_DISPLAY_NAMES.get(name, name)
