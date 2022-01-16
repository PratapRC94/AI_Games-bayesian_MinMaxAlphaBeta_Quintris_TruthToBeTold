# SeekTruth.py : Classify text objects into two categories
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# Code by: Pratap Roy Choudhury[prroyc@iu.edu] | Tanu Kansal[takansal@iu.edu] | Parth Ravindra Rao[partrao@iu.edu] 
#
# Laplace Smoothing Reference : https://towardsdatascience.com/laplace-smoothing-in-na%C3%AFve-bayes-algorithm-9c237a8bdece
# Based on skeleton code by D. Crandall, October 2021
#

import sys

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):

    # some extra words, that are fillers for a sentence. Also some words series(symbols) picked from web
    extraWords = [ "and",  "for", "our", "was", "is", "at", "this", "that", "were", "in", "here", "there", "you", "was", "into",
    "through", "just", "can", "more", "how", "all", "they", "them", '.', '_', '=', ']', '!', '>', '~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', 
      '`', '}', ';', '?', '#', '$', ')', '/', "their", "been", "is", "i", "but", "to", "it", "this", "are", "any", "will",
      "did", "of", "be", "i", "a", "an", "will", "as"
    ]

    # to keep count for words existing in number of sentences
    wordOccurences = {}

    # destructuring test data
    trainObjects = train_data['objects']
    trainLabels = train_data['labels']
    trainClasses = train_data['classes']

    # for code maintainance
    firstClass = "truthful"
    secondClass = "deceptive"

    # destructuring test data
    testObjects = test_data['objects']

    # creating dictionary according to number of classes["truthful"/"deceptive"]
    for i in trainClasses:
        wordOccurences[i] = {}

    # counting number of truth/deceptive reviews in train data
    trainObjectCount = getClassObjectCount( trainObjects, trainLabels)

    # calculating probability of being truth/deceptive in train data
    trainTruthProbability = trainObjectCount[firstClass]/len(trainObjects)
    trainDeceptiveProbability = trainObjectCount[secondClass]/len(trainObjects)

    # calculating number of occurences of word in truth/deceptive reviews in train data
    for i in range(len(trainObjects)):
        splittedObject = set(trainObjects[i].lower().split(" "))
        for word in splittedObject:
            if word not in extraWords:
                if not wordOccurences[trainLabels[i]].get(word):
                    wordOccurences[trainLabels[i]][word] = 1
                else:
                    wordOccurences[trainLabels[i]][word] += 1

    # declaring result
    resultList = []

    # looping through all reviews in test data
    for i in range( len(testObjects)):
        # take review and split into unique words list
        splittedTestObject = set(testObjects[i].lower().split())

        # initialising variables
        truthNumerator = 1
        deceptiveNumerator = 1
        smoothParameter = 1

        # Posterior calculation in Naive Bayes for review being truth/decept
        for word in splittedTestObject:
            if word not in extraWords:
                # laplace smoothing
                countTruth = wordOccurences[firstClass].get( word, 0 )
                countDeceptive = wordOccurences[secondClass].get(word, 0 )
                numberOfClasses = 2

                # lookup calculation
                truthNumerator = truthNumerator * (( countTruth + smoothParameter)/(trainObjectCount[firstClass]+ smoothParameter*numberOfClasses))
                deceptiveNumerator = deceptiveNumerator * (( countDeceptive + smoothParameter)/(trainObjectCount[secondClass]+ smoothParameter*numberOfClasses))

        # multiplying prior
        truthNumerator = truthNumerator * trainTruthProbability
        deceptiveNumerator = deceptiveNumerator * trainDeceptiveProbability

        # comparing probabilities for reviews
        if( truthNumerator >= deceptiveNumerator ):
            resultList.append(firstClass)
        else:
            resultList.append(secondClass)

    return resultList

# counting number of label objects in providen data
def getClassObjectCount( objects, labels ):
    
    measure = {}
    for i in range( len(objects)):
        if not measure.get(labels[i]):
            measure[labels[i]] = 1
        else:
            measure[labels[i]] += 1

    return measure


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    # test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}
    test_data_sanitized = test_data

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))
