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
To verify the behavior of our agent we have made verification environments which we can visually inspect. To run the
interface for the model verification, you need to install the dependencies with:
```pip install --no-cache-dir -r requirements.txt```
And then run:
```python3 apocalypse_sim/run.py --test```
Then click the link to view the interactive console. With the map slider we can select a map, and then press reset to
change the map to the selected one.