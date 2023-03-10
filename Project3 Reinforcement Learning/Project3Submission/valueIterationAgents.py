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
import collections

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
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            count = util.Counter()
            get_states = self.mdp.getStates()
            for state in get_states:
                if self.mdp.isTerminal(state): #check for terminal state
                    count[state] = 0  #value of the terminal state is zero
                else:
                    max_val = -99999   
                    poss_actions = self.mdp.getPossibleActions(state) #get actions for the state 
                    for action in poss_actions:
                        trans_prob = self.mdp.getTransitionStatesAndProbs(state,action) #getting transition state and prob using the defined method
                        value = 0
                        for t in trans_prob:
                            value += t[1] * (self.mdp.getReward(state,action,t[1]) + self.discount * self.values[t[0]])
                        max_val = max(value,max_val) #updating the maximum value by taking a max of prev and new value
                    if max_val != -99999:
                        count[state] = max_val
            
            self.values = count

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

        q_val = 0
        for t in self.mdp.getTransitionStatesAndProbs(state,action):
            q_val += t[1] * (self.mdp.getReward(state,action,t[1]) + self.discount * self.values[t[0]])

        return q_val

        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        #checking for terminal state
        if self.mdp.isTerminal(state):
            return None
        
        #finding actions and their values 
        poss_actions = self.mdp.getPossibleActions(state)
        all_action = {}
        for action in poss_actions:
            all_action[action] = self.computeQValueFromValues(state,action)

        #return action that has the max value
        return max(all_action,key=all_action.get)
        
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        get_states = self.mdp.getStates()
        num_states = len(get_states)

        for i in range(self.iterations):
            state = get_states[i % num_states]
            if not self.mdp.isTerminal(state):
                poss_actions = self.mdp.getPossibleActions(state)
                for action in poss_actions:
                    max_val = max([self.getQValue(state,action)])
                    self.values[state] = max_val

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        queue = util.PriorityQueue()
        prev_values = {}
        get_states = self.mdp.getStates()

        #finding all predecessors using loop
        for state in get_states:
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for t in self.mdp.getTransitionStatesAndProbs(state, action):
                        if t[0] in prev_values:
                            prev_values[t[0]].add(state)
                        else:
                            prev_values[t[0]] = {state}


        for state in get_states:
            if not self.mdp.isTerminal(state):
                diff = abs(self.values[state] - max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)]))
                #pushing negative into queue
                queue.update(state, -diff)

        for iteration in range(self.iterations):
            if queue.isEmpty():
                break
            state = queue.pop()
            if not self.mdp.isTerminal(state):
                self.values[state] = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])

            for p in prev_values[state]:
                if not self.mdp.isTerminal(p):
                    diff = abs(self.values[p] - max([self.computeQValueFromValues(p, action) for action in self.mdp.getPossibleActions(p)]))

                    if diff > self.theta:
                            queue.update(p, -diff)
