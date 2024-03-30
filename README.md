# Refactoring CAD Proof of Concept

## Table of Contents
- [Refactoring CAD POC](#refactoring-cad-poc)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
      - [Jupiter Notebook Prerequisites](#jupiter-notebook-prerequisites)
    - [Installation](#installation)
      - [Jupiter Notebook Setup](#jupiter-notebook-setup)
  - [Usage](#usage)
    - [Using the CAD Refactoring Library](#using-the-cad-refactoring-library)
    - [Interactive Exploration with Jupyter Notebooks](#interactive-exploration-with-jupyter-notebooks)
  - [Testing](#testing)
    - [Docker Environment Testing](#docker-environment-testing)
      - [Running the Test Script](#running-the-test-script)
  - [Contributing](#contributing)
  - [Licence](#licence)
  - [Acknowledgments](#acknowledgments)

## Introduction 
This project, Refactoring CAD Proof of Concept (POC), is designed to showcase a proof of concept (POC) for refactoring CAD models using CadQuery. It includes a library for CAD model refactoring, example scripts, and a Jupyter Notebook environment for interactive exploration.

## Project Structure
The project is organized as follows:

- `data/`: Contains sample data used by the CAD models.
  - processed/: Processed data that the library has transformed.
  - raw/: Original, unmodified data.
  - temp/: Temporary data storage.
- `ci/`: Continuos Intergration tests
  - [`docker_tests.sh`](ci/docker_tests.sh): Tests if docker container loads properly.
- `doc/`: Documentation related to the project.
- `notebooks/`: This directory contains Jupyter Notebooks that provide interactive demonstrations and exploratory interfaces for the project. Notebooks are an excellent tool for:
- `src/`: Source code for the CAD refactoring library.
  - `__init__.py`: Marks the directory as a Python package.
  - `refactoring.py`: Core logic for CAD model refactoring.
- `examples/`: Example scripts demonstrating how to use the library.
  - `simple_refactor_example.py`: A simple script showing a basic refactoring process.
- `tests/`: Test suite for the library.
  - `__init__.py`: Marks the directory as a Python package.
  - `test_refactoring.py`: Test cases for refactoring functionalities.
- `notebooks/`: Jupyter Notebooks for interactive demonstrations and exploration.
- `Dockerfile`: Defines the setup for a Docker container that encapsulates your project's environment. It ensures that anyone can replicate your development setup and run your project with minimal setup, regardless of their operating system or local Python environment. The Dockerfile  includes:
  - Base Image: The starting point for the Docker image is often a lightweight version of Python or a specialized image like bwalter42/jupyter_cadquery:3.5.2 for specific applications.
  Dependencies Installation: Commands to install Python packages listed in requirements.txt, ensuring all necessary libraries are available within the container.
  - Environment Setup: Configuration of the working directory, port exposure for web applications, and default commands or entry points for running the application or service.
- `LICENCE`: The license file for the project.
- `requirements.txt`: A list of Python package dependencies.
- `README.md`: This file provides an overview and instructions for the project.

```
refactoring_cad_poc/
│
├── ci/
│   └── docker_tests.sh   # Script for Docker build and run tests
│
├── data/
│   ├── processed/
│   ├── raw/
│   └── temp/
│
├── doc/
│
│
├── notebooks/          # Jupyter notebooks which can be run using Docker
│
├── src/                # Source code for your CAD refactoring library
│   ├── __init__.py     # Makes this directory a Python package
│   └── refactoring.py  # Core logic for CAD model refactoring
│
├── examples/           # Example scripts showing how to use your library
│   └── simple_refactor_example.py
│
├── tests/
│   ├── __init__.py
│   └── test_refactoring.py
│
├── Dockerfile
├── LICENCE
├── requirements.txt
└── README.md
```


##  Getting Started 
These instructions will cover the setup required to run the Jupyter-CadQuery environment using Docker. This approach ensures that all necessary dependencies are correctly installed and configured.


### Prerequisites
#### Jupiter Notebook Prerequisites
Ensure you have Docker installed on your system to explore the project interactively in the Jupyter-CadQuery environment. For installation instructions, see Docker's official documentation.

### Installation
1. Clone the repository:
    ```bash
    git clone https://your-repository-url/refactoring_cad_poc.git
    cd refactoring_cad_poc
    ```
#### Jupiter Notebook Setup
2. Build the Docker image:
    
    Navigate to the project directory and run:

    ```bash
    docker build -t my_jupyter_cadquery .
    ```
    This command builds a Docker image named my_jupyter_cadquery based on the instructions in your Dockerfile.

    As recommended on [jupyter-cadquery](https://github.com/bernhard-42/jupyter-cadquery), [Dockerfile](Dockerfile) uses the recommended Jupyter-CadQuery image as the base (`bwalter42/jupyter_cadquery:3.5.2`)

1. Run the Docker Container
    Run a container from your image with the necessary port mapping and volume mounting:

    ```sh
    docker run -it --rm -p 8888:8888 -v $(pwd):/home/cq my_jupyter_cadquery
    ```

    This command does the following:

   - -it runs the Docker container in interactive mode.
   - --rm automatically removes the container when it exits.
   - -p 8888:8888 maps port 8888 of the container to port 8888 on your host, allowing you to access JupyterLab via a web browser.
   - -v $(pwd):/home/cq mounts the current directory to /home/cq in the container, enabling direct interaction with your project files.


4. Accessing JupyterLab
    After starting the container, JupyterLab will be accessible via your web browser. Open the following URL:
    
    http://127.0.0.1:8888/lab

    *Check the URL matches the one provided in your terminal*

    JupyterLab should load, presenting an environment where you can create, edit, and run Jupyter notebooks.


## Usage
### Using the CAD Refactoring Library
The examples/ directory contains scripts demonstrating how to use the library. You can run these scripts directly or explore them in the JupyterLab environment.

### Interactive Exploration with Jupyter Notebooks
Navigate to the notebooks/ directory in the JupyterLab interface to find interactive notebooks. These notebooks provide a hands-on way to explore CAD model refactoring processes.

## Testing
### Docker Environment Testing
To ensure the Docker environment for our project is correctly set up and operational, we provide a bash script (`docker_tests.sh`) that automates the testing process. This script performs the following actions:

1. Builds the Docker image from the Dockerfile.
2. Runs a Docker container from this image in detached mode, mounting the current project directory.
3. Checks for the presence of the `notebooks/` folder inside the container to verify successful volume mounting.
4. Cleans up by stopping the running container and optionally removing the Docker image.

#### Running the Test Script
Ensure Docker is installed and running on your system, then execute the following command from the project root directory:

```sh
./ci/docker_tests.sh

```
Note: If you encounter a permission denied error, you may need to make the script executable. You can do so with the following command:
```sh
chmod +x ci/docker_tests.sh
```

## Contributing
Contributions to the Refactoring CAD POC project are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## Licence
This project is licensed under the [MIT Licence](LICENCE).

## Acknowledgments
Thanks to the CadQuery community for providing the tools and support for CAD modelling in Python.

