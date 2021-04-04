"""A module that trains a classifier to predict shopping sales.

Time spent:
v1: 25 + 35

Examples:
    $ python3 shopping.py shopping.csv
"""

import csv
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

TEST_SIZE = 0.4


def convert_month(month):
    month_dict = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'June': 5,
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11
    }
    return month_dict[month]


def convert_visitor_type(visitor):
    if visitor == 'Returning_Visitor':
        return 1
    return 0


def convert_bool_to_int(boolean):
    return int(boolean)


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
    df = pd.read_csv(filename)
    columns = df.columns.tolist()
    int_cols = [
        'Administrative', 'Informational', 'ProductRelated', 'Month',
        'OperatingSystems', 'Browser', 'Region', 'TrafficType', 'VisitorType',
        'Weekend'
    ]
    float_cols = [
        'Administrative_Duration', 'Informational_Duration',
        'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues',
        'SpecialDay'
    ]

    df['Month'] = df['Month'].apply(convert_month)
    df['VisitorType'] = df['VisitorType'].apply(convert_visitor_type)
    df['Weekend'] = df['Weekend'].apply(convert_bool_to_int)
    df['Revenue'] = df['Revenue'].apply(convert_bool_to_int)

    # ensure same order
    assert df.columns.tolist() == columns

    # sadly can't just convert to list with df.values.tolist() because it
    # changes types. Not sure if autograder is going to check types.
    # https://stackoverflow.com/questions/57730170/dataframe-to-list-of-list-without-change-in-data-type-of-values
    exclude_revenue = df.columns[:-1]
    evidence = list(map(list, df[exclude_revenue].itertuples(index=False)))
    labels = df['Revenue'].values.tolist()
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    clf = KNeighborsClassifier(n_neighbors=1)
    clf.fit(evidence, labels)
    return clf
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_labels = 0
    correct_positive_labels = 0
    negative_labels = 0
    correct_negative_labels = 0

    # compute counts
    for i in range(len(labels)):
        # positive labels
        if labels[i] == 1:
            positive_labels += 1
            if predictions[i] == 1:
                correct_positive_labels += 1
        # negative labels
        else:
            negative_labels += 1
            if predictions[i] == 0:
                correct_negative_labels += 1
    
    sensitivity = correct_positive_labels / positive_labels
    specificity = correct_negative_labels / negative_labels
    print(sensitivity, specificity)

    print(classification_report(labels, predictions))
    report = classification_report(labels, predictions, output_dict=True)
    positive_class_recall = report['1']['recall']
    negative_class_recall = report['0']['recall']
    assert positive_class_recall == sensitivity
    assert negative_class_recall == specificity

    return sensitivity, specificity



def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(evidence,
                                                        labels,
                                                        test_size=TEST_SIZE)

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


if __name__ == "__main__":
    main()
