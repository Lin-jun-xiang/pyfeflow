import ifm
import sys

sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")

doc = ifm.loadDocument('YOUR_FEM_FILE')

doc.startSimulator()

nodes = doc.getNumberOfNodes()

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
        doc.setNodalRefDistrValue(rID_velZ, nNode, doc.getResultsZVelocityValue(nNode))

rID_velZ = create_user_data("Velocity_Z")
set_user_data()

doc.stopSimulator()
doc.saveDocument()
