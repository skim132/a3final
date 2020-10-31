import csv
from typing import List

from movie.domainmodels.movie import User


class UserFileCSVReader(object):
    def __init__(self, data_path):
        self._data_path = data_path
        self._users = list()

    @property
    def dataset_of_users(self) -> List[User]:
        self._read_csv_file()
        return self._users

    def _read_csv_file(self):
        with open(self._data_path, 'r') as csv_file:
            cur_users = csv.reader(csv_file, delimiter=',')
            for cur_user in cur_users:
                if cur_user and cur_user not in self._users:
                    self._users.append(User(cur_user[0], cur_user[1]))