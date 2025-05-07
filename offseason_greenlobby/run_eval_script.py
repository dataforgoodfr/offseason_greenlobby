# scripts/evaluate_results.py
import argparse
import pandas as pd
from llm_text_classifier.evaluation.metrics import evaluate_classification

def main(predictions_file, labels_file):
    predictions = pd.read_csv(predictions_file)
    labels = pd.read_csv(labels_file)

    y_pred = predictions['prediction']
    y_true = labels['label']

    metrics = evaluate_classification(y_true, y_pred)
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate classification results.")
    parser.add_argument('--predictions_file', type=str, required=True, help='Path to predictions CSV file.')
    parser.add_argument('--labels_file', type=str, required=True, help='Path to true labels CSV file.')

    args = parser.parse_args()
    main(args.predictions_file, args.labels_file)
