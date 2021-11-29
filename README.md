# pyconcurrent

Python Concurrent Application Demo

Contrast concurrent approaches and techniques, threading, multi-processing, and asyncio using a single, simple, and
quite contrived use-case.

## The Use Case

Fetch each photo resource from [JSON Placeholder](https://jsonplaceholder.typicode.com/photos), a free to use "sample" api,
and record the results in a data structure.

## Getting Started

Create a virtual environment and install dependencies

```shell
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

Switch to the appropriate feature branch and run the application
```shell
git checkout <feature branch name>
python3 -m pyconcurrent.main
```

Available feature branches include:

* manual-threads
