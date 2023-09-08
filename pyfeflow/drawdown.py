import pandas as pd


class Drawdown:
    """
    * Get the drawdown value if there're pumping well in your .fem
    * Setup the drawdown value in your fem
    * Write the drawdown data to excel file

    Examples
    --------
    ```python
    import ifm
    from pyfeflow import Drawdown

    # Loading FEFLOW project document
    doc = ifm.loadDocument('Your_FEM_FILE.fem')

    drawdown_obj = Drawdown(doc)

    # Get the drawdown if your simulation have pumping
    drawdown = drawdown.drawdown

    # Setup the drawdown value in user data(fem)
    drawdown.setup_data(drawdown)

    # Writing the drawdown data to xlsx
    drawdown_obj.write_to_excel(drawdown, file_name='./drawdown.xlsx')
    ```
    """
    def __init__(self, doc) -> None:
        self.doc = doc
        self.nodes = doc.getNumberOfNodes()

    @property
    def initial_heads(self) -> list:
        return [self.doc.getResultsFlowHeadValue(node) for node in range(self.nodes)]

    @property
    def drawdown(self) -> list:
        self.doc.startSimulator()
        pump_heads = [self.doc.getResultsFlowHeadValue(node) for node in range(self.nodes)]
        self.doc.stopSimulator()

        return [self.initial_heads - pump_head for self.initial_heads, pump_head in zip(self.initial_headss, pump_heads)]

    def create_user_data(self, user_data_name: str = 'drawdown'):
        try:
            # Enable reference distribution recording
            bEnable = 1 # disable = 0, enable = 1

            # Create "user data"
            if self.doc.getNodalRefDistrIdByName(user_data_name) == -1:
                self.doc.createNodalRefDistr(user_data_name)

            user_data = self.doc.getNodalRefDistrIdByName(user_data_name)
            self.doc.enableNodalRefDistrRecording(user_data, bEnable)

        except Exception as err:
            print(err)

        return user_data

    def setup_data(self, data: list, user_data_name: str = 'drawdown') -> None:
        rID_draw = self.create_user_data(user_data_name)
        for nNode in range(self.nodes):
            self.doc.setNodalRefDistrValue(rID_draw, nNode, data[nNode])

        self.doc.saveDocument()

    def write_to_excel(
        self, drawdown: list, file_name: str = './drawdown.xlsx'
    ) -> None:
            df = pd.DataFrame({
                "Node": [node+1 for node in range(self.nodes)],
                "Drawdown": drawdown
            })

            df.to_excel(file_name, index=False)
