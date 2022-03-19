import copy
''' 
    Setting up problem
    Agent, Enviornment, State, Action, Reward
'''

NUM_ACTIONS = 4
ACTIONS = [(-1,0), (0,-1), (1,0), (0,1)] # Up Left Down Right (WASD)

# Setting up initial Enviornment (row,column) format

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
EPSILON = 10**(-6)

NUM_ROWS = 6
NUM_COLS = 6

good_reward = [(0,0), (0,2), (0,5), (1,3), (2,4), (3,5)]
bad_reward = [(1,1), (1,5), (2,2), (3,3), (4,4)]
walls = [(0,1), (1,4), (4,1), (4,2), (4,3)]

# Assignment Part 2
# REWARD = -0.04
# GAMMA = 0.99 
# EPSILON = 10**(-6)

# NUM_ROWS = 6
# NUM_COLS = 6

# #START = None
# START = (5,5)
# good_reward = [(0,1), (0,4)]
# bad_reward = [(0,3), (0,5), (4,4)]
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

def value_iteration(environment):
    iteration = 1
    template = copy.deepcopy(environment)
    while True:
        print(f"Iteration {iteration}")

        next_env = copy.deepcopy(template)
        error = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                # * With Termination States
                if (row, col) in walls or (row,col) in good_reward or (row,col) in bad_reward: # ! Termination States
                    continue
                next_env[row][col] = max([calculate_utility(environment, row, col, action) for action in range(NUM_ACTIONS)]) # Bellman update
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
            #! No action if terminal state
            if (row, col) in walls or (row,col) in good_reward or (row,col) in bad_reward: # ! Termination States
                continue
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

print(environment)
print(f"Displaying initial policy")
print_environment(environment)

environment = value_iteration(environment)

optimal_policy = get_optimal_policy(environment)

# Displaying the Optimal Policy
print(f"Optimal policy through Value Iteration is")
print_policy(optimal_policy)