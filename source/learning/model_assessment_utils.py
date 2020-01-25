import numpy as np

def categorical_accuracy(results, y_test):
    pred = np.argmax(results, axis=1)
    ground_truth = np.argmax(y_test, axis=1)
    return np.sum(np.equal(pred, ground_truth))/len(ground_truth)
