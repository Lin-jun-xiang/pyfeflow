# IFM & USER_DATA
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
