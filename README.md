# Tallahassee Crime Map

This project aims to analyze crime information in Tallahasse, FL, collected from [TOPS](https://www.talgov.com/gis/tops/).

## Project Overview

This project contains two parts:

- Traditional data analysis on TOPS data using Geopandas and Scikit-learn
- Crime heatmap prediction given a geographical map, following [He, Zheng (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0952197621003080)

## Dependencies
We will develop the project using Python 3.9.5. Refer to requirements.txt for package requirements.

## Environment Setup

The following setup only works for Linux/MacOS.

- Install Python 3.9.5: `sudo apt install python3.9`

- Install venv: `sudo apt-get install python3.9-venv`

- Create a venv environment: `python3.9 -m venv venv` If you name your venv folder in a different way, please add the folder name to the `.gitignore` file.

- Activate the environment. Once you are in the environment,  it should show (venv) in front of the prompt.**Make sure to activate the environment whenever you are writing the code.** `source venv/bin/activate`

- Install packages using pip. Make sure to download the requirements.txt first. `pip install -r requirements.txt`
