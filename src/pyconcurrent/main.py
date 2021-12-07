"""
main.py
The pyconcurrent entry point.
Usage:
(venv) user@mbp pyconcurrent % PYTHONPATH=./src python -m pyconcurrent.main --help
"""
import argparse
from typing import List, Dict
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
        :param status_code: The response status code
        """
        self.results[status_code] += 1

    def __str__(self):
        return self.results.__str__()

    def __repr__(self):
        return self.results.__repr__()

    def __len__(self):
        return len(self.results)

    def items(self):
        return self.results.items()




api_results = ApiResults()


def _parse_args():
    """Returns the CLI arguments for pyconcurrent"""

    parser = argparse.ArgumentParser(description="pyconcurrent CLI")

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


def _run(max_resource_id: int, base_url: str):
    """
    Runs the demo app with the resource counts with a single worker.

    :param max_resource_id: The maximum resource id
    :param base_url: The base URL used to fetch resources
    """

    resource_ids = list(range(1, max_resource_id + 1))
    _submit_requests(base_url, resource_ids)


if __name__ == "__main__":

    with Timer() as t:
        args = _parse_args()
        logging.info("Starting pyconcurrent with the following options . . . ")
        logging.info(f"workers = 1")
        logging.info(f"resourceid = {args.resourceid}")
        logging.info(f"url = {args.url}")

        _run(args.resourceid, args.url)

    logging.info("results ***********************")
    logging.info(f"elapsed time {t.elapsed_time}")
    logging.info("*****status code count*****")
    for k, v in api_results.items():
        logging.info(f"response code {k} = {v}")
    logging.info("*************************")
