## :penguin:FEFLOW-PYTHON-IFM

<div>
<img src="https://github.com/Lin-jun-xiang/Lin-jun-xiang/blob/main/gif/ba412152801f0d8081e492986ab0529e.gif?raw=true" width=20% height=20% />
</div>


[English](./README.md) | [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)

<div>
    <img src="https://readme-typing-svg.demolab.com/?pause=1&size=50&color=f75c7e&center=True&width=1200&height=120&vCenter=True&lines=Click+the+⭐+Star+please.;Any+questions+can+be+asked+in+Issue." />
</div>


---

- **Required Software**
    - `FEFLOW`: Groundwater flow numerical simulation (Demo or license version)
    - `Python`

<p align=center>
<image src="https://user-images.githubusercontent.com/63782903/229553525-60e5cfaf-fbb4-4b82-994e-4a7d3e64049e.png" width=50%>
</p>

* **Overview of Functions**
    *  - [x] [Introduction to IFM and USER-DATA](./darcyflux-z/)
    *  - [x] [Visualization of Pumping Test Drawdown](./drawdown/)
    *  - [x] [Monte Carlo Numerical Simulation](./mc/)
    *  - [ ] [Markov Chain Monte Carlo Numerical Simulation](./mcmc/)
    *  - [x] [Use *Cache-Optimized* Monte Carlo Simulation](./mc-cache/)
    *  - [x] [Optimization Algorithim (Calibration)](./optimization/)
    *  - [ ] [Discritization Package]()
    *  - [x] [Unsaturation Curve](./water-retention-curve/)
    *  - [x] [Tiff to Excel](./tif-to-excel/)

---

### Introduction

This project develops a package for groundwater flow numerical simulation using `ifm-api-python`.

>What is `ifm-api`?
>Interface Manager is a built-in function (API) in `feflow`. By calling these functions through scripts (e.g., `python`, `c++`), the entire simulation process can be operated to achieve more refined and automated numerical simulation.
>
>For example, if you want to perform tens of thousands of simulations, it is not practical to repeatedly operate through `feflow GUI`, but by scripting, you can write a program to perform tens of thousands of simulations and save the results of each simulation.
>
>`ifm` [docs](http://www.feflow.info/html/help73/feflow/13_Programming/IFM/API/api_index.html)

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
