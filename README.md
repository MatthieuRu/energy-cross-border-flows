# energy-cross-border-flows

Repository for the `energy-cross-border-flows` app. Application to visualize the flows of energy between countries.

Table of Contents
=================

   * [dash-preprocessing](#dash-preprocessing)
      * [Summary](#summary)
      * [Installation](#installation)
         * [Git Clone](#git-clone)
         * [Docker-Compose](#docker-compose)
         * [Conda Environment](#conda-environment)
      * [Usage](#usage)
         * [Scraper](#scraper)
         * [Docker-Compose](#docker-compose-1)
         * [Locally](#locally)


## Summary

This repository included differentes packages to be able to run an application where user can vizualise the flow of energy between countries. The repository includes:

- `scraper`: Scraper class to scrape the data using the [entsoe-library](https://github.com/EnergieID/entsoe-py)
- `db_manager`: Database management classes with a api usinf [FastApi](https://fastapi.tiangolo.com/). It also included a DockerFile, so it can be deploy locally or on a docker container.
- `app`: The app has been developed in [dash](https://plotly.com/dash/). It also included a DockerFile, so it can be deploy locally or on a docker container.

The design of the application is the following:

<img src='./img/diagram.png' width="500" height="200">

## Installation

### Git Clone

- ```git clone https://github.com/MatthieuRu/energy-cross-border-flows.git``` *Git clone the project from Github.*

### Docker-Compose

- ```./start.sh``` *Build and Launch the docker-compose and then each docker images associate including the postgre server*
- ```./stop.sh``` *Stopes the docker images including the postgre server*

### Conda Environment
If need to you can also use a conda environment. It's taking in account all the requirement from all the packages.
- ```conda env create``` *Create the conda environment based on the environment.yml.*
- ```conda activate energy-cross-border-flows``` *Activate the conda environment.*

## Usage

### Scraper



### Docker-Compose

In this section we are not talking about the Scraper

1. The Postre Server

2. The db_manager

3. The app
