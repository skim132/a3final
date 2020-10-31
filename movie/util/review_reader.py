import csv
from typing import List, Dict
class ReviewFileCSVReader(object):
    def __init__(self, data_path):
        self._data_path = data_path
        self._reviews = list()

    @property
    def dataset_of_reviews(self) -> List[Dict]:
        self._read_csv_file()
        return self._reviews

    def _read_csv_file(self):
        with open(self._data_path, 'r') as csv_file:
            reviews = csv.reader(csv_file, delimiter=',')
            for review in reviews:
                review_info = {'movie_id': review[1], 'username': review[2], 'rating': int(review[3]),
                               'comment': review[4], 'timestamp': float(review[5]), 'review_id': review[0]}
                self._reviews.append(review_info)