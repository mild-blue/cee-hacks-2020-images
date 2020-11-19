# CEE Hacks 2020

## Architecture
See [architecture.md](docs/architecture.md)

## Setup:

1. Install [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

1. Create file `.env` int the root directory from template file `.env.template`. This file is used
   by **docker-compose** and by **backend** and **worker** module. 
   NOTE: There is already `.env` in the repository for hackaton purposes. 
   
1. Create file `.env.test` int the root directory from template file `.env.template`. This file is used
   by **docker-compose** and by **backend** and **worker** module in unit tests only.
   This is not necessary for hackaton.
   
1. Setup **common**, **backend** and **worker** modules based on particular `README.md` files.
   Setup of **common** is not necessary.

## Development

### Everything in Docker via Docker-compose

To run whole app in Docker, execute `docker-compose up -d`.

### DB in Docker Only

To run only DB in Docker, execute `docker-compose up -d cee-hacks-2020-images-db`. 
Do not forget to set correct DB address (localhost) and port (exposed one) in `.env` file.
Do not forget to update `.env` file, i.e.:
```
POSTGRES_URL='localhost:5442'
MINIO_URL='localhost:9000'
```

## Deployment

1. To build and push **backend** image, execute `make build_and_push_backend`.
1. To build and push **worker** image, execute `make build_and_push_worker`.
1. To redeploy **staging**, execute `make redeploy_staging`.
