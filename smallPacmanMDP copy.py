from torch import layout
import mdp
import util
from pacman import GameState
from layout import Layout
from game import GameStateData

EMPTY_LOCATION_REWARD = -0.04
FOOD_REWARD = 10
WIN_REWARD = 999
LOSE_REWARD = -999

class SmallPacmanMDP(mdp.MarkovDecisionProcess):

    def __init__(self):
        self.blank_layout = ['%%%%%%%', '%     %', '% %%% %', '% %.  %', '% %%% %', '%.    %', '%%%%%%%']
        self.foodPositions = [(3, 3), (5, 1)]

    def getStates(self):
        """
        Return a list of all states in the MDP.
        Not generally possible for large MDPs.
        """

        empty_spaces = []

        for i in range(len(self.blank_layout)):
            row = self.blank_layout[i]
            for j in range(len(row)):
                point = row[j]
                if point == ' ':
                    empty_spaces.append((i, j))

        states = []
        
        for pacman_space in empty_spaces:
            for ghost_space in empty_spaces:
                if ghost_space != pacman_space:

                    cur_layout = [list(string) for string in self.blank_layout]
                    
                    cur_layout[pacman_space[0]][pacman_space[1]] = 'P'
                    cur_layout[ghost_space[0]][ghost_space[1]] = 'G'

                    cur_layout = ["".join(chars) for chars in cur_layout]

                    state = GameState()

                    state.initialize(Layout(cur_layout), 1)

                    states.append(state)

        # for state in states:
        #     print(state)

        return states

    def getStartState(self):
        """
        Return the start state of the MDP.
        """
       
        layout_text = self.blank_layout
        l = Layout(layoutText=layout_text)
        print(f'l.width: {l.width}')
        print(f'l.food:\n{l.food}')

        state = GameStateData()
        start_state = GameStateData.initialize(state,layout=l, numGhostAgents=2)
        # print(f'state.layout: {state.layout}')
        print(f'start state: {start_state}')
        # return start_state

        print(f'state: {state}')

        return state

        # return GameState.initialize(layout=Layout(), numGhostAgents=2)
        # return GameStateData.initialize(Layout, Layout.getNumGhosts)
        

    def getPossibleActions(self, state):
        """
        Return list of possible actions from 'state'.
        """

        # return state.getLegalActions()
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

        newState = state.generatePacmanSuccessor(action)
        return newState

        # ghostActions = newState.getLegalActions(1)

        # nextStates = [newState.generateSuccessor(1, action) for action in ghostActions]

        # print(len(nextStates))
        # print(newState)
        
        # nextStateProb = 1/len(nextStates)

        # transitionStatesAndProbs = [[nextState, nextStateProb] for nextState in nextStates]
        # return [[newState, 1]]#transitionStatesAndProbs

    def getReward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.
        Not available in reinforcement learning.
        """

        position = nextState.getPacmanPosition()
        # print(f'position: {position}')
        # position = util.nearestPoint(state.agentStates[0].Configuration.getPosition())


        currentFood = state.getFood()
        for i in enumerate(currentFood):
            if i[1]==True:
                # print(f'currentFood at {i[0]}')
                print('')
       

        # if currentFood[position[0]][position[1]] == True:
        #     print('has food!')

        if state.isWin():
            return WIN_REWARD
        elif state.isLose():
            return LOSE_REWARD
        # elif state.hasFood(pacmanPosition[0], pacmanPosition[1]):
        elif currentFood[position[0]][position[1]] == True:
            # print(f'value increase food {FOOD_REWARD}')
            return FOOD_REWARD
        else: # empty space
            return EMPTY_LOCATION_REWARD

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """

        # return state.isWin() or state.isLose()
        return state._win or state._lose