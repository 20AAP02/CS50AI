from cProfile import label
from cmath import log10
import csv
from datetime import datetime
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()
    with open(filename, 'r') as file:
        next(file)
        csvreader = csv.reader(file)
        for row in csvreader:
            ev_values = row[:-1]
            for i in range(len(ev_values)):
                # Convert string numbers to int
                if i in [0, 2, 4, 11, 12, 13, 14]:
                    ev_values[i] = int(ev_values[i])
                # Turn mounth in int
                if i == 10:
                    if ev_values[i] == 'June':
                        ev_values[i] = 5
                    else:
                        ev_values[i] = int(datetime.strptime(ev_values[i], "%b").month) - 1
                # Converting Visitor type in to int
                if i == 15:
                    ev_values[i] = int(ev_values[i] == 'Returning_Visitor')
                # Converting Weekend in to int
                if i == 16:
                    ev_values[i] = int(ev_values[i] == 'TRUE')
                # Convert string numbers in float
                if i in [1, 3, 5, 6, 7, 8, 9]:
                    ev_values[i] = float(ev_values[i])
            evidence.append(ev_values)
            # Add to labels the revenue
            labels.append(int(row.pop().lower() == 'true'))
    return ((evidence, labels))


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return (model.fit(evidence, labels))


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    pos_len = 0
    neg_len = 0
    pos_right = 0
    neg_right = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            pos_len += 1
            if labels[i] == predictions[i]:
                pos_right += 1
        else:
            neg_len += 1
            if labels[i] == predictions[i]:
                neg_right += 1
    sensitivity = pos_right / pos_len
    specificity = neg_right / neg_len
    return ((sensitivity, specificity))

if __name__ == "__main__":
    main()
