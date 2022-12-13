# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from valueIterationAgents import ValueIterationAgent
import random
import game
import util

class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

def scoreEvaluation(state):
    return state.getScore()

# class PacmanValueAgent(ValueIterationAgent):
#     "Exactly the same as ValueIterationAgent, but with different default parameters"

#     def __init__(self, mdp, discount = 0.9, iterations = 100, **args):
#         """
#         These default parameters can be changed from the pacman.py command line.
#         For example, to change the exploration rate, try:
#             python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

#         # alpha    - learning rate
#         # epsilon  - exploration rate
#         # gamma    - discount factor
#         # numTraining - number of training episodes, i.e. no learning after these many episodes
#         # """

#         # args['epsilon'] = epsilon
#         # args['gamma'] = gamma
#         # args['alpha'] = alpha
#         # args['numTraining'] = numTraining
#         # self.index = 0  # This is always Pacman

#         args['mdp'] = mdp
#         args['discount'] = discount
#         args['iterations'] = iterations
#         self.index = 0  # This is always Pacman
#         ValueIterationAgent.__init__(self, **args)

#     def getAction(self, state):
#         """
#         Simply calls the getAction method of valueIterationAgents and then
#         informs parent of action for Pacman.  Do not change or remove this
#         method.
#         """
#         action = ValueIterationAgent.getAction(self,state)
#         self.doAction(state,action)
#         return action
