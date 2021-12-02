"""
main.py

The pyconcurrent entry point.

Usage:
(venv) user@mbp pyconcurrent % PYTHONPATH=./src python -m pyconcurrent.main --help
"""
import argparse
from threading import Thread, Lock
from typing import List, Dict
from collections import defaultdict
import requests
from pyconcurrent.support import create_id_lists, Timer
import logging

logger = logging.getLogger(__name__)


class ApiResults:
    """
    Stores API processing results.
    """

    def __init__(self):
        self.results: Dict = defaultdict(int)

    def add_result(self, status_code: int):
        """
        Adds a processing result to the cached results.
        Holds a lock while the result is added.

        :param status_code: The response status code
        """
        with Lock():
            self.results[status_code] += 1

    def __str__(self):
        return self.results.__str__()

    def __repr__(self):
        return self.results.__repr__()

    def items(self):
        return self.results.items()


api_results = ApiResults()


def _parse_args():
    """Returns the CLI arguments for pyconcurrent"""

    parser = argparse.ArgumentParser(description="pyconcurrent CLI")

    parser.add_argument(
        "-w",
        "--workers",
        help="defines the number of workers used for the demo",
        type=int,
        default=5,
    )
    parser.add_argument(
        "-r", "--resourceid", help="the max photo resource id", default=100, type=int
    )
    parser.add_argument(
        "-u",
        "--url",
        help="the base url used to fetch resources",
        default="https://jsonplaceholder.typicode.com/photos",
        type=str,
    )
    return parser.parse_args()


def _submit_requests(url: str, resource_ids: List):
    """
    Submits GET requests to an API endpoint.

    :param url: The base API resource url
    :param resource_ids: The list of resource ids
    """
    for resource_id in resource_ids:
        response = requests.get(f"{url}/{resource_id}")
        api_results.add_result(response.status_code)


def _run(worker_count: int, max_resource_id: int, base_url: str):
    """
    Runs the demo app with the specified worker and resource counts.

    :param worker_count: The number of workers used
    :param max_resource_id: The maximum resource id
    :param base_url: The base URL used to fetch resources
    """
    work_lists = create_id_lists(max_resource_id, worker_count)
    threads: List[Thread] = []

    for i, wl in enumerate(work_lists):
        t = Thread(
            name=f"pyconcurrent-thread-{i}",
            target=_submit_requests,
            args=(base_url, wl),
        )
        t.start()
        logging.info(f"starting thread {t.name}")
        threads.append(t)

    for t in threads:
        logging.info(f"joining thread {t.name}")
        t.join()


if __name__ == "__main__":

    with Timer() as t:
        args = _parse_args()
        logging.info("Starting pyconcurrent with the following options . . . ")
        logging.info(f"workers = {args.workers}")
        logging.info(f"resourceid = {args.resourceid}")
        logging.info(f"url = {args.url}")

        _run(args.workers, args.resourceid, args.url)

    logging.info("results ***********************")
    logging.info(f"elapsed time {t.elapsed_time}")
    for k, v in api_results.items():
        logging.info(f"response code {k} = {v}")
