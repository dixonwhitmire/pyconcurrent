"""
support.py

Convenience and utility methods.
"""
import time


class Timer:
    """
    Context manager which measures elapsed time
    """

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed_time = self.end - self.start


def create_id_lists(max_id: int, list_count: int):
    """
    Creates a specific number of sequential id lists.
    Each list is equally sized unless the max_id is not evenly divisible by the list_count.
    If the max_id is not evenly divisible by the list_count, an additional list is created to store the remaining
    values.

    Example:
        l = create_id_lists(5000, 5) # creates 5 lists
        l = create_id_lists(5000, 6) # creates 7 lists


    :param max_id: The maximum id value/ceiling used.
    :param list_count: The number of lists to generate.
    """
    resource_lists = []
    entries_per_list = max_id // list_count
    remaining_count = max_id - (entries_per_list * list_count)

    starting_index = 1
    for i in range(1, list_count + 1):
        ending_index = i * entries_per_list
        resource_lists.append(list(range(starting_index, ending_index + 1)))
        starting_index = ending_index + 1

    if remaining_count:
        starting_index = resource_lists[-1][-1] + 1
        ending_index = starting_index + remaining_count
        resource_lists.append(list(range(starting_index, ending_index)))

    return resource_lists
