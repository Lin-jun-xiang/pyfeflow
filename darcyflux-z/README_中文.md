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


