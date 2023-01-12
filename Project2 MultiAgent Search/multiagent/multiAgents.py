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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    
    #return successorGameState.getScore()
    
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def min_max(gameState, depth, agent):
            if agent >= gameState.getNumAgents():
                agent = 0
                depth = depth + 1
            if (depth==self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            elif (agent == 0):
                return max_function(gameState, depth, agent)
            else:
                return min_function(gameState, depth, agent)

            
        def max_function(gameState, depth, agent):
            out = ["new", -float("inf")]
            pacActions = gameState.getLegalActions(agent)
            
            if not pacActions:
                return self.evaluationFunction(gameState)
                
            for actions in pacActions:
                current_state = gameState.generateSuccessor(agent, actions)
                current_value = min_max(current_state, depth, agent+1)
                if type(current_value) is list:
                    test_value = current_value[1]
                else:
                    test_value = current_value
                if test_value > out[1]:
                    out = [actions, test_value]                    
            return out
      

        def min_function(gameState, depth, agent):
            out = ["new", float("inf")]
            ghostActions = gameState.getLegalActions(agent)
            
            if not ghostActions:
                return self.evaluationFunction(gameState)
                
            for actions in ghostActions:
                current_state = gameState.generateSuccessor(agent, actions)
                current_value = min_max(current_state, depth, agent+1)
                if type(current_value) is list:
                    test_value = current_value[1]
                else:
                    test_value = current_value
                if test_value < out[1]:
                    out = [actions, test_value]
            return out
             
        list_op = min_max(gameState, 0, 0)
        return list_op[0]
    
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        def minval_fun(states, agent_index, depth, alpha, beta):
           
            num_agent = gameState.getNumAgents()
            legal_action = states.getLegalActions(agent_index)

            #if no legal actions,return the evaluation function
            if not legal_action:
                return self.evaluationFunction(states)

            min_val = 99999
            cur_beta = beta
           
            if agent_index == num_agent - 1:
                for act in legal_action:
                    min_val =  min(min_val, maxval_fun(states.generateSuccessor(agent_index, act), \
                    agent_index,  depth, alpha, cur_beta))
                    if min_val < alpha:
                        return min_val
                    cur_beta = min(cur_beta, min_val)

            else:
                for act in legal_action:
                    min_val =  min(min_val,minval_fun(states.generateSuccessor(agent_index, act), \
                    agent_index + 1, depth, alpha, cur_beta))
                    if min_val < alpha:
                        return min_val
                    cur_beta = min(cur_beta, min_val)

            return min_val

      #pacman max value function
        
        def maxval_fun(states, agent_index, depth, alpha, beta):
            
            agent_index = 0
            legal_action = states.getLegalActions(agent_index)

           
            if not legal_action  or depth == self.depth:
                return self.evaluationFunction(states)
            
            max_val = -99999
            cur_alpha = alpha

            for act in legal_action:
                max_val = max(max_val, minval_fun(states.generateSuccessor(agent_index, act), \
                agent_index + 1, depth + 1, cur_alpha, beta) )
                if max_val > beta:
                    return max_val
                cur_alpha = max(cur_alpha, max_val)
            return max_val


        actions = gameState.getLegalActions(0)
        alpha = -99999
        beta = 99999

        each_action = {}
        for act in actions:
            value = minval_fun(gameState.generateSuccessor(0, act), 1, 1, alpha, beta)
            each_action[act] = value

            #update alpha value
            if value > beta:
                return act
            alpha = max(value, alpha)

        return max(each_action, key=each_action.get)

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

      
        def expval_fun(states, agent_index, depth):
            num_agent = gameState.getNumAgents()
            legal_action = states.getLegalActions(agent_index)

            #if actions not legal then return the evaluation function
            if not legal_action:
                return self.evaluationFunction(states)
            exp_value = 0
            prob = 1.0 / len(legal_action) 
            for act in legal_action:
                if agent_index == num_agent - 1:
                    cur_expval =  maxval_fun(states.generateSuccessor(agent_index, act), \
                    agent_index,  depth)
                else:
                    cur_expval = expval_fun(states.generateSuccessor(agent_index, act), \
                    agent_index + 1, depth)
                exp_value += cur_expval * prob

            return exp_value


        #Pacman max function
        
        def maxval_fun(states, agent_index, depth):
        
            agent_index = 0
            legal_action = states.getLegalActions(agent_index)

            if not legal_action  or depth == self.depth:
                return self.evaluationFunction(states)

            max_val =  max(expval_fun(states.generateSuccessor(agent_index, act), \
            agent_index + 1, depth + 1) for act in legal_action)

            return max_val

        #maximizing the best moves for pacman at the rootnode
        
        actions = gameState.getLegalActions(0)
        
        #find all actions and the value. Return actions for max value
       
        each_action = {}
        for act in actions:
            each_action[act] = expval_fun(gameState.generateSuccessor(0, act), 1, 1)

        #returning action with best expectimax value
        return max(each_action, key=each_action.get)

        util.raiseNotDefined()
        
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    food_position = currentGameState.getFood().asList()
    food_distance = []
    ghost_states = currentGameState.getGhostStates()
    cap_pos = currentGameState.getCapsules()
    current_position = list(currentGameState.getPacmanPosition())

    for food in food_position:
        food_pac_dis = manhattanDistance(food, current_position)
        food_distance.append(-1 * food_pac_dis)

    if not food_distance:
        food_distance.append(0)

    return max(food_distance) + currentGameState.getScore()
    
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
