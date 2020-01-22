import numpy as np

def categorical_accuracy(results, y_test):
    pred = np.argmax(results, axis=1)
    ground_truth = np.argmax(y_test, axis=1)
    return np.sum(np.equal(pred, ground_truth))/len(ground_truth)

def expected_value(results, y_test):
    pred = np.argmax(results, axis=1)
    ground_truth = np.argmax(y_test, axis=1)
    # same win_matrix as in rps_game except everything is shifted down since the model
    # is trying to predict what the opponent *would* play (and hence play whatever beats it)
    win_matrix = {2: {0: 0,
                      1: -1,
                      2: 1},
                  0: {0: 1,
                      1: 0,
                      2: -1},
                  1: {0: -1,
                      1: 1,
                      2: 0}
                  }

    outcomes = []
    for i in range(len(pred)):
        outcomes.append(win_matrix[pred[i]][ground_truth[i]])
    outcomes = np.array(outcomes)
    return outcomes