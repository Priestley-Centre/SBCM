# Getting Started
1. If you don't already have python installed, you should first go [here](https://www.anaconda.com/distribution/) and install the anaconda distribution. 
2. Download the model to your own computer. You can do this using the github desktop software, or just as a simple zip file.
3. We have tried to avoid using python libraries that are not already included in the distribution (we mostly use pandas, numpy, and matplotlib) so you should not need to install anything else. There is a list of third pary modules requirements in `dependencies.md`
4. The model was designed and implemented using the [spyder](https://www.spyder-ide.org/) IDE (which comes bundled with anaconda) and while it should operate using alternatives, it has not been tested under different frameworks. 
5. Spyder allows you to run specific code at the beginning of each session (you can find this under `tools>preferences>ipython console>startup`) You need to use this to make sure that python can recognise where the model is located. Set up a new python file with code similar to `setup.py`(in this repository) and add it to the "run a file" option of the spyder startup tab.
6. While we see no barrier to the code working on a variety of operating systems, it has only been tested in windows (so other operating systems may require modifications to these instructions.)

## Model introduction

### Core Model
The main body of the model is found in the `Core_Model` folder. This contains four files:

1. `formatting.py`: This contains two core functions, 1) a matplotlib routine to make sure that the fonts on all the graphs produced match and 2) a simple lookup function to translate site codes into proper english text (e.g. `NE_MBB` becomes "NE maple \ beech \ birch")
2. `functions.py`: All of the functions used by the model:
    
    - all of the equations for handling growth, supply chains and emission calculations
    - functions for calculating payback when compared to counterfactuals within the model.
3. `sbcm.py`: The "Simple Biomass Comparison Model" (sbcm). This contains the `Scenario` object used to calculate emissions and changes to carbon pools over time. The `Scenario` object contains a number of functions:

    - `initialise` sets up the model once the key variables have been set.
    - `fell` simulates the felling of a forest site within the model.
    - `runstep` simulates a year's regrowth of the forest site.
    - `report` gathers all the important results into a pandas `DataFrame` and returns a payback period.
    - `spinup` increments the forest management by a number of rotations to ensure that forest and soil carbon are at equilibrium levels.
    - `describe` prints a brief description of the scenario object.

4. `variables.py` contains all the variables as needed to run the model using default settings:

    - `SPP`: a list of species codes
    - `f_value` the multiplier for carbon fertilisation (used in `functions.py`)
    - `original data` USDA data for carbon by species (x and y for forest and soil carbon tC/ha)
    - `forest variables` variables as used in the default (Sterman et al.) parameterisation of the model.
    - `forest_use` / `coal_use` supply chain parameterisations as used in the default version of the model.

### Model Runs
The calculations used to write the paper are all contained here. They are all numbered and should be run in sequence (as some calculations rely on results from earlier calculations) A python script (`all.py`) runs everything but takes about 10 minutes to do it: this is not ~~particularly~~ efficient code... Each `.py` file relates to a corresponding results folder and saves calculated values as `.csv` files. Within each of these folders, further `.py` files exist to produce figures and charts from the paper.
