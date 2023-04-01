import pandas as pd

# Need "Node" and "Head"

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

# Stop simulation with pumping
doc.stopSimulator()

# Writing the drawdown data to xlsx
df = pd.DataFrame({"Node" :  [node+1 for node in range(nodes)],
                              "Drawdown" : drawdown})
print(df.head(5))

df.to_excel("..//Excel//Drawdown.xlsx", index=False)

