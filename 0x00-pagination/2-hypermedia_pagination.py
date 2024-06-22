#!/usr/bin/env python3
"""
Replicate code from the previous task.

Implement a get_hyper method that takes the same arguments
(and defaults) as get_page and returns a dictionary containing
the following key-value pairs:
    - page_size: the length of the returned dataset page
    - page: the current page number
    - data: the dataset page (equivalent to return from previous task)
    - next_page: number of the next page, None if no next page
    - prev_page: number of the previous page, None if no previous page
    - total_pages: the total number of pages in the dataset as an integer
Make sure to reuse get_page in your implementation.

You can use the math module if necessary.
"""
from typing import Tuple, List, Dict, Union
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    returns a tuple of size two containing a
    start index and an end index corresponding to the range of indexes to
    return in a list for those particular pagination parameters.
    """
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        return the appropriate page of the dataset
        """
        assert type(page) is int
        assert page > 0
        assert type(page_size) is int
        assert page_size > 0
        start, end = index_range(page=page, page_size=page_size)
        data = self.dataset()
        if start > len(data):
            return []
        if (start + end) >= len(data):
            return data[start:]
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        returns a dictionary containing
        the following key-value pairs:
            - page_size: the length of the returned dataset page
            - page: the current page number
            - data: the dataset page (equivalent to return from previous task)
            - next_page: number of the next page, None if no next page
            - prev_page: number of the previous page, None if no previous page
            - total_pages: the total number of pages
                in the dataset as an integer
        """
        assert type(page) is int
        assert page > 0
        assert type(page_size) is int
        assert page_size > 0
        _dict = {}
        start, end = index_range(page=page, page_size=page_size)
        dataset = self.dataset()
        dataset_len = len(dataset)
        if start >= dataset_len:
            data = []
        elif (start + end) >= dataset_len:
            data = dataset[start:]
        else:
            data = dataset[start:end]

        total_pages = math.ceil(dataset_len / page_size)

        _dict['page_size'] = len(data)
        _dict['page'] = page
        _dict['data'] = data
        _dict['next_page'] = None if total_pages - page <= 0 else page + 1
        _dict['prev_page'] = None if page == 1 else page - 1
        _dict['total_pages'] = total_pages

        return _dict
