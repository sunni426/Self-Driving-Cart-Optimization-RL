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

# import smallPacmanMDP as mdp
# import smallPacmanMDP as MDP
import util
import copy
import random


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
        self.runValueIteration() # added, Sunni

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        states = self.mdp.getStates()
        start_state = self.mdp.getStartState()
        current_state = start_state
        temp_counter = util.Counter()

        for i in range(self.iterations):

            # print(f'current_state: {current_state}')

            # below: commented out, Sunni
            oldvalues = copy.deepcopy(self.values) #create a copy of the values vector to be used in updating
            #                         # note that oldvalues = self.values doesn't work -- this results in
            #                         # oldvalues and self.values pointing to the same object
            # for s in states:
            #     max_val = float("-inf")
            #     for a in self.mdp.getPossibleActions(s):
            #         q_value = self.computeQValueFromValues(s,a)
            #         # print(f'q_value: {q_value}')
            #         if q_value > max_val:
            #             max_val = q_value
            #         temp_counter[s] = max_val
            #         print(f'temp_counter[s]: {temp_counter[s]}')
            # self.values = temp_counter

            if self.mdp.isTerminal(current_state):
                self.values = 0 # a terminal state has value zero

            else: #only non-terminal states are considered below

                possible_actions = self.mdp.getPossibleActions(current_state) 
                temp_value=-100000000 #really low number below the value function
                # print(f'possible actions: {possible_actions}')

                same_val_actions = []

                prev_action = possible_actions[0]

                for action in possible_actions: 

                    val_a = 0 # this variable will compute the value of each action
                    next_state = self.mdp.getTransitionStatesAndProbs(current_state, action)
                    # next is a set of pairs of next state + probabilities
                    reward = self.mdp.getReward(current_state,action,next_state)

                    # print(f'reward: {rew}')
                    val_a += (reward + self.discount * oldvalues[next_state]) # by end of this for, val_a is the value of taking action a
                    
                    if temp_value == val_a:
                        if prev_action not in same_val_actions:
                            same_val_actions.append(prev_action)
                        if action not in same_val_actions:
                            same_val_actions.append(action)
                        best_action = random.choice(same_val_actions)

                    elif val_a > temp_value:
                        temp_value = val_a # maximum computation
                        best_state = next_state
                        best_action = action
                    
                    # for sprime, prob in next:
                    #     rew = self.mdp.getReward(s,a,sprime)
                    #     val_a += prob*(rew+self.discount*oldvalues[sprime]) #by end of this for, val_a is the value of taking action a


                    prev_action = action

                self.values[current_state] = temp_value #at end of loops, update self.values

                print(f'state: \n{current_state}')
                print(f'action: {best_action}\n')

                current_state = best_state



                # print(f'value update: value = {temp_value}')
                    
    
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
        next = self.mdp.getTransitionStatesAndProbs(state, action)
        # print(next)



        reward = self.mdp.getReward(state,action,next)
        # print(f'action: {action}')
        # print(f'reward returned: {reward}\n')

        return reward

        # total = 0
        # for next_state, prob in action_prob_pairs:
        #     reward = self.getReward(state, action, next_state)
        #     total += prob * (reward + self.discount * self.values[next_state])
        # return total

        # next = mdp.getTransitionStatesAndProbs(state, action)
        # return mdp.getReward(next, action)

        # next = self.mdp.getTransitionStatesAndProbs(state, action)
        
        # answer = 0
        # for sprime, prob in next:
        #     rew = self.mdp.getReward(state,action,sprime)
        #     answer += prob*(rew + self.discount*self.values[sprime])
            
        # return answer
    

    def computeActionFromValues(self, state):
        """
        The policy is the best action in the given state
        according to the values currently stored in self.values.

        You may break ties any way you see fit.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        best_action = None
        val = float("-inf")
  
        if self.mdp.isTerminal(state):
            return None #return None if the state is terminal
        
        else: #only non-terminal states below here 
            possible_actions = self.mdp.getPossibleActions(state)
            
            #choose the first possible action and set it to be the action to be returned
            answer = possible_actions[0]
            val = self.computeQValueFromValues(state, answer)
            
            #next compute the action with the largest Q-value
            for a in possible_actions:
                val_a = self.computeQValueFromValues(state, a) 
                if val_a > val: 
                    val = val_a
                    best_action = a
            return best_action
       

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)



import smallPacmanMDP 
MDP = smallPacmanMDP.SmallPacmanMDP()
class PacmanValueAgent(ValueIterationAgent):
    "Exactly the same as ValueIterationAgent, but with different default parameters"

    def __init__(self, mdp = MDP, discount = 0.9, iterations = 100, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        # alpha    - learning rate
        # epsilon  - exploration rate
        # gamma    - discount factor
        # numTraining - number of training episodes, i.e. no learning after these many episodes
        # """


        # args['mdp'] = MDP
        # args['discount'] = discount
        # args['iterations'] = iterations
        self.index = 0  # This is always Pacman
        ValueIterationAgent.__init__(self, mdp=MDP, discount = 0.9, iterations = 100, **args)

    # def getAction(self, state):
    #     """
    #     Simply calls the getAction method of valueIterationAgents and then
    #     informs parent of action for Pacman.  Do not change or remove this
    #     method.
    #     """
    #     action = ValueIterationAgent.getAction(state)
    #     self.doAction(state,action)
    #     return action


