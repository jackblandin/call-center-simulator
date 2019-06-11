# Call Center Simulator

## Setup

The following steps show how to setup the conda environment so that all dependencies are correctly installed, as well as how to run the Jupyter Notebooks in the context of the conda environment.

```sh
# Create the conda environment from the config file
conda env create -f=conda.yaml

# Activate the conda environment
conda activate call-center-simulator

# Create an IPython kernel which will allow you to run the Jupyter Notebook in the conda environment
python3.4 -m ipykernel install --user --name call-center-simulator --display-name "conda (call-center-simulator)"

# Start the jupyter notebook
jupyter notebook
```

Then when you're in the Jupyter Notebook, select `Kernel > Change Kernel > conda (call-center-simulator)`.


## Start simulator
```
python3.4 call-center-simulator/simulate.py
