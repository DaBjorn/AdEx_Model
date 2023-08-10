# AdEx_Model

This repository contains the work I did for my MS thesis work on Adaptive Exponential Integrate and fire model.

Uploaded files:
1. adex_fns.py contains the AdEx differential equation
2. paramvalues.py contains the parameter values used in the numerical analysis
3. Nonlinear.py creates a curve that represents the exponential dependency of the integrate and fire model
4. spikepatter.py contains the code for creating spike patterns of the AdEx model by using the parameter values and function from 1 and 2.
5. firingrate.py contains the code for plotting the variation of firing rate with respect to input current.
6. randomcoupled_neurons.py contains the code for plotting the spikepattern of 100 neurons randomly (p = 0.2) which is given a uniform current input
7. uncoupled_neurons.py contains the code for plotting the spikepatter of 100 neurons which are not coupled given the same input
8. spikepatter_brian.py uses the brian2 python module to plot the spike pattern of AdEx model
9. coupled_neurons.py shows the time series and spike pattern of two coupled neurons in which only one of them recieves the input current
