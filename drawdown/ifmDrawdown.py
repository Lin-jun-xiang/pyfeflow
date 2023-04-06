import pandas as pd
import sys
import ifm

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
df = pd.DataFrame({"Node" :  [node+1 for node in range(nodes)],
                              "Drawdown" : drawdown})

df.to_excel("..//Excel//Drawdown.xlsx", index=False)
