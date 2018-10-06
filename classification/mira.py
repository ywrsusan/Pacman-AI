# mira.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"

        max_correct = 0
        max_c = 0
        c_weights = util.Counter()
        weights = util.Counter()
        # self.weights = util.Counter()
        Cgrid = sorted(Cgrid)
        for c in Cgrid:
            self.weights = dict((label, util.Counter()) for label in self.legalLabels)

            for iteration in range(self.max_iterations):
                for i in range(len(trainingData)):

                    sample = trainingData[i]
                    trueLabel = trainingLabels[i]

                    predict = self.classify([sample])[0]
                    if predict != trueLabel:

                        tao = min(c, ((self.weights[predict] - self.weights[trueLabel])*sample+1.0)/ (2*(sample*sample)))
                        for feature, value in sample.items():
                            self.weights[trueLabel][feature] += tao*value
                            self.weights[predict][feature] -= tao*value
            predict_result = self.classify(validationData)
            correct_result = [predict_result[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
            if correct_result > max_correct:
                max_c = c
                max_correct = correct_result
                for l in self.legalLabels:
                    c_weights[l] = self.weights[l].copy()

        self.weights = c_weights
        self.c = max_c
        print max_c
        return max_c

    

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighOddsFeatures(self, label1, label2):
        """
        Returns a list of the 100 features with the greatest difference in feature values
                         w_label1 - w_label2

        """
        featuresOdds = []

        "*** YOUR CODE HERE ***"

        return featuresOdds
