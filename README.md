# pyconcurrent

Python Concurrent Application Demo

Contrast concurrent approaches and techniques, threading, multi-processing, and asyncio using a single, simple, and
quite contrived use-case.

## The Use Case

Fetch each photo resource from [JSON Placeholder](https://jsonplaceholder.typicode.com/photos), a free to use "sample" api,
and record the results in a data structure.

Note: This isn't a use case which would really benefit from multiprocessing. The multiprocessing implementation is included
just to contrast approaches.

## Getting Started

Create a virtual environment and install dependencies

```shell
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

Switch to the appropriate feature branch and run the application
```shell
git checkout <feature branch name>
PYTHONPATH=./src python3 -m pyconcurrent.main
```

Available feature branches include:

* main - a single threaded approach
* manual-threads - multiple threads implemented without an "executor"
* threadpool-executor - threadpool executor with future callback function
* process-executor - processpool executor with future callback function
