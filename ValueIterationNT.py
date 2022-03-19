import copy
import csv
import math
''' 
    Setting up problem
    Agent, Enviornment, State, Action, Reward
'''

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor

NUM_ACTIONS = 4
ACTIONS = [(-1,0), (0,-1), (1,0), (0,1)] # Up Left Down Right (WASD)

# Setting up initial Enviornment (row,column) format

# Lecture Example
START = None
REWARD = -0.04
GAMMA = 0.99
EPSILON = 10**(-2)

NUM_ROWS = 3
NUM_COLS = 4

good_reward = [(0,3)]
bad_reward = [(1,3)]
walls = [(1,1)]

# Assignment Example 1
START = (3,2)
REWARD = -0.04
# Gamma for sample output
# GAMMA = 0.94604
GAMMA = 0.99 
EPSILON = 10**(-2)

NUM_ROWS = 6
NUM_COLS = 6

good_reward = [(0,0), (0,2), (0,5), (1,3), (2,4), (3,5)]
bad_reward = [(1,1), (1,5), (2,2), (3,3), (4,4)]
walls = [(0,1), (1,4), (4,1), (4,2), (4,3)]

# Assignment Part 2
# REWARD = -0.04
# GAMMA = 0.99
# EPSILON = 10**(-2)

# NUM_ROWS = 6
# NUM_COLS = 6

# #START = None
# START = (5,5)
# good_reward = [(0,1), (0,4)]
# bad_reward = [(0,3), (1,1), (1,2), (1,3), (0,5), (4,4)]
# walls = [(4,1), (4,2), (4,3), (4,5), (2,0), (2,1), (2,2), (2,3), (2,4), (0,0), (0,2)]

environment = [ [0] * NUM_COLS for i in range(NUM_ROWS)]

for coord in good_reward:
    environment[coord[0]][coord[1]] = 1

for coord in bad_reward:
    environment[coord[0]][coord[1]] = -1

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
            elif START != None and (row,col) == START:
                val = "S" + " (" + ["U", "L", "D", "R"][policy[row][col]] + ")"
            elif (row, col) in good_reward:
                val = "+1" + " (" + ["U", "L", "D", "R"][policy[row][col]] + ")"
            elif (row, col) in bad_reward:
                val = "-1" + " (" + ["U", "L", "D", "R"][policy[row][col]] + ")"
            else:
                val = ["Up", "Left", "Down", "Right"][policy[row][col]]
            display += " " + val[:6].ljust(6) + " |"
        display += "\n"
    print(display)

# Get utility of the state reached after performing the given action from given state
def get_utility(environment, row, col, action):
    change_row, change_col = ACTIONS[action]
    new_row = row + change_row
    new_col = col + change_col

    if new_row < 0 or new_row >= NUM_ROWS or new_col < 0 or new_col >= NUM_COLS \
        or (new_row, new_col) in walls: # ! Collided with boundary or wall, no movement
        return environment[row][col]
    else:
        return environment[new_row][new_col]

# Get the utility of a state given an action and
def calculate_utility(environment, row, col, action):
    #utiltiy = REWARD
    
    if (row, col) in good_reward:
        utility = 1
    elif (row, col) in bad_reward:
        utility = -1
    else:
        utility = REWARD
    utility += 0.1 * GAMMA * get_utility(environment, row, col, (action - 1) % 4)
    utility += 0.8 * GAMMA * get_utility(environment, row, col, action)
    utility += 0.1 * GAMMA * get_utility(environment, row, col, (action + 1) % 4)

    return utility

def value_iteration(environment, isAnalyze):
    if isAnalyze:
        with open('vi_analysis.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Initial values are all 0
            for row in range(NUM_ROWS):
                    for col in range(NUM_COLS):
                        writer.writerow([f"({row},{col})", 0, 0])

            iteration = 1
            while True:
                print(f"Iteration {iteration}")

                next_env = copy.deepcopy(environment)
                error = 0
                for row in range(NUM_ROWS):
                    for col in range(NUM_COLS):
                        # Bellman update
                        next_env[row][col] = max([calculate_utility(environment, row, col, action) for action in range(NUM_ACTIONS)]) 
                        error = max(error, abs(next_env[row][col] - environment[row][col]))
                        writer.writerow([f"({row},{col})", iteration, truncate(next_env[row][col],3)])
                
                environment = next_env

                print_environment(environment)
                if error < EPSILON * (1 - GAMMA) / GAMMA:
                    break
                iteration += 1
    else:
        iteration = 1
        while True:
            print(f"Iteration {iteration}")

            next_env = copy.deepcopy(environment)
            error = 0
            for row in range(NUM_ROWS):
                for col in range(NUM_COLS):
                    # Bellman update
                    next_env[row][col] = max([calculate_utility(environment, row, col, action) for action in range(NUM_ACTIONS)]) 
                    error = max(error, abs(next_env[row][col] - environment[row][col]))
          
            environment = next_env

            print_environment(environment)
            if error < EPSILON * (1 - GAMMA) / GAMMA:
                break
            iteration += 1

    return environment

# Get the optimal policy from environment
def get_optimal_policy(environment):
    policy = [[-1] * NUM_COLS for i in range(NUM_ROWS)]

    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            # * No Terminal State, validate best action for all
            # if (row, col) in walls or (row,col) in good_reward or (row,col) in bad_reward: # ! Termination States
            #     continue

            # Select action that maximizes utility 
            max_action = None
            max_utility = -float("inf")

            for action in range(NUM_ACTIONS):
                utility = calculate_utility(environment, row, col, action)
                if utility > max_utility:
                    max_action = action
                    max_utility = utility
            policy[row][col] = max_action
    
    return policy

isAnalyze = True

if isAnalyze:
    with open('vi_analysis.csv', 'w', newline='') as file:
        writer = csv.writer(file)

print(environment)
print(f"Displaying initial policy")
print_environment(environment)

environment = value_iteration(environment, isAnalyze)

optimal_policy = get_optimal_policy(environment)

# Displaying the Optimal Policy
print(f"Optimal policy through Value Iteration is")
print_policy(optimal_policy)