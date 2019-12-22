import csv
from os.path import isfile
from typing import Tuple, Union

from torch import Tensor


class CSVFile:

    FILE_NAME = 'throws.csv'

    def __init__(self):
        if not self.file_exists():
            self.add_row(['distance', 'force', 'result', 'datetime'])

    def add_row(self, data):
        with open(self.FILE_NAME, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows([data])

    def add_observation(self, distance: float, force: Union[float, Tensor], result: float, time):
        if isinstance(force, Tensor):
            if len(force.shape) == 1 and force.shape[0] == 1:
                force = force.tolist()[0]
            else:
                raise ValueError('Wrong force tensor shape {}'.format(force.shape))
        self.add_row([distance, force, result, time])

    def file_exists(self) -> bool:
        return isfile(self.FILE_NAME)
