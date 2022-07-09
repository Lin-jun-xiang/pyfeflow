# Optimization-by-BAS
### Introduction
Using Beetle Antennae Search algorithm (BAS) to solve the groundwater simulation problem.

* Numerical groundwater simulation tool : FEFLOW7.3

* Script : Python 3.8.6

In our study area have a lot of private wells that we cannot get the detailed information (ex: well location, well pumping rate). Therefore, we set some virtual wells uniformly in the study area, and all the pumping rate are our system parameters. The system parameters will be adjust by BAS.

The BAS are developed in 2017 (Jiang and Li), and the algorithm as following:

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159463464-716ea7a1-7af6-491e-aebd-db98ea735cd2.png" width=50%/>
</p>

---
### Workflow

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
> **absolute error** is 6.87

> **root mean square** is 7.83

> **standard deviation** is 8.

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159640520-910c0a10-67a5-45de-b03b-93d0be45e868.png" width=200px/>
</p>

---
### Part4 - After Optimization

We set well in the study area uniformly, and then use BAS.

> **absolute error** is 0.988

> **root mean square** is 1.3

> **standard deviation** is 1.3.

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159641259-042c74c8-3028-4253-a7b8-249b46966bc5.png" width=50%/>
</p>

---
### Part5 - Results

The **absolute error** reduces
