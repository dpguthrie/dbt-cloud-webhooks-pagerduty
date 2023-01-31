# dbt Cloud Webhooks - Datadog

## Overview

This repo contains code necessary to create PagerDuty alerts in the event of a job error.

## Requirements

Python 3.7+

- [dbtc](https://dbtc.dpguthrie.com) - Unofficial python interface to dbt Cloud APIs
- [FastAPI](https://fastapi.tiangolo.com) - Modern, fast, web framework for building APIs with Python 3.7+
- [requests](https://requests.readthedocs.io/en/latest/) - Elegant and simple HTTP library for Python, built for human beings
- [uvicorn](https://uvicorn.org) - ASGI web server implementation for Python 

## Getting Started

Clone this repo

```bash
git clone https://github.com/dpguthrie/dbt-cloud-webhooks-pagerduty.git
```

## Deploy on fly.io (Optional)

[fly.io](https://fly.io) is a platform for running full stack apps and databases close to your users.

### Install

Directions to install [here](https://fly.io/docs/hands-on/install-flyctl/)

Once installed, sign up for fly.io

```bash
flyctl auth signup
```

Now sign in

```bash
flyctl auth login
```

Launch your app!

```bash
flyctl launch
```

### Secrets

The following secrets need to be configured to your runtime environment for your application to work properly.

- `DBT_CLOUD_SERVICE_TOKEN` - Generate a [service token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens#generating-service-account-tokens) in dbt Cloud.  Ensure that it has at least the `Metadata Only` permission as we will be making requests against the Metadata API.
- `PD_ROUTING_KEY` - Use the integration key for your integration (will be used as `routing_key`).  More info [here](https://developer.pagerduty.com/docs/ZG9jOjExMDI5NTgw-events-api-v2-overview#getting-started)

To set a secret in your fly.io app, do the following:

```bash
flyctl secrets set DBT_CLOUD_SERVICE_TOKEN=***
```

Or set them all at once:

```bash
flyctl secrets set DBT_CLOUD_SERVICE_TOKEN=*** PD_ROUTING_KEY=***
```

### Other Helpful Commands

Check the secrets set in your app

```bash
flyctl secrets list
```

Monitor your app

```bash
flyctl monitor
```

Open browser to currently deployed app

```bash
flyctl open
```

## Other Deploy Options

- [AWS Lambda Example](https://adem.sh/blog/tutorial-fastapi-aws-lambda-serverless)
- [Google Cloud Run Example](https://github.com/sekR4/FastAPI-on-Google-Cloud-Run)