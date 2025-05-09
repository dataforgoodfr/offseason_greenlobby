from sklearn.metrics import accuracy_score 
from sklearn.metrics import precision_score 
from sklearn.metrics import recall_score 
from sklearn.metrics import f1_score


def evaluate_classification(y_true, y_pred):
    return {
        "accuracy": [accuracy_score(y_true, y_pred)],
        "precision": [precision_score(y_true, y_pred, average='weighted')],
        "recall": [recall_score(y_true, y_pred, average='weighted')],
        "f1_score": [f1_score(y_true, y_pred, average='weighted')]
    }