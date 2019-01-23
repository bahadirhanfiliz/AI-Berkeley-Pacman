# multiAgents.py
# --------------
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

        FoodPosList = newFood.asList()
        numberOfFoodLeft = len(FoodPosList)
        
        eatFoodWeight = -10 
        foodWeight = 5
        ghostWeight = -25

        
        # FoodScore
        foodDistScore = 0
        for eachFood in FoodPosList:
            foodDist = manhattanDistance(newPos, eachFood)
            if (foodDist != 0):
                foodDistScore = foodDistScore + 1.0/foodDist
                
        # GhostScore
        ghostDistScore = 0
        for eachGhostState in newGhostStates:
            position = eachGhostState.getPosition()
            ghostDist = manhattanDistance(newPos, position)
            if (ghostDist != 0):
                ghostDistScore = ghostDistScore + 1.0/ghostDist
            else:
                ghostDistScore = ghostDistScore + 500
                
        
        
        function = ( foodWeight * foodDistScore + eatFoodWeight  * numberOfFoodLeft                                  # chasing foods
        + ghostWeight * ghostDistScore  )                                             # running away from ghosts                           # hunting scared ghosts

        
        
        return function





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
        
#        Recursive algorithm that does dfs until depth node 
        numberOfAgents = gameState.getNumAgents()
        maxDepth = self.depth * numberOfAgents

        def miniMax(gameState, currentDepth):
            currentDepth = currentDepth + 1
            agentNo = currentDepth % numberOfAgents
            if (currentDepth == maxDepth or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState), None)
            if (agentNo == 0):
                check = (-float("Inf"), None)
                PacmanActions = gameState.getLegalActions(agentNo)
                
                for action in PacmanActions:
                    nextState = gameState.generateSuccessor(0, action)
                    value = miniMax(nextState, currentDepth)[0]
                    check = max(check, (value, action))
                return check
                    
            else:
                check = (float("Inf"), None)
                GhostActions = gameState.getLegalActions(agentNo)
                
                for action in GhostActions:
                    nextState = gameState.generateSuccessor(agentNo, action)
                    value = miniMax(nextState, currentDepth)[0]
                    check = min(check, (value, action))
                return check
                
    
        return miniMax(gameState, -1)[1]

        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        #        Recursive algorithm that does dfs until depth node 
        numberOfAgents = gameState.getNumAgents()
        maxDepth = self.depth * numberOfAgents

        def miniMax(gameState, currentDepth, alpha, beta):
            currentDepth = currentDepth + 1
            agentNo = currentDepth % numberOfAgents
            if (currentDepth == maxDepth or gameState.isWin() or gameState.isLose()):
                return (self.evaluationFunction(gameState), None)
            if (agentNo == 0):
                check = (-float("Inf"), None)
                PacmanActions = gameState.getLegalActions(agentNo)
                
                for action in PacmanActions:
                    nextState = gameState.generateSuccessor(0, action)
                    value = miniMax(nextState, currentDepth, alpha, beta)[0]
                    check = max(check, (value, action))
                    if (check[0] > beta):
                        return check
                    alpha = max(alpha, check[0])
                return check
                    
            else:
                check = (float("Inf"), None)
                GhostActions = gameState.getLegalActions(agentNo)
                
                for action in GhostActions:
                    nextState = gameState.generateSuccessor(agentNo, action)
                    value = miniMax(nextState, currentDepth, alpha, beta)[0]
                    check = min(check, (value, action))
                    if (check[0] < alpha):
                        return check
                    beta = min(beta, check[0])
                return check
                
    
        return miniMax(gameState, -1, -float("inf"), float("inf") )[1]


        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        numberOfAgents = gameState.getNumAgents()
        maxDepth = self.depth * numberOfAgents

        def miniMax(gameState, currentDepth):
            currentDepth = currentDepth + 1
            agentNo = currentDepth % numberOfAgents
            if (currentDepth == maxDepth or gameState.isWin() or gameState.isLose()):
                return [self.evaluationFunction(gameState), None]
            if (agentNo == 0):
                check = [-float("Inf"), None]
                PacmanActions = gameState.getLegalActions(agentNo)
                
                for action in PacmanActions:
                    nextState = gameState.generateSuccessor(0, action)
                    value = miniMax(nextState, currentDepth)[0]
                    check = max(check, [value, action])
                return check
                    
            else:
                check = [0, None]
                GhostActions = gameState.getLegalActions(agentNo)
                
                uniformProb = 1.0/len(GhostActions)
                
                for action in GhostActions:
                    nextState = gameState.generateSuccessor(agentNo, action)
                    value = miniMax(nextState, currentDepth)[0]
                    check[0] = check[0] + uniformProb * value
                return check
                
    
        return miniMax(gameState, -1)[1]
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <running away from ghosts, hunting scared ghosts, chasing power capsules>
    """
    "*** YOUR CODE HERE ***"

        

    # Useful information you can extract from a GameState (pacman.py)
    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curGhostStates = currentGameState.getGhostStates()
    for ghost in currentGameState.getGhostStates():
        if not ghost.scaredTimer:
          isScared = 0
        else: 
          isScared = 1


    FoodPosList = curFood.asList()
    numberOfFoodLeft = len(FoodPosList)
    CapsulePosList = currentGameState.getCapsules()
    numberOfPalletsLeft = len(currentGameState.getCapsules())
    numberOfGhostsLeft = len(currentGameState.getGhostStates())
    
    eatFoodWeight = -10 
    foodWeight = 5
    ghostWeight = -40
    ghostScaredWeight = 100
    capsuleWeight = 7
    eatPaletWight = -20
    eatGhostWight = -50

    
    # FoodScore
    foodDistScore = 0
    for eachFood in FoodPosList:
        foodDist = manhattanDistance(curPos, eachFood)
        if (foodDist != 0):
            foodDistScore = foodDistScore + 1.0/foodDist
            
    # GhostScore
    ghostDistScore = 0
    for eachGhostState in curGhostStates:
        position = eachGhostState.getPosition()
        ghostDist = manhattanDistance(curPos, position)
        if (ghostDist != 0):
            ghostDistScore = ghostDistScore + 1.0/ghostDist
        else:
            ghostDistScore = ghostDistScore + 500
            
    # PowerPalletScore
    capsuleDistScore = 0
    for eachCapsule in CapsulePosList :
        capsuleDist = manhattanDistance(curPos, eachCapsule)
        if (capsuleDist != 0):
            capsuleDistScore = capsuleDistScore + 1.0/capsuleDist
        else:
             capsuleDistScore = capsuleDistScore + 50
             

            
    
    
    function = ( foodWeight * foodDistScore + eatFoodWeight  * numberOfFoodLeft                                  # chasing foods
    + (1 - isScared) * ghostWeight * ghostDistScore                                 # running away from ghosts
    + isScared * ghostScaredWeight * ghostDistScore + numberOfGhostsLeft * eatGhostWight                             # hunting scared ghosts
    + (1 - isScared) * capsuleWeight * capsuleDistScore + numberOfPalletsLeft * eatPaletWight)

                                           # chasing power capsules                          # hunting scared ghosts

#    print isScared
    
    
    return function



        


    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

