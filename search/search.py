# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

from util import  Stack, Queue, PriorityQueue


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        
        returns : list of: successor, action, stepCost
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        
        returns : total scalar cost of list of actions
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

    

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    frontier1 = util.Stack()             # stacks nodes
    frontier2 = util.Stack()            # stacks actions
    isVisited = set()                # stores the visited nodes / used hash set for faster implementation
    root = problem.getStartState()      # where will the search start, we take that from problem class
    
    if (problem.isGoalState(root)):    # checks if search needed 
        #print("Start state is goal state!! No need for action!")
        return []                                       # if not needed then return empty list
    
    frontier1.push(root)            # add root to stack
    frontier2.push([])              # add initial path of [] to stack
    
    while not frontier1.isEmpty():
       
        node = frontier1.pop()
        path = frontier2.pop()
        
        if node not in isVisited:
            isVisited.add(node)                   # add isVisited in order not to visit again
        
            if (problem.isGoalState(node)):
            #print("Solution found!")
                return path                         # Solution found!
        
        
            for successor in problem.getSuccessors(node):
                frontier1.push(successor[0])
                frontier2.push(path + [successor[1]])
                
    
    #print("No solution is found!")
    return []
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    frontier1 = util.Queue()             # queues nodes
    frontier2 = util.Queue()            # queues actions
    isVisited = set()                # stores the visited nodes / used hash set for faster implementation
    root = problem.getStartState()      # where will the search start, we take that from problem class
    
    if (problem.isGoalState(root)):    # checks if search needed
       # print("Start state is goal state!! No need for action!")
        return []                                       # if not needed then return empty list
    
    frontier1.push(root)            # add root to queue
    frontier2.push([])              # add initial path of [] to queue
    
    while not frontier1.isEmpty():
       
        node = frontier1.pop()
        path = frontier2.pop()
        
        if node not in isVisited:
            isVisited.add(node)                   # add isVisited in order not to visit again
        
            if (problem.isGoalState(node)):
           # print("Solution found!")
               return path                         # Solution found!
        
        
            for successor in problem.getSuccessors(node):
                frontier1.push(successor[0])
                frontier2.push(path + [successor[1]])
                
    
   # print("No solution is found!")
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier1 = util.PriorityQueue()             # queue nodes
    frontier2 = util.PriorityQueue()            # stacks actions
    frontier3 = util.PriorityQueue()
    isVisited = set()                # stores the visited nodes / used hash set for faster implementation
    root = problem.getStartState()      # where will the search start, we take that from problem class
    
    if (problem.isGoalState(root)):    # checks if search needed
       # print("Start state is goal state!! No need for action!")
        return []                                       # if not needed then return empty list
    
    frontier1.push(root, 0)            # add root to queue
    frontier2.push([], 0)              # add initial path of [] to queue
    frontier3.push(0, 0)
    
    while not frontier1.isEmpty():
       
        node = frontier1.pop()
        path = frontier2.pop()
        cost = frontier3.pop()
        
        if node not in isVisited:
            isVisited.add(node)                   # add isVisited in order not to visit again
        
            if (problem.isGoalState(node)):
           # print("Solution found!")
                return path                         # Solution found!
        
        
            for successor in problem.getSuccessors(node):
                frontier1.push(successor[0], cost + successor[2])
                frontier2.push( (path + [successor[1]]), cost + successor[2])
                frontier3.push( cost + successor[2], cost + successor[2] )
                
    
    #print("No solution is found!")
    return []
    util.raiseNotDefined()
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    frontier1 = util.PriorityQueue()             # queue nodes
    frontier2 = util.PriorityQueue()            # stacks actions
    frontier3 = util.PriorityQueue()
    isVisited = set()                # stores the visited nodes / used hash set for faster implementation
    root = problem.getStartState()      # where will the search start, we take that from problem class
    
    if (problem.isGoalState(root)):    # checks if search needed
       # print("Start state is goal state!! No need for action!")
        return []                                       # if not needed then return empty list
    
    frontier1.push(root, 0)            # add root to queue
    frontier2.push([], 0)              # add initial path of [] to queue
    frontier3.push(0, 0)
    
    while not frontier1.isEmpty():
       
        node = frontier1.pop()
        path = frontier2.pop()
        cost = frontier3.pop()
        
        if node not in isVisited:
            isVisited.add(node)                   # add isVisited in order not to visit again
        
            if (problem.isGoalState(node)):
           # print("Solution found!")
                return path                         # Solution found!
        
        
            for successor in problem.getSuccessors(node):
                frontier1.push(successor[0], cost + successor[2] + heuristic(successor[0], problem))
                frontier2.push( (path + [successor[1]]), cost + successor[2] + heuristic(successor[0], problem))
                frontier3.push( cost + successor[2], cost + successor[2] + heuristic(successor[0], problem))
                
    
    #print("No solution is found!")
    return []
    util.raiseNotDefined()

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
