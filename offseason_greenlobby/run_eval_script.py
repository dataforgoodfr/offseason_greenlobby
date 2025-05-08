import argparse
import pandas as pd
from config import COL_LABEL,COL_PREDICTIONS,METRICS
from evaluation.metrics import evaluate_classification
from utils.utils import list_of_strings
import os.path
from sklearn.metrics import confusion_matrix
from datetime import datetime


def main(predictions_file: str, metrics_param: list, verbose: bool, save: bool, output_file: str):
    """
    """

    # Load dataset
    predictions = pd.read_csv(predictions_file)

    # Get columns
    y_true = predictions[COL_LABEL].str.lower()
    y_pred = predictions[COL_PREDICTIONS].str.lower()

    # Compute the desired metrics 
    metrics = evaluate_classification(y_true, y_pred)

    metrics["prompt"] = [predictions['prompt'].values[0]]
    metrics["idee"] = [predictions['IDEES'].values[0]]
    metrics["y_true"] = [y_true.to_list()]
    metrics["y_pred"] = [y_pred.to_list()]
    metrics["time_eval"] = [datetime.now()]


    # Plot
    if verbose == True:
        print("Confusion matrix:")
        print(confusion_matrix(y_pred=y_pred,y_true=y_true,labels=["oui","non"]))
        for metric in metrics_param:
            print(f"{metric}: {metrics[metric][0]:.4f}")

    # If save parameter is set
    if save == True:
        # If the file already exists
        if os.path.isfile(output_file):
            df_res = pd.read_csv(
                output_file)
            for metric, value in metrics.items():
                metrics[metric] = value[0]
            df_res.loc[-1] = metrics
            df_res.to_csv(output_file,index=0)
        # Else create it
        else:
            pd.DataFrame.from_dict(metrics).to_csv(
                output_file,
                index=0,)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate classification results.")
    parser.add_argument('--predictions_file', type=str, required=True, help='Path to predictions CSV file.')
    parser.add_argument('--metrics_param', type=list_of_strings, default=METRICS, help='List of metrics to plot. Default ["accuracy", "precision", "recall","f1_score"]')
    parser.add_argument('--verbose', type=bool, default=True, help='Boolean to plot or not to plot')
    parser.add_argument('--save', type=bool, default=True, help='Decision to save evaluation output to output file.')
    parser.add_argument('--output_file', type=str, default="../data/results/eval/evaluations.csv", help='Output file')

    args = parser.parse_args()
    main(args.predictions_file, args.metrics_param, args.verbose, args.save, args.output_file)



