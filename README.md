# FastAPI chat backend

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

Backed for chat app, supports: REST API, WS, DynamoDB integration, and S3 integration.

## Getting Started <a name = "getting_started"></a>

### Prerequisites

1. Make sure that you have boto3 installed and configured with your AWS credentials.
2. Add the appropriate IAM policies - access for DynamoDB and S3

### Installing

Install the requirements

```
pip install -r requirements.txt
```

## Usage <a name = "usage"></a>

For starting the server:

```
python main.py
```

Then you can access it on: <href>http://127.0.0.1:8000/docs</href>

All Models can be viewed on the "Schemas" section on the docs webpage.
