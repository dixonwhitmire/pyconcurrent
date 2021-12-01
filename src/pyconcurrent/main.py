"""
main.py

The pyconcurrent entry point.
"""
import argparse


def _parse_args():
    """Returns the CLI arguments for pyconcurrent"""

    parser = argparse.ArgumentParser(description="pyconcurrent CLI")

    parser.add_argument(
        "-w",
        "--workers",
        help="defines the number of workers used for the demo",
        default=5,
    )
    parser.add_argument(
        "-r", "--resourceid", help="the max photo resource id", default=5_000
    )
    parser.add_argument(
        "-u",
        "--url",
        help="the base url used to fetch resources",
        default="https://jsonplaceholder.typicode.com/photos",
    )
    return parser.parse_args()


def _run(worker_count: int, max_resource_id: int, base_url: str):
    """
    Runs the demo app with the specified worker and resource counts.

    :param worker_count: The number of workers used
    :param max_resource_id: The maximum resource id
    :param base_url: The base URL used to fetch resources
    """
    pass

if __name__ == "__main__":
    args = _parse_args()
