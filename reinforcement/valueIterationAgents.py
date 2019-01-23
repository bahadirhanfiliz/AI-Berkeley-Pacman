# valueIterationAgents.py
# -----------------------
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
    
# dis
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
        
        # V(i+1)(s) = arg max (a) T(s,a,s')[R(s,a,s') + discount * V(i)(s')] or
        # V(i+1)(s) = arg max (a) T(s,a,s')[R(s,a,s') + discount * arg max (a) q-Value(i)(s',a')] 
        # our case = V(i+1)(s) = arg max (s) computeQValueFromValues(state, action)
        # do this for number of iterations and start from V(0) = 0 of each state
       
        
        vStars = util.Counter()  # in order to make it same object as values, vStarts of each state
        
        for step in range(iterations):
            mdpStates = mdp.getStates()
            for state in mdpStates:
                vStarCandidates = []
                
                if (mdp.isTerminal(state)):
                    vStarCandidates.append(0)
                else:
                    PossibleActions = mdp.getPossibleActions(state)
                    for action in PossibleActions:
                        qValue = self.computeQValueFromValues(state, action)
                        vStarCandidates.append(qValue)
                        
                vStars[state] = max(vStarCandidates)
                
            self.values = vStars.copy()
            

            
            
        
        


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

# dis
    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        
        # * indicates fixed
        # Q(*s,a*) = T(s,a,s') [R(s,a,s') + discount * V(s')]
    
        transitionInfo = self.mdp.getTransitionStatesAndProbs(state, action)
        
#        print transitionInfo

        expectedQ = 0
        for possibleTransition in transitionInfo:
            nextPossibleState = possibleTransition[0]
            transitionProb = possibleTransition[1]
            iterationR = self.mdp.getReward(state, action, nextPossibleState) # each iterations R value
            iterationQ = transitionProb * (iterationR + self.discount * self.values[nextPossibleState])
            expectedQ = expectedQ + iterationQ
            
        return expectedQ
        
    
        util.raiseNotDefined()

# dis
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        # if terminal return None
        if (self.mdp.isTerminal(state)):
            return None
        else:
            possibleActions = self.mdp.getPossibleActions(state)
            
            currentMaxQ = - float("inf")
            currentBestAction = None
            for action in possibleActions:
                currentQ = self.computeQValueFromValues(state, action)
                if (currentQ > currentMaxQ):
                    currentMaxQ = currentQ
                    currentBestAction = action
                    
            return currentBestAction  # which is at the end optimal action
        
    
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
