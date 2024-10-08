
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):


    def getAction(self, gameState):
      
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    

    def getAction(self, gameState):
        
        print(f"Inside getAction")
        action, score = self.minimax(0, 0, gameState)  # Get the action and score for pacman (agent_index=0)
        print(f"action: {action} score: {score}")
        return action  # Return the action to be done as per minimax algorithm
        #util.raiseNotDefined()
    def minimax(self, curr_depth, agent_index, gameState):
        
        tmp = curr_depth
        indentation = "  " * curr_depth
        print(f"{indentation}Inside minimax------ curr_depth: {curr_depth} agent_index: {agent_index} ")
        # Roll over agent index and increase current depth if all agents have finished playing their turn in a move
        if agent_index >= gameState.getNumAgents():
            agent_index = 0
            curr_depth += 1
        # Return the value of evaluationFunction if max depth is reached
        if curr_depth == self.depth:
            return None, self.evaluationFunction(gameState)
        # Initialize best_score and best_action with None
        best_score, best_action = None, None
        if agent_index == 0:  # If it is max player's (pacman) turn
            for action in gameState.getLegalActions(agent_index):  # For each legal action of pacman
                # Get the minimax score of successor
                # Increase agent_index by 1 as it will be next player's (ghost) turn now
                # Pass the new game state generated by pacman's `action`
                next_game_state = gameState.generateSuccessor(agent_index, action)
                
                _, score = self.minimax(curr_depth, agent_index + 1, next_game_state)
                
                # Update the best score and action, if best score is None (not updated yet) or if current score is
                # better than the best score found so far
                if best_score is None or score > best_score:
                    best_score = score
                    best_action = action
                print(f"{indentation}curr_depth: {curr_depth} agent_index: {agent_index} action: {action} score:{score} best_score: {best_score}")
        else:  # If it is min player's (ghost) turn
            for action in gameState.getLegalActions(agent_index):  # For each legal action of ghost agent
                # Get the minimax score of successor
                # Increase agent_index by 1 as it will be next player's (ghost or pacman) turn now
                # Pass the new game state generated by ghost's `action`
                next_game_state = gameState.generateSuccessor(agent_index, action)
                
                _, score = self.minimax(curr_depth, agent_index + 1, next_game_state)
                print(f"{indentation}curr_depth: {curr_depth} agent_index: {agent_index} action: {action} score:{score} best_score: {best_score}")
                # Update the best score and action, if best score is None (not updated yet) or if current score is
                # better than the best score found so far
                if best_score is None or score < best_score:
                    best_score = score
                    best_action = action
        # If it is a leaf state with no successor states, return the value of evaluationFunction
        
        if best_score is None:
            return None, self.evaluationFunction(gameState)
        print(f"{indentation}Exit minimax------ curr_depth: {tmp} agent_index: {agent_index} best_action: {best_action} best_score: {best_score}")
        return best_action, best_score  # Return the best_action and best_score
    
class AlphaBetaAgent(MultiAgentSearchAgent):
   

    def getAction(self, gameState):
       
        def alphaBeta(state, depth, agentIndex, alpha, beta):
            if depth == self.depth * state.getNumAgents() or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None

            if agentIndex == 0:  # Pacman's turn (maximizer)
                value = float('-inf')
                action = None
                for a in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, a)
                    successorValue, _ = alphaBeta(successor, depth + 1, (agentIndex + 1) % state.getNumAgents(), alpha, beta)
                    if successorValue > value:
                        value = successorValue
                        action = a
                    alpha = max(alpha, value)
                    if value > beta:
                        return value, action
                return value, action
            else:  # Ghosts' turn (minimizers)
                value = float('inf')
                action = None
                for a in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, a)
                    successorValue, _ = alphaBeta(successor, depth + 1, (agentIndex + 1) % state.getNumAgents(), alpha, beta)
                    if successorValue < value:
                        value = successorValue
                        action = a
                    beta = min(beta, value)
                    if value < alpha:
                        return value, action
                return value, action

        _, bestAction = alphaBeta(gameState, 0, 0, float('-inf'), float('inf'))
        return bestAction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    

    def getAction(self, gameState):
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction