# Drawdown Visualization
* [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)

### Introduction

* Drawdown: the difference between groundwater levels before and after pumping.

* Calculation of drawdown
    * Subtracting the groundwater level after pumping from the groundwater level before pumping.

* Tools used
    * Numerical groundwater simulation software: FEFLOW 7.3

    * Scripting language: Python 3.8.6

* Program principle:
    1. Use `ifm` to extract the current hydraulic head value (`doc.getResultsFlowHeadValue()`)
    2. Set the pumping rate and simulate the pumping
    3. Extract the hydraulic head value after pumping
    4. Calculate the drawdown by subtracting the hydraulic head value after pumping from the hydraulic head value before pumping.

### Example

1. `ifmDrawdown.py` calculates `drawdown.xlsx` as follows:
    | Node | Drawdown |
    | ---- | -------- |
    |1|0.000639|
    |2|0.001099|
    |3|0.007327|
    |...|...|

2. After executing code, In the feflow GUI:

    * `User Data`
    
        ![](../images/2023-04-03-16-41-50.png)


3. Visualize the drawdown

   <p align=center>
   <image src="https://user-images.githubusercontent.com/63782903/229460648-27bd0a51-1e2d-4d38-ac1e-21d49c0a4b34.png" width=50%>
      </p>
