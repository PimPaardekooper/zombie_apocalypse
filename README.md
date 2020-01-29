# zombie_apocalypse
whe moddel zombbies
# How to run our project
We have made it very easy. Just follow these steps:
### Install docker
Yo can install docker using these steps written here:
https://docs.docker.com/get-docker/
## Build the docker image
```sudo docker image build -t zombie .```
## Run docker image
```sudo docker run -p 8521:8521 zombie```
You will see a file called output.pdf containing the resulting figure.

# Verification of agent behavior
We have made verification environments, which we can visually inspect, to verify the behavior of our agents. To open the
graphical user interface (GUI) for model verification, the following steps must be followed:
1. Install project dependencies: ```pip install --no-cache-dir -r requirements.txt```
2. Run the server: ```python3 apocalypse_sim/run.py --test```
3. Click the link in your terminal to view the GUI.

With the map slider, one can select a map and then press ```reset``` to see the changes to the GUI and model.
