# IFM & USER_DATA
* [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)

### Introduction

* This chapter is the easiest part, allowing everyone to experience the usage of `ifm` and understand how to use `user-data`.

### Example

* The purpose of `ifmDarcyZ.py` is to:

    * Retrieve "**Darcy velocity in the Z direction**" from the model using ifm.
    * Use `ifm` to create a custom variable (`user-data`) in the `.fem` file.
    * Assign the Darcy velocity in the Z direction to the custom variable.
    * Save the file.

* After the program is executed, the custom variable will appear in the `fem` file:

    ![](../images/2023-04-05-22-21-57.png)
    <p align=center>
    <image src="https://user-images.githubusercontent.com/63782903/230112056-21a9b469-cc8a-442c-8c1c-0468f4f96469.png" width=50%>
    </p>

```python
# ifmDarcyZ.py
import sys

import ifm


sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")

doc = ifm.loadDocument('YOUR_FEM_FILE')

doc.startSimulator()

nodes = doc.getNumberOfNodes()


def create_user_data(user_data_name: str):
    """Creates a user data with the given name.
    
    Parameters
    ----------
    user_data_name (str)
        A string representing the name of the user data to be created.

    Returns
    -------
    user_data (int)
        An integer representing the ID of the created user data.
    """
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
    """Sets the user data.
    """
    for nNode in range(nodes):
        doc.setNodalRefDistrValue(rID_velZ, nNode, doc.getResultsZVelocityValue(nNode))

rID_velZ = create_user_data("Velocity_Z")
set_user_data()

doc.stopSimulator()
doc.saveDocument()
```
