# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        def computeValue(mdp, state, iterationCount):

            if mdp.isTerminal(state):
                # self.values[state] = 0
                return self.values[state]

            # if self.values[state] != 0:
            #     return self.values[state]
            iterationCount -= 1
            if iterationCount < -1:
                return self.values[state];

            actions = mdp.getPossibleActions(state)
            maxExpect = -9999
            for action in actions:
                expect = 0.0
                transactionAndProb = mdp.getTransitionStatesAndProbs(state, action)

                for element in transactionAndProb:
                    # print element
                    nextState = element[0]
                    nextIteration = iterationCount
                    expect += element[1]*(mdp.getReward(state, action, nextState)+computeValue(mdp, nextState, nextIteration)*discount)

                if expect > maxExpect:
                    maxExpect = expect

            self.values[state] = maxExpect
            return maxExpect


        allStates = mdp.getStates()
        for i in range(self.iterations):
            # print "iteration number", i
            temp = util.Counter()
            for state in allStates:
                if self.mdp.isTerminal(state):
                    continue;
                maxExpect = -9999
                for action in mdp.getPossibleActions(state):
                    expect = self.computeQValueFromValues(state, action);
                    if expect > maxExpect:
                        maxExpect = expect

                temp[state] = maxExpect
            self.values = temp


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        utility = 0.0;
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            utility += prob*(self.mdp.getReward(state, action, nextState)+self.values[nextState]*self.discount)
        return utility
        util.raiseNotDefined()

        # state_prob = self.mdp.getTransitionStatesAndProbs(state,action)
        # val = 0
        # for (next_state,prob) in state_prob:
        #     reward = self.mdp.getReward(state,action,next_state)
        #     val += prob*(reward+self.discount*self.values[next_state])
        # return val

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        maxValue = -9999
        bestAction = None
        for action in self.mdp.getPossibleActions(state):
            value = self.computeQValueFromValues(state, action)
            if value > maxValue:
                maxValue = value
                bestAction = action

        return bestAction


        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
