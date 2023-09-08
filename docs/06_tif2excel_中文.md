# Tiff to Excel

### 簡介

* 將 `.tif` 檔案轉換為 `Excel` 格式

### 目的

* 方便建立數值模型，將**地表高程**資料(`.tif`)轉換為 `.xlsx`，並將其導入 `feflow`

---

### 範例

```python
# tif2excel.py
import numpy as np
import pandas as pd
from osgeo import gdal


def tif_to_xyz(tif_path: str, output: str, step=3) -> None:
    """
    Convert a GeoTIFF file to an Excel file in XYZ format.

    Args:
        tif_path (str): The path of the input GeoTIFF file.
        step (int): The sampling interval of the output data. Default is 3.

    Returns:
        None.

    """
    ds = gdal.Open(tif_path)
    band = ds.GetRasterBand(1)

    width = ds.RasterXSize
    height = ds.RasterYSize

    gt = ds.GetGeoTransform()
    minX = gt[0]
    minY = gt[3] + width*gt[4] + height*gt[5]
    maxX = gt[0] + width*gt[1] + height*gt[2]
    maxY = gt[3]

    print(f"the domain : ({minX}, {maxX}) ({minY}, {maxY})")

    elevation = band.ReadAsArray()

    gridx = np.linspace(minX, maxX, width)
    gridy = np.linspace(maxY, minY, height) # flip the y-axis to match the XYZ format
    X, Y = np.meshgrid(gridx[::step], gridy[::step])
    Z = elevation[::step, ::step].flatten()

    # Remove the boundary value (-32767)
    boundary_index = np.where(Z == -32767)[0]
    X, Y, Z = np.delete(X.flatten(), boundary_index), np.delete(Y.flatten(), boundary_index), np.delete(Z, boundary_index)
    S = np.ones_like(X)

    file = pd.DataFrame({'x': X, 'y': Y, 'z': Z, 'slice': S})
    file.to_excel(output, index=False)
    print("Finished!")


if __name__ == "__main__":
    tif_file = 'YOUR_TIFF_FILE.tiff'
    output = 'test.xlsx'

    tif_to_xyz(tif_file, output)
```