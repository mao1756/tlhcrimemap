![tally crime map logo](https://github.com/mao1756/tlhcrimemap/assets/56581117/2c6fe833-e1bc-4503-8e75-207704dddff5)

# Tallahassee Crime Map

This project aims to analyze crime information in Tallahasse, FL, collected from [TOPS](https://www.talgov.com/gis/tops/).

## Project Overview

This project contains two parts:

- Traditional data analysis on TOPS data using Geopandas and Scikit-learn
- Crime heatmap prediction given a geographical map, following [He, Zheng (2021)](https://www.sciencedirect.com/science/article/abs/pii/S0952197621003080)

## Results

Please first see the [project slides](https://github.com/mao1756/tlhcrimemap/blob/main/documents/slides-outline/slides-outline.pdf) for the project summary.

### Data collection

On top of the dataset available in the `dataset` folder, you can also collect new data from TOPS using [our data collection script](https://github.com/mao1756/tlhcrimemap/blob/main/codes/TOPSdatacollection.py). Please take a look at the comments in the script on how to use it.

### Experimental Data Analysis

In addition to the slides, see our [EDA notebook](https://github.com/mao1756/tlhcrimemap/blob/main/notebooks/exploratory_data_analysis.ipynb) for detailed analysis.

### Training of pix2pix
To train pix2pix, you first need to create the image dataset for geographical and heat maps. For this, you can use [our processing script](https://github.com/mao1756/tlhcrimemap/blob/main/codes/create_pix2pix_dataset.py). After that, you need to use the [combining script](https://github.com/mao1756/tlhcrimemap/blob/main/pytorch-CycleGAN-and-pix2pix/datasets/combine_A_and_B.py) from the pix2pix repository. For the explanation of our script, see the comments in it, and for the script from pix2pix, see [their document](https://github.com/mao1756/tlhcrimemap/blob/main/pytorch-CycleGAN-and-pix2pix/docs/datasets.md). After you have made the dataset, you can train pix2pix using their script. For details, see [their documentation](https://github.com/mao1756/tlhcrimemap/blob/main/pytorch-CycleGAN-and-pix2pix/README.md).
