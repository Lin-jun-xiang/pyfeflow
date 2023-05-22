# Optimization-by-BAS
* [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)
### Introduction
* Using Beetle Antennae Search algorithm (`BAS`) to solve the unknow parameter problem from groundwater simulation (Reduce simulation error).

* Tools
    * Numerical groundwater simulation tool : FEFLOW7.3

    * Script : Python 3.8.6

* Function and Purpose

    * Establishing a groundwater flow model requires **fitting** simulated values to observed values, which may be difficult due to lack of data.
    * **Optimization algorithms** can **automatically adjust parameters** to achieve the fitting goal.
    * This function can use optimization algorithms to find missing data parameters and fit simulated values to observed values.

* **Optimization** algorithms vs. `FePEST` calibration:

   * Optimization algorithms can customize the objective function, making it faster and easier to fit the simulation results.
   * Optimization algorithms are not limited to specific parameters and can be applied to any unknown parameter optimization (e.g. `FePEST` can only calibrate `element` properties and cannot calibrate pumping well parameters).

* `BAS` is a type of optimization algorithm developed by Jiang and Li in 2017. The algorithm is as follows:

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159463464-716ea7a1-7af6-491e-aebd-db98ea735cd2.png" width=50%/>
</p>

* Context
In our research area, there are many private wells for which we cannot obtain detailed information (such as well location and pumping rates). Therefore, we uniformly set up some virtual wells in the study area, and all pumping rates are system parameters. These system parameters will be adjusted through `BAS` to match the simulated and observed values.
(Note: unknown parameters can be considered hydraulic conductivity, porosity, saturation, etc.)

* :warning: `Important Note`: This application scenario is referenced from the paper - <a href="https://hdl.handle.net/11296/tq3m78" target="_blank">Numerical simulation of groundwater development and evaluation - A case study of Kaoping River</a>

---
### Algorithm Flow

* Define the following:
    * **Unknown parameters** (parameters to be optimized): pumping rates of each well
    * **Objective function**: Root Mean Square Error (RMSE) between simulated hydraulic head and observed water level
    * Beetle step length
    * Spacing between whiskers

* Algorithm:

    1. Randomly initialize unknown parameters (pumping rates)
    2. Perform simulation
    3. Calculate the objective function using simulated hydraulic head and observed water level (the goal is to minimize the objective function, i.e., minimize the error)
    4. Adjust parameters using BAS, iterate repeatedly until the objective function is less than the threshold

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/168416976-8bc62e63-a839-44ba-9dec-d194c9b0ad56.png" widht=50%/>
</p>

---
### Part1 - Study area

Roughly explain:
1. The study area is Pingtung in Taiwan.
2. The following image is the groundwater table of observation.

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159640237-e52cecde-67de-4818-94fc-4c3c03219a4f.png" width=50%/>
</p>

---
### Part2 - Groundwater Simulation

Roughly explain:
1. We use the **FEFLOW7.3** to build our flow model.
2. Setting the boundary condition. (ex: Dirichlet, Neumann...)
3. Setting the hydraulic conductivity and inflow of study area.

---
### Part3 - Before Optimization

As we can see, the result is not good without well setting.
(gray line : observation ; color line : simulation result)

And compare to the observation data, the

> **absolute error**: `6.87`
>
> **root mean square**: `7.83`
>
> **standard deviation**: `8`

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159640520-910c0a10-67a5-45de-b03b-93d0be45e868.png" width=200px/>
</p>

---
### Part4 - After Optimization

We set well in the study area uniformly, and then use BAS.

> **absolute error** : `0.988`
>
> **root mean square**: `1.3`
>
> **standard deviation**: `1.3`

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159641259-042c74c8-3028-4253-a7b8-249b46966bc5.png" width=60%/>
</p>

---
### Part5 - Results

<p align="center">
<image src="https://user-images.githubusercontent.com/63782903/178942962-eb72864d-f97b-45e6-b571-ab54cf841cc3.png" width=50% />

<p align="center">
<image src="https://user-images.githubusercontent.com/63782903/178094741-34584c0d-b9a9-44c4-8386-3b2c3005522c.png" width=50%/>

<a href="#top">Back to top</a>
