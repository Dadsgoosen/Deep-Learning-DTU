from itertools import islice, chain
from typing import List

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def iter_chunks(seq, chunk_size):
    it = iter(seq)
    while True:
        chunk = list(islice(it, chunk_size))
        if chunk:
            yield chunk
        else:
            break


def mean_result(data: List[float], amount: int = 8):
    results = []
    for ite in iter_chunks(data, amount):
        results.append(np.mean(np.array(ite)))
    return results


d_1c_0001 = pd.read_csv('./rl/throws_1c_0.0001.csv', delimiter=';').to_numpy()
d_1c_001 = pd.read_csv('./rl/throws_1c_0.001.csv', delimiter=';').to_numpy()
d_8c_001 = pd.read_csv('./rl/throws_8c_0.001.csv', delimiter=';').to_numpy()
d_r_8c_001 = pd.read_csv('./rl/throws_r_8c_0.001.csv', delimiter=';').to_numpy()
d_r_4c_0001 = pd.read_csv('./throws.csv', delimiter=';').to_numpy()

plt.figure(1)
plt.plot(d_1c_0001[:, 2], label='Model A', zorder=4, color='#558B2F')
plt.plot(d_1c_001[:, 2], label='Model B', zorder=3, color='#FF5722')
plt.plot(mean_result(d_8c_001[:, 2]), label='Model C', zorder=1, color='#FF9800')
plt.plot(mean_result(d_r_8c_001[:2400, 2]), label='Model D', zorder=1, color='#4CAF50')
plt.plot(mean_result(d_r_4c_0001[:, 2], 4), label='Model F', zorder=0)
plt.grid(True)
plt.title('Reinforcement Learning Training Performance')
plt.xlabel('Throw')
plt.ylabel('Throw Result')
plt.legend()
plt.savefig('rl_training.svg')
plt.show()






