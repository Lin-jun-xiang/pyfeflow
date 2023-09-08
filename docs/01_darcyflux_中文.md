# IFM & USER_DATA
### 簡介

* 本章節是最簡易的部分，讓大家體驗 `ifm` 用法，同時了解 `user-data` 的使用方式

### 範例

* `ifmDarcyZ.py` 的目的:

    * `ifm` 取出模型 "**Z 方向的達西流速**"
    * 使用 `ifm` 於 `.fem` 檔案建立自定義變數 (`user-data`)
    * 將 Z 方向的達西流速賦值於自定義變數
    * 存檔

* 程式執行完後，`fem` 檔案會出現自定義變數:

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
