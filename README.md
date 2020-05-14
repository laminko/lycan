# [lycan](https://en.wikipedia.org/wiki/Lycan): loadtester script

A simple load testing script using [locust](https://locust.io/) and [pyyaml](https://pyyaml.org/). The story behind this is Ko [Setkyar](https://github.com/setkyar) wants to test some APIs and not-so-complex and light weight solution. I found locust but tasks are defined in python. To overcome this, I create this python wrapper which generates `HttpLocust` and `TaskSet` classes from `yaml` file at runtime.

## Installation

First, an python environment is required. To resolve this, I would like to recommend **miniconda**.
To install **miniconda**, please refer to https://docs.conda.io/en/latest/miniconda.html.

### Requirements

 - python 3.6+

### Dependencies

Install required python libraries.

```bash
cd /path/to/lycan
# NOTE:
# To create python 3.6 environment,
# $ conda create -n <env-name> python=3.6
#
# To activate environment, if not yet.
# $ conda activate <env-name>

# Then, install required dependencies
$ pip install -r requirements.txt
```

## Usage

First, create a `yaml` file inside `rules` directory.

Rule format is as follows:

```yaml
name: TestThisHost
proto: http
host: localhost
port: 8000
tasks:
  - endpoint: /api/v1/users/
    method: POST
    # To define Headers
    headers:
      Content-Type: application/json
      ...
    data:
      name: kyawkyaw
      address: Yangon
  - endpoint: /api/v1/users/1
    method: GET
    headers:
      Content-Type: application/json
  - ...
```

Then, run following command:

```bash
$ locust -f loadtester.py
```

To start load testing, please open `http://localhost:8089` in browser.

Ref: https://docs.locust.io/en/stable/quickstart.html#open-up-locust-s-web-interface.