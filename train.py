import pandas as pd
import numpy as np
import torch.utils.data as torch_data
import torch

from net import SupervisedModel

files = ['twentyfour_agents.csv', 'throws.csv', 'seven_agents.csv', 'single_agent.csv', 'twelve_agents.csv']

x = []
y = []

for file in files:
    data = pd.read_csv('./supervised_data/' + file, delimiter=';').to_numpy()
    for d in data:
        if d[2] < 1:
            d_x: str = d[0]
            d_x = d_x.replace(',', '.')
            d_y: str = d[1]
            d_y = d_y.replace(',', '.')
            x.append([float(d_x)])
            y.append([float(d_y)])


class ThrowDataSet(torch_data.Dataset):

    def __init__(self, x, y):
        self.x = torch.tensor(x)
        self.y = torch.tensor(y)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


dataset = ThrowDataSet(x, y)

loader = torch_data.DataLoader(dataset, 8, True)

model = SupervisedModel()

model.train(loader)
