# MUSIC

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Project](#running-the-project)
  - [Running a Specific Container](#running-a-specific-container)
  - [Accessing the Applications](#accessing-the-applications)


## Overview

This is a Django REST Framework application that provides an API for managing artists, albums, tracks, and playlists with there specific tracks and orders.

### Features

- **Artists**: List artists
- **Albums**: List albums
- **Tracks**: List tracks
- **Playlists**:  playlists Create, read, update, and delete

## Getting Started

### Prerequisites

To get started with Music, you will need the following prerequisites:

- Docker
- Docker Compose

### Installation

1. Clone this repository to your local machine:

   HTTPS: `https://github.com/ankurzalaya06/musics.git`

   ```bash
   cd musics
   ```

2. Build the Docker containers using the following command:

   ```bash
   docker-compose.yml build
   ```

## Usage

### Running the Project

To run the entire project, including  containers and services, use the following command:

```bash
docker-compose up
```

### Running a Specific Container

If you want to access container and  its shell, use the following command as an example:

```bash
docker-compose  exec -it music_catalogue-web-1 sh
```

Here's what each part of the command means:

- `docker-compose`: This command is used to manage multi-container Docker applications using a `docker-compose.yml` file.
- `exec`: This command is used to execute a command in a running container.
- `music_catalogue-web-1`: This is the name of the container you want to run the command in.


### Accessing the Applications

Once the project is running, you can access the applications using the following URLs:

- Frontend Main Site: [http://localhost:8000](http://localhost:8000)
- Frontend Admin Site: [http://localhost:8000/admin](http://localhost:8000/admin)

Access the backend services using their respective ports:

- Backend APIS Service: [http://localhost:8000/api](http://localhost:8000/api)



### For downloading Docker and Docker Compose:

- Download Docker: [Docker](https://www.docker.com/get-started)
- Download Docker Compose: [Docker Compose](https://docs.docker.com/compose/install/)
```
