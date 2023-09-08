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

```python
# ifmDrawdown.py
import sys

import ifm
import pandas as pd


# Adding FEFLOW directory to system path
sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")

# Loading FEFLOW project document
doc = ifm.loadDocument('Your_FEM_FILE')

# Get the Nodes in fem
nodes = doc.getNumberOfNodes()

# Get the initial head for each node
init_heads = [doc.getResultsFlowHeadValue(node) for node in range(nodes)]

# Start simulation with pumping
doc.startSimulator()

# Get the head for each node after pumping
pump_heads = [doc.getResultsFlowHeadValue(node) for node in range(nodes)]

# Calculate the "drawdown"
drawdown = [init_head - pump_head for init_head, pump_head in zip(init_heads, pump_heads)]


def create_user_data(user_data_name: str):
    try:
        # Enable reference distribution recording
        bEnable = 1 # disable = 0, enable = 1

        # Create "user data"
        if doc.getNodalRefDistrIdByName(user_data_name) == -1:
            doc.createNodalRefDistr(user_data_name)

        user_data = doc.getNodalRefDistrIdByName(user_data_name)
        doc.enableNodalRefDistrRecording(user_data, bEnable)

    except Exception as err:
        print(err)

    return user_data


def set_user_data():
    for nNode in range(nodes):
        doc.setNodalRefDistrValue(rID_draw, nNode, pump_heads[nNode])

rID_draw = create_user_data("drawdown")
set_user_data()

doc.stopSimulator()
doc.saveDocument()

# Writing the drawdown data to xlsx
df = pd.DataFrame({
    "Node": [node+1 for node in range(nodes)],
    "Drawdown": drawdown
})

df.to_excel("..//Excel//Drawdown.xlsx", index=False)
```
