# Simulate a Self-Driving-Car
Using the technique of "Behavioral Cloning" train a car to drive itself on a track in Unity3D simulation


## Usage

### Run the pretrained model

Start up [the Udacity self-driving simulator](https://github.com/udacity/self-driving-car-sim), choose **lake track** and press the Autonomous Mode button.  Then, run the model as follows:

```python
python Run_Simulation.py
```

### To train the model

Fire up the Simulator and record data in training mode for any track.

Run **model.ipynb**

This will generate files `model-<val_loss>.h5`. Choose the file with minimum validation loss as the model file.

Then Run 
```
python Run_Simulation.py --path=[PATH TO MODEL]
```

## Demo

![ Demo ]( ./Demo.gif )
