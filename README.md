# Technical test

Quick implementation of a social network posts ingestion pipeline.

# Testing

First deploy the docker-compose stack:

```bash
docker-compose up --force-recreate
```

*Please note that it might take some time as app and consumer services will need to pull their requirements dependancies.*

Then start the demo script:

```bash
./demo.sh
```

This script will ingest data in the data folder and fetch them back. This script assumes you have `curl` installed on your computer.
