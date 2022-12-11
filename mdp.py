# mdp.py
# ------
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


import random
import util
import game
import pacman

# added, Sunni
import game
from game import GameStateData, Actions, Game
from pacman import GameState

EMPTY_LOCATION_REWARD = -0.04
FOOD_REWARD = 10
CAPSULE_REWARD = 100
GHOST_REWARD = -1000

GAMMA = 0.9
DANGER_ZONE_RATIO = 6
DANGER = 500
ITERATIONS = 10

class MarkovDecisionProcess:

    def __init__(self):
        self.map = self.walls = self.corners = None

    def getStates(self):
        """
        Return a list of all states in the MDP.
        Not generally possible for large MDPs.
        """
        # abstract
        # state = AgentState( self.start, self.isPacman )
        state = GameStateData(self)
        return state

    def getStartState(self):
        """
        Return the start state of the MDP.
        """
        # abstract
        return GameStateData.initialize() #, layout, numGhostAgents )
        

    def getPossibleActions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        # abstract
        # return [[-1, 0], [1, 0], [0, 1], [0, -1]] 
        # actions = Directions
        # return actions
        # Actions.getPossibleActions
        # return Actions
        return GameState.getLegalActions(state)


    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.

        Note that in Q-Learning and reinforcment
        learning in general, we do not know these
        probabilities nor do we directly model them.
        """
        # abstract
        return GameState.generateSuccessor(state,action)

    def getReward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.

        Not available in reinforcement learning.
        """
        # abstract
        position = util.nearestPoint(state.agentStates[0].Configuration.getPosition())

        if state._win:
            return 999
        elif state._lose:
            return -999
        elif state.food[position[0]][position[1]]:
            return 10
        else: # empty space
            return -0.1
        

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        # abstract
        # if Game.getProgress(self)
        return state._win or state._lose
