from valueIterationAgents import ValueIterationAgent
import smallPacmanMDP

mdp = smallPacmanMDP.SmallPacmanMDP()

valueIterationAgent = ValueIterationAgent(mdp)

# print(valueIterationAgent.values)
# v = valueIterationAgent.values
# for val in v:
#     print(val)