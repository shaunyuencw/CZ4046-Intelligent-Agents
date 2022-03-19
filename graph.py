#%%
from email.mime import audio
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

value_headers = ['State', 'Iteration', 'Utility']
policy_headers = ['State', 'Iteration', 'Action', 'Utility']

value_df = pd.read_csv('vi_analysis.csv', names = value_headers, index_col='State')
policy_df = pd.read_csv('pi_analysis.csv', names = policy_headers, index_col='State')
#%%
# Select state to analyze (row,col)
state = "(0,1)"
value_state_df = value_df.loc[state]
policy_state_df = policy_df.loc[state]

print(value_state_df)

#%%
value_fig, ax1 = plt.subplots()

iter = value_state_df['Iteration']
util = value_state_df['Utility']


ax1.set_xlabel('Iteration')
ax1.set_ylabel('Utility')
ax1.set_ylim(0,100)
color = 'tab:blue'
ax1.plot(iter, util, color=color, label='Utility Value')

plt.title(f"(VI) Iteration to utility function for State {state}")
plt.show()

#%%

policy_fig, ax1 = plt.subplots()

iter = policy_state_df['Iteration']

util = policy_state_df['Utility']
action = policy_state_df['Action']

ax1.set_xlabel('Iteration')

ax1.xaxis.set_major_locator(tck.MultipleLocator(1))
ax1.set_ylabel('Utility')
color = 'tab:blue'
ax1.set_ylim(0,110)
ax1.plot(iter, util, color=color, label='Utility Value')

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('Action')
ax2.set_ylim(-1,4)
ax2.yaxis.set_major_locator(tck.MultipleLocator(1))
ax2.plot(iter, action, color=color, label='Action')

plt.title(f"(PI) Iteration to utility function for state {state}")
plt.show()

# %%

# %%
