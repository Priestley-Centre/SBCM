
# Simple Bioenergy Comparison Model
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Priestley-Centre/SBCM?include_prereleases)](https://github.com/Priestley-Centre/SBCM/releases)
[![GitHub](https://img.shields.io/github/license/Priestley-Centre/SBCM)](https://github.com/Priestley-Centre/SBCM/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Version control
This is version 0.9. Pre-release. It is broadly equivalent to the supplementary materials available with the paper introducing the model: (DOI https://doi.org/10.1088/2515-7620/ab7ff3). There are a few tweaks and updates required before we get to version 1.0 though (mostly to the documentation). 

## Changes coming soon
With the publication of a paper introducing the model now having passed peer review and being published, we will be making some changes. The model runs that we have included here will be attached to **Version 1** of the model (which will have a formal release) and will then be removed. This is because subsequent editions of the model will be using a different framework and they will not run on the same version. If you still want to see the files, they will be attached to the paper along with a copy of the model that they are designed to use, or you can go to the releases page and download version 1 (which will have them bundled with it).
Subsequent changes will require a new version and a clearing of the decks, and this is the version which will be available from the front page.

**If this is not making sense, then don't worry - I'll be working on this quite a bit over the next few days, and it should all become clear soon.**


## Getting Started
1. If you don't already have python installed, you should first go [here](https://www.anaconda.com/distribution/) and install the anaconda distribution. 
The model does not require any python libraries that are not already included in the distribution (primarily pandas, numpy, and matplotlib) so you should not need to install anything else. If you do, this is easy to install from the Python command line using either the >conda install [package] or >pip install [package]
2.  Download the model to your own computer. You can do this using the github desktop software, or just as a simple download.
3. The model was designed and implemented using the [spyder](https://www.spyder-ide.org/) IDE (which comes bundled with anaconda) and while it should operate using alternatives, it has not been tested under different frameworks. 
4. Spyder allows you to run specific code at the beginning of each session (you can find this under tools>preferences>ipython console>startup) You need to use this to make sure that python can recognise where the model is located. Set up a new python file with code similar to `setup.py`(in this repository) and add it to the "run a file" option of the spyder startup tab.
5. While we see no barrier to the code working on a variety of operating systems, it has only been tested in windows (so other operating systems may require modifications to these instructions.)

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

## Code Edits & bug reports 
We absolutely want this code to be freely available, and welcome any useful modifications, upgrades, and bug reports.
Please do be aware, however that this code is live and being worked on frequently, so it would probably be a good idea to contact the author first to make sure that you won't break something important or that your idea is not already being worked on.

