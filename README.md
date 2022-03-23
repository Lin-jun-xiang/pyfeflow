# Optimization-by-BAS
### Introduction
Using Beetle Antennae Search algorithm (BAS) to solve the groundwater simulation problem.

In our study area have a lot of private wells that we cannot get the detailed information (ex: well location, well pumping rate). Therefore, we set some virtual wells uniformly in the study area, and all the pumping rate are our system parameters. The system parameters will be adjust by BAS.

The BAS are developed in 2017 (Jiang and Li), and the algorithm as following:

![image](https://user-images.githubusercontent.com/63782903/159463464-716ea7a1-7af6-491e-aebd-db98ea735cd2.png)

---
### Part1 - Study area

Roughly explain:
1. The study area is Pingtung in Taiwan.
2. The following image is the groundwater table of observation.

![image](https://user-images.githubusercontent.com/63782903/159640237-e52cecde-67de-4818-94fc-4c3c03219a4f.png)

---
### Part2 - Groundwater Simulation

Roughly explain:
1. We use the **FEFLOW7.3** to build our flow model.
2. Setting the boundary condition. (ex: Dirichlet, Neumann...)
3. Setting the hydraulic conductivity and inflow of study area.

---
### Part3 - Result

As we can see, the result is not good without well setting.
(gray line : observation ; color line : simulation result)

And compare to the observation data, the **absolute erro**r is 6.87, **root mean square** is 7.83 and **standard deviation** is 8.

![image](https://user-images.githubusercontent.com/63782903/159640520-910c0a10-67a5-45de-b03b-93d0be45e868.png)

---
### Part4 - Optimization

We set well in the study area uniformly, and then use BAS.

The **absolute erro**r is 0.988, **root mean square** is 1.3 and **standard deviation** is 1.3.

![image](https://user-images.githubusercontent.com/63782903/159641259-042c74c8-3028-4253-a7b8-249b46966bc5.png)

