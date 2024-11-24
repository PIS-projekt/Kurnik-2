# Backend app

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
