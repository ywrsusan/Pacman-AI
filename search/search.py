# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def checkVisitedNode(path, nextState):

    tempStack = util.Stack()
    flag = True
    while path.isEmpty() != True:
        temp = path.pop()
        tempStack.push(temp)
        if temp[0] == nextState[0]:
            flag = False

    while tempStack.isEmpty()!=True:
        temp = tempStack.pop()
        path.push(temp)
    return flag;


def DFS(problem, path, currentState):


    if problem.isGoalState(currentState):
        return True
    else:

        #print "Current State:", currentState
        successors = problem.getSuccessors(currentState)
        #print "Current successors:", successors
        for element in successors:
            # search if it's already in the Stack
            if checkVisitedNode(path, element):
                path.push(element)
                if (DFS(problem, path, element[0]) == True):
                    return True
                else:
                    path.pop()
    return False;


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    path = util.Stack()

    currentState = problem.getStartState()
    path.push((currentState, 'Stop', 1))
    if DFS(problem, path, currentState):
        #print "Goal Found."
        pathList = [path.pop()[1]]
        count = 0
        while path.isEmpty()!=True:
            count +=1
            temp = path.pop()
            if temp[1] != 'Stop':
                pathList.insert(0, temp[1])
        return pathList
    else:
        print "Goal Not Found."


    util.raiseNotDefined()

# def checkVisitedNode(visitedQueue, nextState):
#     tempQueue = util.Queue()
#     flag = True;
#     while (visitedQueue.isEmpty()!=True):
#         temp = visitedQueue.pop()
#         tempQueue.push(temp)
#         if temp[0] == nextState[0]:
#             flag = False
#
#     while (tempQueue.isEmpty()!=True):
#         temp = tempQueue.pop()
#         visitedQueue.push(temp)
#
#     return flag


def findPreState(currentState):
    state = currentState[0]
    x,y = state[0], state[1]

    if currentState[1] == 'South':
        dx = 0
        dy = 1
    elif currentState[1] == 'North':
        dx = 0
        dy = -1

    elif currentState[1] == 'East':
        dx = -1
        dy = 0
    elif currentState[1] == 'West':
        dx = 1
        dy = 0
    else:
        dx = 0
        dy = 0

    return (int(x+dx), int(y+dy))
    # if currentState[1] == 'South':
    #     return tuple(map(sum,zip(state , (0,1))))
    # elif currentState[1] == 'North':
    #     return tuple(map(sum,zip(state , (0,-1))))
    # elif currentState[1] == 'East':
    #     return tuple(map(sum,zip(state , (-1,0))))
    # elif currentState[1] == 'West':
    #     return tuple(map(sum,zip(state , (1,0))))
    # else:
    #     return state

def checkExistedNodeQueue(NodeQueue, nextState):
    tempQueue = util.Queue()
    flag = True
    while NodeQueue.isEmpty()!=True:
        temp = NodeQueue.pop()
        tempQueue.push(temp)
        if temp[0] == nextState[0]:
            flag = False
    while tempQueue.isEmpty()!=True:
        temp= tempQueue.pop()
        NodeQueue.push(temp)

    return flag

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    NodeQueue = util.Queue()
    visitedNode = util.Stack()
    startState = (problem.getStartState(), 'Stop', 1)
    NodeQueue.push(startState)

    parents = {}
    # currentState =NodeQueue.pop()
    # print currentState
    while (NodeQueue.isEmpty() != True):
        currentState = NodeQueue.pop()
        if problem.isGoalState(currentState[0]):
            # print "goal: ",currentState
            # print "Goal Found"
            break
        visitedNode.push(currentState)
        successors = problem.getSuccessors(currentState[0])
        for element in successors:
            if(checkVisitedNode(visitedNode, element) and checkExistedNodeQueue(NodeQueue, element)):
                #print element, currentState
                parents[element] = currentState
                NodeQueue.push(element)

    path = util.Stack()
    path.push(currentState)

    while True:
        if currentState in parents:
            parent = parents[currentState]
            path.push(parent)
            currentState = parent
        else:
            break

    # back reverse
    pathList = list()
    while path.isEmpty()!=True:
        temp = path.pop()
        if temp[1] != 'Stop':
            pathList.append(temp[1])
            #print temp;
    # "length: ", len(pathList)

    return pathList

    util.raiseNotDefined()


def checkExistedNodePQueue(NodePQueue, nextState):
    tempQueue = util.Queue()
    flag = True

    while NodePQueue.isEmpty()!=True:
        temp = NodePQueue.pop()
        if temp[0] == nextState[0]:
            if temp[2] > nextState[2]:
                continue;
            else:
                flag = False
        # if temp == nextState:
        #     flag = False
        tempQueue.push(temp)

    while tempQueue.isEmpty()!=True:
        temp= tempQueue.pop()
        NodePQueue.push(temp, temp[2])

    return flag

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    startState = (problem.getStartState(), 'Stop', 0)
    NodePQueue = util.PriorityQueue()
    NodePQueue.push(startState, startState[2])
    visitedNode = util.Stack()
    parents = {}

    while (NodePQueue.isEmpty()!=True):

        currentState = NodePQueue.pop()
        visitedNode.push(currentState)
        if problem.isGoalState(currentState[0]):
            print "Goal Found"
            break;

        successors = problem.getSuccessors(currentState[0])
        for element in successors:
            #print element
            element = (element[0], element[1], element[2]+currentState[2])
            if (checkVisitedNode(visitedNode, element) and checkExistedNodePQueue(NodePQueue, element)):
                NodePQueue.push(element, element[2])
                parents[element] = currentState

    path = util.Stack()
    path.push(currentState)

    while True:
        if currentState in parents:
            #print temp
            parent = parents[currentState]
            path.push(parent)
            currentState = parent
        else:
            break

    pathList = list()
    while (path.isEmpty()!=True):
        temp = path.pop()
        if temp[1] != 'Stop':
            pathList.append(temp[1])

    return pathList



    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    # if problem is PositionSearchProblem:
    #     goal = problem.goal
    # elif problem is GraphSearch:
    #     goal = problem.goals
    # goal = problem.goals
    # distance = testClasses.heuristic
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    startState = (problem.getStartState(), 'Stop', 0)
    NodePQueue = util.PriorityQueue()
    NodePQueue.push(startState, startState[2])
    visitedNode = util.Stack()
    visitedNodeList = list()
    parents = {}
    while (NodePQueue.isEmpty()!=True):
        currentState = NodePQueue.pop()
        # print "h function: ", heuristic(currentState[0], problem)
        visitedNode.push(currentState)
        visitedNodeList.append(currentState[0])
        if problem.isGoalState(currentState[0]):
            #print "Goal Found"
            #print currentState
            break;

        successors = problem.getSuccessors(currentState[0])
        for element in successors:
            #print element
            element = (element[0], element[1], element[2]+currentState[2]+heuristic(element[0], problem)-heuristic(currentState[0], problem))
            if element[0] not in visitedNodeList and checkExistedNodePQueue(NodePQueue, element):
                NodePQueue.push(element, element[2])
                parents[element] = currentState
        #break
    path = util.Stack()
    path.push(currentState)

    while True:
        if currentState in parents:
            #print temp
            parent = parents[currentState]
            path.push(parent)
            currentState = parent
        else:
            break

    pathList = list()
    while (path.isEmpty()!=True):
        temp = path.pop()
        if temp[1] != 'Stop':
            pathList.append(temp[1])


    return pathList


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
