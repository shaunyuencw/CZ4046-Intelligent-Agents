# Imports
from os import environ
import random
import copy

''' 
    Setting up problem
    Agent, Enviornment, State, Action, Reward
'''

NUM_ACTIONS = 4
ACTIONS = [(-1,0), (0,-1), (1,0), (0,1)] # Up Left Down Right (WASD)

# Lecture Example
# REWARD = -0.01
# GAMMA = 0.99
# EPSILON = 10**(-6)

# NUM_ROWS = 3
# NUM_COLS = 4

# good_reward = [(0,3)]
# bad_reward = [(1,3)]
# walls = [(1,1)]

# Assignment Part 1
REWARD = -0.04
GAMMA = 0.99
EPSILON = 10**(-3)

NUM_ROWS = 6
NUM_COLS = 6

good_reward = [(0,0), (0,2), (0,5), (1,3), (2,4), (3,5)]
bad_reward = [(1,1), (1,5), (2,2), (3,3), (4,4)]
walls = [(0,1), (1,4), (4,1), (4,2), (4,3)]

environment = [ [0] * NUM_COLS for i in range(NUM_ROWS)]

for coord in good_reward:
    environment[coord[0]][coord[1]] = 1

for coord in bad_reward:
    environment[coord[0]][coord[1]] = -1

# Start from random policy
policy = [[random.randint(0,3) for j in range(NUM_COLS)] for i in range(NUM_ROWS)]

# Start from fixed policy
#fixed_action = 0 # Up (0) Left (1) Down (2) Right (3) (WASD) 
#policy = [[fixed_action] * NUM_COLS for i in range(NUM_ROWS)]

# Prints out the current environment's utility values
def print_environment(environment):
    display = ""
    for row in range(NUM_ROWS):
        display += "|"
        for col in range(NUM_COLS):
            if (row, col) in walls:
                val = "WALL"
            elif (row, col) in good_reward:
                val = "+1"
            elif (row, col) in bad_reward:
                val = "-1"
            else:
                val = str(environment[row][col])
            display += " " + val[:5].ljust(5) + " |"
        display += "\n"
    print(display)

# Prints out the given policy (reccommended action at each state)
def print_policy(policy):
    display = ""
    for row in range(NUM_ROWS):
        display += "|"
        for col in range(NUM_COLS):
            if (row, col) in walls:
                val = "WALL"
            elif (row, col) in good_reward:
                val = "+1"
            elif (row, col) in bad_reward:
                val = "-1"
            else:
                val = ["Up", "Left", "Down", "Right"][policy[row][col]]
            display += " " + val[:5].ljust(5) + " |"
        display += "\n"
    print(display)

# Get utility of the state reached after performing the given action from given state
def get_utility(environment, row, col, action):
    change_row, change_col = ACTIONS[action]
    new_row = row + change_row
    new_col = col + change_col

    if new_row < 0 or new_row >= NUM_ROWS or new_col < 0 or new_col >= NUM_COLS or (new_row, new_col) in walls: # ! Collided with boundary or wall, no movement
        return environment[row][col]
    else:
        return environment[new_row][new_col] 

# Get the utility of a state given an action and
def calculate_utility(environment, row, col, action):
    utility = REWARD
    utility += 0.1 * GAMMA * get_utility(environment, row, col, (action - 1) % 4)
    utility += 0.8 * GAMMA * get_utility(environment, row, col, action)
    utility += 0.1 * GAMMA * get_utility(environment, row, col, (action + 1) % 4)

    return utility

# Performs evaluation of the current policy and make improvements if any
def policy_evaluation(policy, environment):
    error = 0
    while True:
        next_env = copy.deepcopy(environment)
        error = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                # ! With Terminal States
                if (row, col) in walls or (row,col) in good_reward or (row,col) in bad_reward:
                    continue
                
                next_env[row][col] = calculate_utility(environment, row, col, policy[row][col])
                error = max(error, abs(next_env[row][col] - environment[row][col]))

        environment = next_env
        if error < EPSILON * (1 - GAMMA) / GAMMA:
            break
    return environment
                
def policy_iteration(policy, environment):
    iteration = 1
    while True:
        
        environment = policy_evaluation(policy, environment)
        is_changed = False

        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                # ! With Terminal States
                if (row, col) in walls or (row,col) in good_reward or (row,col) in bad_reward:
                    continue
                max_action = None
                max_utility = -float("inf")
                for action in range(NUM_ACTIONS):
                    utility = calculate_utility(environment, row, col, action)
                    if utility > max_utility:
                        max_action = action
                        max_utility = utility
                    
                if max_utility > calculate_utility(environment, row, col, policy[row][col]):
                    policy[row][col] = max_action
                    is_changed = True

        print(f"Iteration {iteration}")
        print_policy(policy)
        
        if is_changed == False:
            break

        iteration += 1

    return policy

# Dispalying the Inital Policy
print(f"Displaying initial policy")
print_policy(policy)

# Policy Iteration
policy = policy_iteration(policy, environment)

# Displaying the Optimal Policy
print(f"Optimal policy through Policy Iteration is")
print_policy(policy)