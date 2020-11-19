# CEE Hacks 2020

## Architecture
See [architecture.md](docs/architecture.md)

## Setup:

1. Install [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).

1. Create file `.env` int the root directory from template file `.env.template`. This file is used
   by **docker-compose** and by **backend** and **worker** module.  
   
1. Create file `.env.test` int the root directory from template file `.env.template`. This file is used
   by **docker-compose** and by **backend** and **worker** module in unit tests only.
   
1. Setup **common**, **backend** and **worker** modules based on particular `README.md` files.

## Development

### Docker-compose Only

To run whole app in Docker, execute `docker-compose up -d`.

### DB in Docker Only

To run only DB in Docker, execute `docker-compose up -d cee-hacks-2020-images-db`. 
Do not forget to set correct DB address (localhost) and port (exposed one) in `.env` file.
