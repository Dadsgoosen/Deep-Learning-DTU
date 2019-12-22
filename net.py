from typing import List
from matplotlib import pyplot as plt

import torch
import torch.utils.data as torch_data
import torch.nn as nn
import torch.optim as optim

import pandas as pd

import csv
import os

from torch.utils.data import DataLoader

from memory import ReplayMemory


class ThrowDataSet(torch_data.Dataset):

    def __init__(self, x, y):
        self.x = torch.tensor(x) if not isinstance(x, torch.Tensor) else x
        self.y = torch.tensor(y) if not isinstance(y, torch.Tensor) else y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class Net(nn.Module):

    def __init__(self):
        super().__init__()
        self.input = nn.Linear(in_features=1, out_features=1)
        self.hidden = nn.Linear(in_features=8, out_features=8)
        self.output = nn.Linear(in_features=1, out_features=1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.input(x))
        x = self.relu(self.hidden(x))
        return self.output(x)


class SupervisedModel:

    BATCH_SIZE = 8
    EPOCHS = 100

    def __init__(self):
        self.model: nn.Module = Net()
        self.criterion = nn.MSELoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.001)
        self.distances: torch.Tensor = None
        x, y = self.get_data()
        self.train(DataLoader(ThrowDataSet(x, y), self.BATCH_SIZE, True))

    def get_data(self):

        files = ['throws.txt']

        x = []
        y = []

        for file in files:
            data = pd.read_csv('./supervised_data/' + file, delimiter=';').to_numpy()
            for d in data:
                if d[0] == 0:
                    d_x: str = d[1]
                    d_x = d_x.replace(',', '.')
                    d_y: str = d[2]
                    d_y = d_y.replace(',', '.')
                    x.append([float(d_x)])
                    y.append([float(d_y)])

        return x, y

    def train(self, loader):

        plt.figure()
        loses = []

        for epoch in range(self.EPOCHS):
            running_loss = 0.0
            for i, data in enumerate(loader, 0):
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data
                # zero the parameter gradients
                self.optimizer.zero_grad()

                # forward + backward + optimize
                outputs = self.model(inputs)

                loss = self.criterion(outputs, labels)

                loss.backward()

                self.optimizer.step()

                # print statistics
                running_loss += loss.item()
            print("Loss: ", running_loss / self.BATCH_SIZE)
            loses.append(running_loss / self.BATCH_SIZE)
            running_loss = 0.0

        plt.plot(loses, label='Training')
        plt.grid(True)
        plt.title('Mean Squared Error Training Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig('supervised_loss.svg')

        torch.save(self.model.state_dict(), 'throw_model.pt')

    def throw(self, distances: List[float]) -> torch.Tensor:
        """
        Get height and force prediction
        :param distances: The distance to the goal
        :return: A list with the height and force respectively
        """
        distances = torch.tensor(distances, dtype=torch.float)
        distances = distances.unsqueeze(1)
        self.distances = distances
        return self.model(distances)

    def learn(self, predictions: torch.Tensor, results: List[float]):
        print(predictions, results)


class BasketballModel:
    """
    Handler for Net
    """
    FILE_NAME = 'model.pt'

    def __init__(self, should_load_state: bool = True):
        self.model: nn.Module = Net()
        self.distances: torch.Tensor = None
        self.criterion = nn.MSELoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.0001)
        self.memory = ReplayMemory(100000)
        if should_load_state:
            self.__load_model()
        self.model.train()

    def __load_model(self) -> None:
        """
        Load the model and optimizer states from the filesystem, if they exist.
        """
        if os.path.isfile(self.FILE_NAME):
            checkpoint = torch.load(self.FILE_NAME)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    def throw(self, distances: List[float]) -> torch.Tensor:
        """
        Get height and force prediction
        :param distances: The distance to the goal
        :return: A list with the height and force respectively
        """
        distances = torch.tensor(distances, dtype=torch.float)
        distances = distances.unsqueeze(1)
        self.distances = distances
        return self.model(distances)

    def learn(self, predictions: torch.Tensor, results: List[float]) -> None:
        """
        Perform a learning step from the accumulated results
        :param predictions: The predictions that let to the results
        :param results: The throw distance results
        """
        # Convert the results to a PyTorch tensor object
        results = torch.tensor(results).unsqueeze(1)
        # Debug, let's print the values
        print("Predictions: {}".format(predictions), "Results: {}".format(results))
        # Create a torch tensor from the results
        x = predictions
        # We add the predictions with the distance result as reinforcement
        y = x - results
        # get the inputs; data is a list of [inputs, labels]
        # zero the parameter gradients
        self.optimizer.zero_grad()
        # forward + backward + optimize
        outputs = self.model(y)
        loss = self.criterion(outputs, y)
        loss.backward()
        self.optimizer.step()
        print("Saving model with loss {}".format(loss))
        # Just to be safe we then save the new current state
        self.save()

    def save(self) -> None:
        """
        Save the model to file
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, self.FILE_NAME)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()
