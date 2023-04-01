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
