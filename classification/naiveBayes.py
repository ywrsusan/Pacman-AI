# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1 # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting counts over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the correct label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """

        "*** YOUR CODE HERE ***"
        # print self.features

        # library_ = util.Counter()
        # labelCount_ = util.Counter()
        # for l in self.legalLabels:
        #     library_[l] = util.Counter()
        #
        # for i in range(len(trainingData)):
        #     sample = trainingData[i]
        #     label = trainingLabels[i]
        #     labelCount_[label] += 1
        #     for feature, value in sample.items():
        #         library_[label][feature] += value
        #
        # # smoothing and testing
        # correct = util.Counter()
        # for k in kgrid:
        #     self.library = util.Counter()
        #     for l in self.legalLabels:
        #         self.library[l] = library_[l].copy()
        #     self.labelCount = labelCount_.copy()
        #
        #     #smoothing
        #     self.labelCount.incrementAll(self.legalLabels, k)
        #     self.labelCount.divideAll(self.labelCount.totalCount()+len(self.legalLabels)*k)
        #     self.labelCount.normalize()
        #     for l in self.legalLabels:
        #         self.library[l].incrementAll(self.features, k)
        #         self.library[l].divideAll(self.labelCount[l] + len(self.features)*k)
        #         self.library[l].normalize()
        #
        #     #testing
        #     predict = self.classify(validationData)
        #     correct[k] = [predict[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
        #
        #     #print
        #     print k, float(correct[k])/float(len(validationData ))
        #
        #
        # k = correct.argMax()
        # self.library = util.Counter()
        # for l in self.legalLabels:
        #     self.library[l] = library_[l].copy()
        # self.labelCount = labelCount_.copy()
        #
        # self.labelCount.incrementAll(self.legalLabels, k)
        # self.labelCount.divideAll(self.labelCount.totalCount() + len(self.legalLabels)*k)
        # self.labelCount.normalize()
        # for l in self.legalLabels:
        #     self.library[l].incrementAll(self.features, k)
        #     self.library[l].divideAll(self.labelCount[l] + len(self.features)*k)
        #     self.library[l].normalize()



        conditionalProbOfFeature_ = util.Counter()
        labelCount_ = util.Counter()
        probOfFeature_ = util.Counter()
        correct = util.Counter()

        for i in range(len(trainingData)):
            sample = trainingData[i]
            label = trainingLabels[i]
            labelCount_[label] += 1
            for feature, value in sample.items():
                probOfFeature_[(label, feature)] += 1
                conditionalProbOfFeature_[(label, feature)] += value

        # smoothing and testing
        for k in kgrid:
            self.probOfFeature = probOfFeature_.copy()
            self.conditionalProbOfFeature = conditionalProbOfFeature_.copy()
            self.labelCount = labelCount_.copy()
            self.labelCount.normalize()
            for l in self.legalLabels:
                for feature in self.features:
                    self.conditionalProbOfFeature[(l, feature)] += k
                    self.conditionalProbOfFeature[(l, feature)] /= float(self.probOfFeature[(l,feature)]+2*k)

            predict = self.classify(validationData)
            correct[k] = [predict[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)

        k = correct.argMax()
        self.probOfFeature = probOfFeature_.copy()
        self.conditionalProbOfFeature = conditionalProbOfFeature_.copy()
        self.labelCount = labelCount_.copy()
        self.labelCount.normalize()
        self.k = k
        for l in self.legalLabels:
            for feature in self.features:
                self.conditionalProbOfFeature[(l, feature)] += k
                self.conditionalProbOfFeature[(l, feature)] /= float(self.probOfFeature[(l,feature)]+2*k)


    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()

        "*** YOUR CODE HERE ***"

        for label in self.legalLabels:
            logJoint[label] = math.log(self.labelCount[label])
            for feature, value in datum.items():
                if value == 1:
                    logJoint[label] += math.log(self.conditionalProbOfFeature[(label,feature)])
                elif value == 0:
                    logJoint[label] += math.log(1-self.conditionalProbOfFeature[(label,feature)])
                else: print "OTHER", value
        return logJoint


        # for label in self.legalLabels:
        #     logJoint[label] = math.log(self.prior[label])
        #     for feat, value in datum.items():
        #         if value > 0:
        #             logJoint[label] += math.log(self.conditionalProb[feat,label])
        #         else:
        #             logJoint[label] += math.log(1-self.conditionalProb[feat,label])
        #
        # return logJoint

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        featuresOdds = []

        "*** YOUR CODE HERE ***"
        temp = []
        
        for feature in self.features:
            pa = self.conditionalProbOfFeature[(label1, feature)]
            pb = self.conditionalProbOfFeature[(label2, feature)]
            if pb == 0:
                pa += 0.000001
                pb += 0.000001
            temp.append([feature, float(pa)/float(pb)])
        temp = sorted(temp,key = lambda l:l[1], reverse=True)
        for element in temp:
            featuresOdds.append(element[0])
        featuresOdds = featuresOdds[0:99]

        # for feat in self.features:
        #     featuresOdds.append((self.conditionalProbOfFeature[label1,feat]/self.conditionalProbOfFeature[label2, feat], feat))
        # featuresOdds.sort()
        # featuresOdds = [feat for val, feat in featuresOdds[-100:]]
        #
        # return featuresOdds
        #
        #

        return featuresOdds
