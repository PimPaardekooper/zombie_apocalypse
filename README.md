# Project Computational Science: Modelling of a zombie apocalypse
This repository contains the code behind the model we created for Project Computational Science. Our project is written in Python 3 and was verified to work from Python 3.6.9 up to Python 3.7.6. Other versions might not work or produce different results.

## Packages
We have made extensive use of third-party packages. These can be found in ```requirements.txt```. To install the packages all at once, the following command can be run: ```pip install --no-cache-dir -r requirements.txt```.

## Run Mesa GUI
To run an in-browser visualization of our project, we have used the Mesa framework. To start Mesa's GUI, you should follow these steps:

1. Navigate to folder containing the server launcher: ```cd apocalypse_sim/```
2. Run the launcher: ```python3 run.py```
3. Click the link in your terminal to view the GUI if it doesn't open automatically.

To run the simulation step by step, use the ```step``` button in the top right area of the GUI. To run the simulation until only (susceptible) humans or zombies are left, use the ```start``` button. To end the simulation, use the ```stop``` button. To apply new parameters for the model to run with or simply reset the simulation, use the ```reset``` button.

## Visual inspection of model
We have made several verification environments, which we can visually inspect, to verify the behavior of our agents. To open the graphical user interface (GUI) for model verification, the following steps must be followed:

1. Navigate to folder containing the server launcher: ```cd apocalypse_sim/```
2. Run the launcher: ```python3 run.py --test```
3. Click the link in your terminal to view the GUI if it doesn't open automatically.

With the map slider on the left, one can switch between verification environments and then press ```reset``` to generate a new map.

### Verification environments
- Id 0: Test if killing/infection works properly (outcome depends on seed).
- Id 1: Test if zombie tracking works properly.
- Id 2: Test if human fleeing works properly.
- Id 3: Test if grouping behaviour works properly.

## Reproduction of figure
We have saved all our experiments in the ```apocalypse_sim/experiments/``` folder. However, since some experiments may take multiple hours to run, we have provided a small experiment to reproduce one of the figures from our poster and report. Navigate to ```apocalypse_sim/experiments/``` and run ```python3 compute_time_series.py && python3 plot_series.py```. The resulting figure is stored in ```apocalypse_sim/experiments/results/series.pdf``` should correspond to the figure included at the end of this README.

## Flags
We have made use of several flags to make our lives a bit easier. They can be used as follows: ```python3 run.py --[flag]```.
- ```--test```: Loads agent behavior inspection maps.
- ```--experiments```: Loads the map with changeable parameters that match the parameters used in our experiments.
- ```--netherland```: Loads the Netherlands map.
- ```--doorway```: Loads doorway tests.
- ```--roads```: Loads roads that zombies can't enter into the map.



#### Figure
![alt text](https://i.imgur.com/FxzA4Rt.png)
