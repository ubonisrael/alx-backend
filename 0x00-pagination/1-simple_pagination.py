#!/usr/bin/env python3
"""
Implement a method named get_page that takes two integer
arguments page with default value 1 and page_size with default value 10.
- You have to use this CSV file
    (same as the one presented at the top of the project)
- Use assert to verify that both arguments are
    integers greater than 0.
- Use index_range to find the correct indexes to paginate the
    dataset correctly and return the appropriate page of the dataset
    (i.e. the correct list of rows).
- If the input arguments are out of range for the dataset, an empty list
    should be returned.
"""
from typing import Tuple, List
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
        if start >= len(data):
            return []
        if (start + end) >= len(data):
            return data[start:]
        return data[start:end]
