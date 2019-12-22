import random
from datetime import datetime
import json
import math

import torch
import torch.random as tr
from types import SimpleNamespace
from socket import socket
from typing import Tuple

from csv_helper import CSVFile
from memory import ReplayMemory
from net import BasketballModel, SupervisedModel
from socket_server import SocketServer
from helpers import is_request, is_result, is_correct_message
from training_handler import TrainingHandler, Connection

tr.manual_seed(9)


class ModelServer(SocketServer):
    HOST = 'localhost'
    PORT = 5600

    def __init__(self, *args, **kwargs):
        self.model = BasketballModel()
        self.handler = TrainingHandler()
        self.status = 0
        self.last_connection_amount = 0
        self.running_time = datetime.now()
        self.memory = ReplayMemory(100000)
        self.csv = CSVFile()
        super(ModelServer, self).__init__(self.HOST, self.PORT)

    def on_message_received(self, sock: socket, data, received_data: str, addr: Tuple[str, int]) -> None:
        request = json.loads(received_data)
        print('Received {} from {}'.format(request, addr))
        if is_correct_message(request):
            host, prt = addr
            conn = self.handler.get_connection(prt)
            if is_result(request):
                res_throw = float(request['throw'])
                res_force = float(request['force'])
                res_distance = float(request['distance'])
                self.csv.add_observation(res_throw, res_force, res_distance,
                                         (datetime.now() - self.running_time).total_seconds())
                self.memory.push(res_throw, res_force, res_distance)
                conn.result = res_distance
            elif is_request(request):
                conn.distance = float(request['distance'])

    def on_step(self):
        # If all the results from the throws are in,
        if self.handler.all_results_are_in():
            # Then let us learn from all the results
            self.model.learn(self.handler.predictions, self.handler.get_all_results())
            # Clear the results so that we can receive fresh results
            self.handler.clear_results()
            del self.handler.predictions
            self.status = 0
        # If all the distances are in
        if self.handler.all_distances_are_in():
            # Then we can predict the force and height
            throws = self.model.throw(self.handler.get_all_distances())
            # PyTorch tries to be clever, but we need it in the right dimensions
            if len(throws.shape) <= 1:
                throws = throws.unsqueeze(0)
            # Add the predictions to the training handler for later
            self.handler.predictions = throws
            # And send them to all the connected clients
            for conn, throw in zip(self.handler.get_connections(), throws):
                # In order to send the tensor data over the network,
                # we must first convert the tensor to simple python
                # data types and then we can access them as normal.
                t = throw[0].tolist()
                # t = random.uniform(0.2, 1)
                self.send_prediction_to_connection(conn, t, t)
            # Clear distances afterwards
            self.handler.clear_distances()
            self.status = 1

    def on_connection_closed(self, addr: Tuple[str, int]):
        host, port = addr
        self.handler.remove_connection(port)

    def on_accept_connection(self, sock: socket, addr: Tuple[str, int], data: SimpleNamespace):
        host, port = addr
        self.handler.add_connection(Connection(sock, host, port, data))

    def send_prediction_to_connection(self, conn: Connection, force: float, height: float) -> None:
        prediction = {'Type': 'prediction', 'Force': force, 'Height': height}
        self.send_message(conn.data, prediction)

    def ask_for_distances(self, conn: Connection) -> None:
        request = {'Type': 'request'}
        self.send_message(conn.data, request)
