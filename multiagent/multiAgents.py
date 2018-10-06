# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        if chosenIndex == 'STOP' and len(bestIndices) > 1:
            bestIndices.remove(chosenIndex)
            chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"


        ghostPosition = successorGameState.getGhostPositions()
        if newPos in ghostPosition: return -999999

        score = 100

        for i in range(len(ghostPosition)):
            ghost = ghostPosition[i]
            if newScaredTimes[i] == 0:
                distance = abs(ghost[0]-newPos[0])+abs(ghost[1]-newPos[1])
                if distance == 0: return -999999
                score += distance


        foodList = currentGameState.getFood().asList()
        if newPos in foodList: score += 20

        current_dist = 999999
        new_dist = 999999
        currentPos = currentGameState.getPacmanPosition()
        for food in foodList:
            tmp_distance = abs(food[0]-currentPos[0])+abs(food[1]-currentPos[1])
            if tmp_distance < current_dist: current_dist = tmp_distance

            tmp_distance = abs(food[0]-newPos[0])+abs(food[1]-newPos[1])
            if tmp_distance < new_dist: new_dist = tmp_distance

        if new_dist < current_dist: score += 100

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """


    def minimax(self, gameState, depth, numOfAgents):
        # print gameState
        if numOfAgents >= gameState.getNumAgents():
            numOfAgents = 0
        if numOfAgents > 0: minimax_state = "Min"
        else: minimax_state = "Max"
        # print minimax_state
        if gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState), " ")

        actions = gameState.getLegalActions(numOfAgents)

        if depth == 0:
            return (self.evaluationFunction(gameState)," ")

        # max_state
        if minimax_state == "Max":
            max_score = -99999
            bestAction = "STOP"
            for action in actions:
                nextState = gameState.generateSuccessor(numOfAgents,action)
                # print "here:"
                # print self.minimax(nextState, minimax_state*(-1), depth-1)
                score, temp = self.minimax(nextState, depth-1, numOfAgents+1)
                if score > max_score:
                    max_score = score
                    bestAction = action
            return (max_score,bestAction)
        # min_state
        elif minimax_state == "Min":
            min_score = 99999
            bestAction = "STOP"
            for action in actions:
                nextState = gameState.generateSuccessor(numOfAgents,action)
                score,temp  = self.minimax(nextState, depth-1, numOfAgents+1)
                if score < min_score:
                    min_score = score
                    bestAction = action
            return (min_score,bestAction)


    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        actionStack = util.Stack();
        state_score, action = self.minimax(gameState, self.depth*gameState.getNumAgents(), 0)
        return action



        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphabeta(self, gameState, depth, numOfAgents, alpha, beta):
        # print gameState
        if numOfAgents >= gameState.getNumAgents():
            numOfAgents = 0
        if numOfAgents > 0: minimax_state = "Min"
        else: minimax_state = "Max"

        if gameState.isLose() or gameState.isWin():
            return (self.evaluationFunction(gameState), " ")

        if depth == 0:
            return (self.evaluationFunction(gameState), " ")

        actions = gameState.getLegalActions(numOfAgents)
        # max_state
        if minimax_state == "Max":
            max_score= -99999
            bestAction = "STOP"
            for action in actions:
                nextState = gameState.generateSuccessor(numOfAgents,action)
                score, temp = self.alphabeta(nextState, depth-1, numOfAgents+1, alpha, beta)

                if score > max_score:
                    max_score = score
                    bestAction = action
                if score > alpha:
                    alpha = score
                if score > beta:
                    break

            return (max_score,bestAction)
        # min_state
        elif minimax_state == "Min":
            min_score = 99999
            bestAction = "STOP"
            for action in actions:
                nextState = gameState.generateSuccessor(numOfAgents,action)
                score,temp  = self.alphabeta(nextState, depth-1, numOfAgents+1, alpha, beta)

                if score < min_score:
                    min_score = score
                    bestAction = action
                if score < beta:
                    beta = score
                if score < alpha:
                    break
            return (min_score,bestAction)



    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        actionStack = util.Stack();
        state_score, action = self.alphabeta(gameState, self.depth*gameState.getNumAgents(), 0, -999999, 999999)
        return action





        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectmax(self, gameState, depth, numOfAgents):
        # print gameState
        numOfAgents = numOfAgents%gameState.getNumAgents()
        if numOfAgents > 0: expectmax_state = 'Expect'
        else: expectmax_state = 'Max'

        if gameState.isLose() or gameState.isWin() or depth == 0:
            return (self.evaluationFunction(gameState), ' ')

        actions = gameState.getLegalActions(numOfAgents)
        # max_state
        if expectmax_state == 'Max':
            max_score= -99999
            bestAction = 'STOP'
            # print "new: "
            for action in actions:
                nextState = gameState.generateSuccessor(numOfAgents,action)
                score, temp = self.expectmax(nextState, depth-1, numOfAgents+1)

                if score > max_score:
                    max_score = score
                    bestAction = action

            return (max_score,bestAction)
        # min_state
        else:
            totalScores = 0
            for action in actions:
                nextState = gameState.generateSuccessor(numOfAgents,action)
                score,temp  = self.expectmax(nextState, depth-1, numOfAgents+1)
                totalScores += score
            if len(actions) > 0:
                averageScore = totalScores/len(actions)
                return (averageScore, ' ')
            return (0, ' ')


    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        state_score, action = self.expectmax(gameState, self.depth*gameState.getNumAgents(), 0)
        return action

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:

      Firstly check if it's a Win state, and return a high score for Win state

      Calculate the Manhattan distance between current position and ghost position.
      If the ghost could be eaten by pacman, try to get close to ghost (by minus
      the distance), and add a bonus if pacman eats a ghost, otherwise try to get
      away from ghost (by add the distance).

      Give a bonus when pacman eats food, or eats a capsule. and give bonus to pacman
      whenever it makes food less than before.

      Add a weighted .getScore() to the final score to give time Penalty.

    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    if currentGameState.isWin():
        return 99999

    ghostPosition = currentGameState.getGhostPositions()

    score = 100

    for i in range(len(ghostPosition)):
        ghost = ghostPosition[i]
        distance = abs(ghost[0]-newPos[0])+abs(ghost[1]-newPos[1])
        if newScaredTimes[i] == 0:
            if distance == 0: return -99999
            score += distance
        else:
            score -= distance
            if distance == 0: score += 50


    foodList = currentGameState.getFood().asList()
    if newPos in foodList: score += 50
    capsuleList = currentGameState.getCapsules()
    if newPos in foodList: score += 100
    foodList += capsuleList


    # current_dist = 99999
    # new_dist = 99999
    # for food in foodList:
    #     tmp_distance = abs(food[0]-newPos[0])+abs(food[1]-newPos[1])
    #     if tmp_distance < new_dist: new_dist = tmp_distance

    score = score - 50*len(foodList)

    return score + currentGameState.getScore()


    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
