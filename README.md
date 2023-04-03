## :penguin:FEFLOW-PYTHON
* [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)

- **Required Software**
    - `FEFLOW`: Groundwater flow numerical simulation (Free or paid version)
    - `Python`

* **Overview of Functions**
    *  - [x] [Visualization of Pumping Test Drawdown](./drawdown/)
    *  - [x] [Monte Carlo Numerical Simulation](./mc/)
    *  - [ ] [Markov Chain Monte Carlo Numerical Simulation](./mcmc/)
    *  - [x] [Automatic Optimization (Calibration) Simulation](./optimization/)
---

### Introduction

This project develops a package for groundwater flow numerical simulation using `ifm-api-python`.

>What is `ifm-api`?
>Interface Manager is a built-in function (API) in `feflow`. By calling these functions through scripts (e.g., `python`, `c++`), the entire simulation process can be operated to achieve more refined and automated numerical simulation.
>
>For example, if you want to perform tens of thousands of simulations, it is not practical to repeatedly operate through `feflow GUI`, but by scripting, you can write a program to perform tens of thousands of simulations and save the results of each simulation.

---

### Instructions

1. Click the :star: `Star` button on this project to support and motivate the developer.

2. Make sure you have `feflow` and `python` installed on your computer.

3. Use the link in the function overview to access detailed information and source code for each function.

    * Each function introduction will first explain whether `feflow` requires a `license`.

    * Each function will have a detailed instruction file (`README.md`).

4. Clone the repository using `git clone https://github.com/Lin-jun-xiang/feflow-python-ifm.git`.

5. Start using the package.

<a href="#top">Back to top</a>
