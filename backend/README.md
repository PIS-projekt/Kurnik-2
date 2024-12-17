# Backend app

## Running locally using docker

The docker compose consists of 3 targets:

* `backend` - runs the database & backend server in development mode

```bash
docker compose up backend
```

* `database` - runs the database container

```bash
docker compose up database
```

* `backend-tests` - tests, lints and generate coverage reports,
commands described below

```bash
docker compose up database-tests [command]
```

After making changes, remember to run compose with the `--build` flag
or they will not affect the containers. When making changes to the backend,
it's easier to use `pdm start` to avoid rebuilding the backend on each change
and run just the database using compose.

## Scripts

### Install production dependencies locally

```bash
pdm install --prod
```

### Install development dependencies locally

```bash
pdm install --dev
```

### Run application

```bash
pdm run start
```

### Run tests

```bash
pdm run test
```

### Run linter

```bash
pdm run lint
```

### Run formatter

```bash
pdm run format
```

### Generate coverage report

```bash
pdm run coverage
```

### Build Docker image for production

```bash
docker build -t pis-backend --target prod .
```

### Build Docker image for testing

```bash
docker build -t pis-backend-test --target test .
```

### Run Docker development container

```bash
docker run pis-backend-test [COMMAND]
COMMAND:
    test - run tests
    lint - run linter
    coverage - generate coverage report
```
