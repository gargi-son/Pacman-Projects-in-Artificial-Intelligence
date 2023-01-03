# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    frontier=util.Stack()  #storing stack in variable frontier
    explored_nodes=[] #creating a list to store explored states 

    frontier.push((problem.getStartState(),[])) #pushing the start state in the frontier


    while not frontier.isEmpty():  #running the while loop till the frontier is not empty
        p,q=frontier.pop()      #removing the last node in and putting in variables
        if p not in explored_nodes:  #check if p is already explored
            explored_nodes.append(p)  #adding p to explored state, if not already present
            if problem.isGoalState(p):  #doing the goal state test and returning q back
                return q
            else:
                next_node=problem.getSuccessors(p)  #if not the goal state, expand the node with the getSuccessors method
                for r,s,t in next_node:   #use a for loop to iterate through the next states 
                    new=q+[s]
                    frontier.push((r,new))  #pushing the values in the stack.
    return q
  
   # util.raiseNotDefined()




def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    frontier=util.Queue()   #storing queue in variable frontier
    explored_nodes=[]    #creating a list to store explored states 

    first_node=(problem.getStartState(),[],0)  #assigning the start state to a variable
    frontier.push(first_node)  #pushing the varibale in the queue frontier


    while not frontier.isEmpty():  #running the while loop till the frontier is not empty
        p,q,r=frontier.pop()     #removing the last node in and putting in variables
        if p not in explored_nodes:   #check if p is already explored
            explored_nodes.append(p)    #adding p to explored state, if not already present
            if problem.isGoalState(p):   #doing the goal state test and returning q back
                return q
            else:
                next_node=problem.getSuccessors(p)  #if not the goal state, expand the node with the getSuccessors method
                 
                for x,y,z in next_node:  #use a for loop to iterate through the next states
                    new=q+[y]
                    nc=r+z
                    frontier.push((x,new,nc))
    return q
    
   # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"


    frontier=util.PriorityQueue()
    visited_nodes={}
    first_node=(problem.getStartState(),[],0)

    frontier.push(first_node,0)

    while not frontier.isEmpty():
        p,q,r = frontier.pop()
        if(p not  in visited_nodes) or (r<visited_nodes[p]):
            visited_nodes[p]=r

            if problem.isGoalState(p):
                return q
            else:
                next_node=problem.getSuccessors(p)
                for x,y,z in next_node:
                    np=q+[y]
                    nc=r+z
                    frontier.update((x,np,nc),nc)
    return q
    

   
 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

   
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    
    frontier=util.PriorityQueue()  
    visited_nodes=[]
    first_node=(problem.getStartState(),[],0)
    frontier.push(first_node,0)

    while not frontier.isEmpty():
        p,q,r=frontier.pop()
        node=(p,r)
        visited_nodes.append((p,r))

        if problem.isGoalState(p):
            return q
        else:
            next_state=problem.getSuccessors(p)

            for x,y,z in next_state:
                n1=q+[y]
                node_cost=problem.getCostOfActions(n1)
                put_node=(x,n1,node_cost)
                checked=False
                for i in visited_nodes:
                    est,ect=i

                    if (x == est) and (node_cost>= ect):
                        checked = True 
                    if not checked:
                        frontier.push(put_node,node_cost+heuristic(x,problem))
                        visited_nodes.append((x,node_cost))

        return q

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
