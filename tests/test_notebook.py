import testbook
from testbook import testbook

@testbook('notebooks/Example01_BrokenModularisation.ipynb', execute=True)
def test_broken_modularisation(tb):
    # Import the BrokenModularisation class from the notebook
    BrokenModularisation = tb.ref("BrokenModularisation")

    # Define parameters for the test
    params = {
        "length": 120.0, 
        "width": 40.0, 
        "height": 80.0, 
        "feature_A_length": 40.0, 
        "feature_A_thickness": 60.0, 
        "feature_B_length": 40.0, 
        "feature_B_thickness": 60.0, 
        "hole_diameter": 20.0, 
        "hole_A_position": (20, 70), 
        "hole_B_position": (100, 70)
    }
    
    # Execute the class with the parameters
    # Ensure the class and its methods are correctly referenced from the notebook
    obj = tb.execute_cell('name_of_cell_defining_BrokenModularisation') # Adjust to your cell label/name

    # Optionally, directly execute a cell that instantiates the object if present in the notebook
    # tb.execute_cell('cell_label_for_instantiation')

    # Here you would add assertions to verify the correctness of your object
    # Note: Direct assertion on the notebook objects might need fetching the object or its properties back to the test scope
    assert obj is not None, "Failed to create BrokenModularisation object"
