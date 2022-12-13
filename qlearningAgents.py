# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        self.Qvalues = util.Counter()
        # you should be able to address self.Qvalues[(state,action)]
        ReinforcementAgent.__init__(self, **args)

# function call: python gridworld.py -a q -k 15

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        if (state,action) in self.Qvalues:
          return self.Qvalues[(state, action)]
        else:
          return 0.0


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"

        legalActions = self.getLegalActions(state)

        if len(legalActions)>0: # yes legal actions: in terminal state, use self.getLegalActions(state), returns legal actions for a state
          
          max_action_value = self.getQValue(state,legalActions[0])
          for i in legalActions:
            if max_action_value < self.getQValue(state,i):
              max_action_value = self.getQValue(state,i)

          return max_action_value

        else:
          return 0.0


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        # at every state, choose action that maximizes the Q-value from vector Qt

        legalActions = self.getLegalActions(state)
        check_all_equal = 0 # to check if all actions in QValue are the same. if so, randomize actions

        if len(legalActions)>0: # yes legal actions: in terminal state, use self.getLegalActions(state), returns legal actions for a state
          
          max_action = legalActions[0]
          for i in legalActions:
            if self.getQValue(state, max_action) < self.getQValue(state,i): # need to change
              max_action = i
            if self.getQValue(state,max_action) == self.getQValue(state,i):
              check_all_equal += 1
          
          # check if all actions in QValue are the same
          if check_all_equal == len(legalActions):
            max_action = random.choice(legalActions)
            
          return max_action

        else:
          return None

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        # print(f'state.direction')
        
        if len(legalActions)>0:
          if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
          else:
            action = self.computeActionFromQValues(state)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        # best_action_next = self.getValue(nextState) # same as self.computeValueFromQValues(nextState)
        best_action_next = self.computeValueFromQValues(nextState)
        
        self.Qvalues[(state,action)] = self.Qvalues[(state,action)] + self.alpha*(reward + self.discount*best_action_next - self.Qvalues[(state,action)])

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """

        # print(f'state: \n{state}')
        # print(f'state[0]: {state[0]}')

        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent): # using linear approximation: approximate Q values
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):

        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE (IN CODING ASSIGNMENT 3) ***"

        QValue = 0.0 
        w = self.weights
        feature = self.featExtractor.getFeatures(state, action)
        for i in feature:
          QValue += feature[i] * w[i]
        return QValue
      

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE (IN CODING ASSIGNMENT 3) ***"

        max_action = action
        for i in self.getLegalActions(nextState):
          if self.getQValue(nextState, max_action) < self.getQValue(nextState,i):
            max_action = i
 
        feature = self.featExtractor.getFeatures(state,action)

        for i in feature:
          self.weights[i] = self.weights[i] + self.alpha*(reward + self.discount*self.getQValue(nextState,max_action) - self.getQValue(state, action))*feature[i]
 


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE (IN CODING ASSIGNMENT 3, OPTIONAL) ***"
            pass
