### Building and running the application
This file was originally generated using `docker init` which in of itself it a helpful docker command ;)

When you're ready, start your application by running:
`docker compose up --build` [-d] for detached.

## Helpful docker commands:
* Bring everything down
```bash
docker compose down
```
* Exec into container (enter its terminal)
```bash
docker exec -it <container id> /bin/bash
```
* Exec into db container, start sql command line with running
```bash
docker exec -it github-pi-db-1 /bin/bash
psql
```

## Other Commands for running our project:
### __See the Makefile__

* Run in dev mode (syncs files as you edit them)
```bash
docker compose watch
```

* Run without dev mode
```bash
docker compose up --build -d
```

* Get and follow logs
```bash
docker compose logs -f
```

* Dump Database
```bash
docker exec -it github-pi-db-1 /bin/bash
psql

```

### Deploying your application to the cloud

If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

