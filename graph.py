import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

files = [['seven_agents.csv', 'Seven Agents'],
         ['single_agent.csv', 'Single Agent'],
         ['twelve_agents.csv', 'Twelve Agents'],
         ['twentyfour_agents.csv', 'Twenty Four Agents']]


def create_plt_data(data):
    count = 0
    y = []
    x = []
    for d in data:
        if d[2] < 1:
            count += 1
        x.append(d[3])
        y.append(count)
    return x, y


def plot_csv_data(file_names):
    plt.figure()
    for f in file_names:
        data = pd.read_csv('./supervised_data/' + f[0], delimiter=';').to_numpy()
        x, y = create_plt_data(data)
        plt.plot(x, y, label=f[1])
    plt.title('Successful Throws Over Time')
    plt.xlabel('Time in seconds')
    plt.ylabel('Cumulative Successful Throws')
    plt.legend()
    plt.savefig('./fig/throw.svg')
    plt.savefig('./fig/throw.png')
    plt.show()


plot_csv_data(files)
