import numpy as np

# TODO Things we need to define
# TODO 1. A set of states: Represents all the possible locations for the agent in the environment.
# TODO 2. A set of actions: Represents all the actions the agent can take at any given state.
# TODO 3. Transition probabilities: Represents the probability that the action the agent attempts will be successful
# TODO 4. Rewards: Values of arriving in a specific state
# TODO 5. Discount factor Gamma: Menat to diminish the value of future rewards compared to instant rewards

# * The goal of the agent in a Markov Decision Process is to find the optimal policy, which is the set of optimal actions
# * to take at any given state

all_states = []

GAMMA = 0.99
EPSILON = 0.05

rewards = {}

MAX_COL = 6
MAX_ROW = 6

walls = [(1,0), (4,1), (1,4), (2,4), (3,4)]
plus_one = [(0,0), (2, 0), (5,0), (3,1), (4,2), (5,3)]
minus_one = [(1,1), (5,1), (2,2), (3,3), (4,4)]

# MAX_COL = 4
# MAX_ROW = 3

# rewards = {}
# # Lecture notes example
# start = (0,2)
# walls = [(1, 1)]
# plus_one = [(3,0)]
# minus_one = [(3,1)]

def check_valid(col, row):
    return col >= 0 and col < MAX_COL and row >= 0 and row < MAX_ROW and (col, row) not in walls

def get_direction(action):
    if action == 'U': 
        return 0
    elif action == 'R': 
        return 1
    elif action == 'D':
        return 2
    elif action == 'L':
        return 3


def rotate(action, direction):
    if direction == 'L': 
        action -= 1 
    elif direction == 'R':
        action += 1

    if action == -1:
        action = 3
    else:
        action = action % 3

    if action == 0: 
        return 'U'
    elif action == 1: 
        return 'R'
    elif action == 2:
        return 'D'
    elif action == 3:
        return 'L'

def get_next_state(state, action):
    if action == 'U': 
        next = [state[0], state[1] - 1] # Row - 1 (up 1)
    if action == 'D': 
        next = [state[0], state[1] + 1] # Row + 1 (down 1)
    if action == 'L': 
        next = [state[0] - 1, state[1]] # Col - 1 (left 1)
    if action == 'R':
        next = [state[0] + 1, state[1]] # Col + 1 (right 1)

    if check_valid(next[0], next[1]):
        return next
    else:
        return state

for col in range(MAX_COL):
    for row in range(MAX_ROW):
        all_states.append((col, row))
        
# Set of states and rewards
for state in all_states:
    if state in walls:
        # Walls have no value
        rewards[state] = 0
    elif state in plus_one:
        # Assuming Reward for goal is +1
        rewards[state] = 1
    elif state in minus_one:
        # Asssuming Reward value for lava is -1
        rewards[state] = -1
    else:
        # Asssuming Reward for remaining white squares is -0.04
        rewards[state] = -0.04 

print(rewards)

 # Set of actions
actions = {}
print(type(actions))
for state in all_states:
    if state not in walls:
        col = state[0]
        row = state[1]
        actions[state] = []

        # Move Left
        if check_valid(col - 1, row):
            actions[state].append('L')
        # Move Right
        if check_valid(col + 1, row):
            actions[state].append('R')
        # Move Up
        if check_valid(col, row - 1):
            actions[state].append('U')
        # Move Down
        if check_valid(col, row + 1):
            actions[state].append('D')

print(f"Actions available")
for state, state_actions in actions.items():
    print(state)
    print(state_actions)

 # Transitional Probability
t_probability = {
    'U' : 0.8, # 80% probability of going up
    'L' : 0.1, # 10% probability of going left
    'R' : 0.1, # 10% probability of going right
    'D' : 0    # 0% probability of going down
}

# TODO Value Iteration Method

# Start by defining an initial policy
policy = {}
for state in actions.keys():
    policy[state] = None
print("Printing out Initial Policy ~")
print(policy)


# Define initial value function
V = {}
for state in all_states:
    if state in actions.keys():
        V[state] = 0

    if state in minus_one:
        V[state] = -1

    if state in plus_one:
        V[state] = 1    

print("Printing out Initial Values ~")
print(V)


# TODO Value Iteration Algorithm
iteration = 0
while True:
    print(f"Policy at iteration {iteration}")
    print(policy)
    biggest_change = 0
    for state in all_states:
        if state in policy:
            old_v = V[state]
            new_v = 0

            #print(f"Actions for {state} are: {actions[state]}")
            for action in actions[state]:
                #print(f"Printing state/action: {state}, {action}")
                
                # Transitional probability
                correct_action = get_next_state(state, action) # 80% g
                #print(f"0.1 chance of {rotate(get_direction(action), 'L')}")
                l_action = get_next_state(state, rotate(get_direction(action), 'L'))
                #print(f"0.1 chance of {rotate(get_direction(action), 'R')}")
                r_action = get_next_state(state, rotate(get_direction(action), 'R'))

                #print(f"Main: {correct_action}, Left: {l_action}, Righ: {r_action}")

                #print(f"Printing next: {next}")
                # Calculating the value
                next_state = tuple(correct_action)
                l_next_state = tuple(l_action)
                r_next_state = tuple(r_action)
                v = rewards[state] + (GAMMA * ((V[next_state] * 0.8) + V[l_next_state] * 0.1 + V[r_next_state] * 0.1))
                if v > new_v:
                    new_v = v
                    policy[state] = action
        
        # Save best of all actions for the state 
        V[state] = new_v
        biggest_change = max(biggest_change, np.abs(old_v - V[state]))
    
    # Check if good enough 
    if biggest_change < EPSILON:
        break
    iteration += 1
print(f"Printing final policy")
for state in policy:
    print(f"{state} : {policy[state]}")
