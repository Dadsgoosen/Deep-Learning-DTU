from torch import Tensor
from threading import Lock
from socket import socket
from types import SimpleNamespace
from typing import Optional, Dict, Union, List, Tuple


class Connection:

    def __init__(self, sock: socket, address: str, port: int, data: SimpleNamespace):
        self.port: int = port
        self.address: str = address
        self.sock: socket = sock
        self.data = data
        self.__result: Optional[float] = None
        self.__distance: Optional[float] = None
        self.__predictions: Optional[Tensor] = None

    @property
    def distance(self) -> Optional[float]:
        return self.__distance

    @distance.setter
    def distance(self, value: float):
        self.__distance = value
        print('Setting distance to {} for port {}'.format(value, self.port))

    @distance.deleter
    def distance(self):
        self.__distance = None

    def has_distance(self) -> bool:
        return self.__distance is not None

    @property
    def result(self) -> Optional[float]:
        return self.__result

    @result.setter
    def result(self, value: float):
        self.__result = float(value)
        print('Setting result to {} for port {}'.format(value, self.port))

    @result.deleter
    def result(self):
        self.__result = None

    def has_result(self) -> bool:
        return self.__result is not None


class TrainingHandler:

    def __init__(self):
        self.lock = Lock()
        self.connections: Dict[int, Connection] = {}
        self.__predictions: Optional[Tensor] = None

    @property
    def connection_amount(self) -> int:
        return len(self.connections.keys())

    @property
    def predictions(self):
        return self.__predictions

    @predictions.setter
    def predictions(self, value: Tensor):
        if not isinstance(value, Tensor):
            raise TypeError('Prediction parameter is not of type Tensor')
        self.__predictions = value

    @predictions.deleter
    def predictions(self):
        self.__predictions = None

    def has_predictions(self) -> bool:
        return self.__predictions is not None

    def get_connections(self) -> List[Connection]:
        return list(self.connections.values())

    def all_results_are_in(self) -> bool:
        self.lock.acquire()
        result = True if len(self.connections.keys()) > 0 else False
        for k, v in self.connections.items():
            if not v.has_result():
                result = False
                break
        self.lock.release()
        return result

    def all_distances_are_in(self) -> bool:
        self.lock.acquire()
        result = True if len(self.connections.keys()) > 0 else False
        for prt, conn in self.connections.items():
            if not conn.has_distance():
                result = False
                break
        self.lock.release()
        return result

    def get_all_results(self) -> List[float]:
        if not self.all_results_are_in():
            raise RuntimeError('Not all results are in')
        return [float(conn.result) for prt, conn in self.connections.items()]

    def get_all_distances(self) -> List[float]:
        if not self.all_distances_are_in():
            raise RuntimeError('Not all distances are in')
        return [float(conn.distance) for prt, conn in self.connections.items()]

    def clear_distances(self) -> None:
        self.lock.acquire()
        for k in self.connections.keys():
            del self.connections[k].distance
        self.lock.release()

    def clear_results(self) -> None:
        self.lock.acquire()
        for k in self.connections.keys():
            del self.connections[k].result
        self.lock.release()

    def add_connection(self, connection: Connection) -> None:
        self.lock.acquire()
        self.connections[connection.port] = connection
        self.lock.release()

    def remove_connection(self, connection: Union[int, Connection]) -> None:
        port: int = connection if isinstance(connection, int) else connection.port
        self.lock.acquire()
        del self.connections[port]
        self.lock.release()

    def get_connection(self, port: int) -> Connection:
        self.lock.acquire()
        conn = self.connections[port]
        self.lock.release()
        return conn
