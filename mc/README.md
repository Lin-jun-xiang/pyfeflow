# MonteCarlo
* [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)
### Introduction

* Monte Carlo simulation:
    By using multiple random sampling and simulation, various possibilities of groundwater flow can be obtained and the **uncertainty** of groundwater flow can be **quantified** to improve the accuracy and reliability of model prediction.

* Simulation method:

    1. Define the **Probability Density Function (PDF)** of the parameters, which can usually be established based on empirical formulas.
    2. Randomly sample the defined PDF to generate **realizations** and obtain the corresponding groundwater flow field.
    3. Repeat steps 1 and 2.
    4. For the n simulation results obtained in step 3, conduct statistical analysis such as calculating the mean, standard deviation, percentiles, etc., to obtain a statistical distribution that represents the simulation results.
    5. Based on the obtained statistical distribution, conduct risk assessment or other related applications, such as calculating the probability distribution of a certain water level or flux, or calculating the worst-case scenario under different water level or flux conditions.

* Tools used:
    * Numerical groundwater simulation tool: FEFLOW 7.3
    * Scripting language: Python 3.8.6

---

### Example

1. Use the **hydraulic conductivity (K)** as the uncertain parameter in the experiment.

2. Define the PDF of K based on empirical formulas

3. Use the stats module in Python to generate n random samples of K.

4. Conduct Monte Carlo simulation:
    * Set the sampled K values to the model using ifm.
    * Each time the K value is set, conduct simulation and record the velocity.
    * Repeat the above n times.

5. Visualize the results of the velocity obtained from n simulation runs. (`matplotlib`, `seaborn`, `plotly`, ...)
    ![](../images/2023-04-03-21-59-51.png)