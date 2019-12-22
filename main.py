from model_server import ModelServer
from pickle import dump
from datetime import datetime
import torch

server = ModelServer()
server.start()


"""import pandas as pd

v1 = pd.read_csv('./data/throws.csv', delimiter=';')
v2 = pd.read_csv('./data/throws_v2.csv', delimiter=';')

counter_v1 = 0
counter_v2 = 0

for row in v1.to_numpy():
    if row[2] <= 0:
        counter_v1 += 1

for row in v2.to_numpy():
    if row[2] <= 0:
        counter_v2 += 1

print('lr 0.001: {}, lr 0.0001: {}'.format(counter_v1/len(v1), counter_v2/len(v2)))
"""
