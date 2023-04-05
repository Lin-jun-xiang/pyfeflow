import ifm
import sys

sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")

doc = ifm.loadDocument('C:\\JunXiang\\傑明工程\\Fem\\test.fem')

doc.startSimulator()

nodes = doc.getNumberOfNodes()

def create_user_data(user_data_name: str):
    try:
        # Enable reference distribution recording
        bEnable = 1 # disable = 0, enable = 1

        # Create "user data"
        doc.createNodalRefDistr(user_data_name)

        rID_velZ = doc.getNodalRefDistrIdByName(user_data_name)
        doc.enableNodalRefDistrRecording(rID_velZ, bEnable)

    except Exception as err:
        print(err)

    return rID_velZ

def set_user_data():
    for nNode in range(nodes):
        doc.setNodalRefDistrValue(rID_velZ, nNode, doc.getResultsZVelocityValue(nNode))

rID_velZ = create_user_data("Velocity_Z")
set_user_data()

doc.stopSimulator()
doc.saveDocument()
