# Author: Zulfadli Zainal
# Github: https://github.com/zulfadlizainal
# Linkedin: https://linkedin.com/in/zulfadlizainal

import pandas as pd
import matplotlib.pyplot as plt

# Import RE Count Table

df_RE_Count = pd.read_excel('RE_Count.xlsx', index_col=0)

# Input SI RE Size (Assumptions: 1008 RE to 2016 RE)

sib_size = 0
while 1008 > sib_size or 2016 < sib_size:
    try:
        sib_size = int(input("Size of SI RE (1008 RE to 2016 RE): "))
    except ValueError:
        print('Not an Integer')

# Create Info Table

df_RE_Count_display = df_RE_Count.drop(
    ['Slots/Subframe', 'Slots/Frame', 'Normal CP Symbol/Frame', 'Normal CP RE/Frame/RB'], axis=1, inplace=False)

# Print Resource Configurations

print(' ')
print('### List of RE Configurations ###')
print(' ')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_RE_Count_display)

print(' ')
print('### End of List ###')
print(' ')

# Input Resource Configurations (No 1 to 36)

config = 0
while 1 > config or 36 < config:
    try:
        config = int(input("Resource Configurations (1 to 36): "))
    except ValueError:
        print('Not an Integer')

# Selected Resources

select = df_RE_Count.loc[config, 'Normal CP RE/Frame']
select_config = df_RE_Count.loc[config, 'ID']

# Prepare Result Grid (RMSI - SIB1)

no_of_beams = [1, 2, 4, 8, 16, 32, 64]
si_periodicity_ms = [20]

max_beams = max(no_of_beams)

df_si_occupancy = pd.DataFrame(no_of_beams, columns=['No of Beams'])

i = 0
index = 0

for index in range(len(si_periodicity_ms)):

    l = no_of_beams[i]                         # L = No of beams

    for index in range(len(si_periodicity_ms)):

        for index in range(len(si_periodicity_ms)):

            if i < len(si_periodicity_ms):

                if l <= max_beams:

                    df_si_occupancy[f'RMSI Periodicity (SIB1) = {si_periodicity_ms[i]} ms'] = ((
                        ((sib_size) / (si_periodicity_ms[i]/10)) * df_si_occupancy['No of Beams'])/select)*100

                    l = no_of_beams[i]

                else:
                    None

            else:
                None

    i = i+1

print(df_si_occupancy)

# Plot Result

df_si_occupancy.plot.bar(x='No of Beams', y='RMSI Periodicity (SIB1) = 20 ms')

plt.xlabel("No of Beams")
plt.ylabel("Occupancy (%)")
plt.title(f'\n RMSI Occupancy / Frame % (SIB1 NR)\n Assume SIB1 Size = {sib_size} RE \n FR_SCS_BW = {select_config} \n')
plt.legend()
plt.grid()

plt.show()