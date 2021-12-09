"""
main.py

The pyconcurrent entry point.

Usage:
(venv) user@mbp pyconcurrent % PYTHONPATH=./src python -m pyconcurrent.main --help
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, Future
from threading import Lock
from typing import Dict
from collections import defaultdict
import requests
from pyconcurrent.support import Timer
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


def _submit_request(url: str) -> int:
    """
    Submits a GET request to an endpoint, returning a HTTP response status code.

    :param url: The resource url
    :return: The HTTP status return code
    """
    response = requests.get(url)
    return response.status_code


def _result_callback(future: Future):
    """Records the API status code result"""
    try:
        status_code: int = future.result()
    except Exception as ex:
        logging.exception(ex)
    else:
        api_results.add_result(status_code)


def _run(worker_count: int, max_resource_id: int, base_url: str):
    """
    Runs the demo app with the specified worker and resource counts.

    :param worker_count: The number of workers used
    :param max_resource_id: The maximum resource id
    :param base_url: The base URL used to fetch resources
    """
    resource_ids = list(range(1, max_resource_id + 1))

    with ProcessPoolExecutor(max_workers=worker_count) as e:
        for resource_id in resource_ids:
            future = e.submit(_submit_request, f"{base_url}/{resource_id}")
            future.add_done_callback(_result_callback)


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
    logging.info("*****status code count*****")
    for k, v in api_results.items():
        logging.info(f"response code {k} = {v}")
    logging.info("*************************")
