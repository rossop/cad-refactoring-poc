from unittest.mock import patch, MagicMock
import pytest
from testbook import testbook

@pytest.fixture(scope='module')
def tb():
    with testbook('notebooks/refactoring-unit-test.ipynb', 
                  execute=['imports', 'model', 'lshapedblock', 
                           'lshapedextrude', 'refactoring-test',
                           'RefactoringTest']) as tb:
        yield tb


def test_model_functionality(tb):
    Model = tb.ref("Model")
    model_instance = Model(10, 20, 30)

    assert model_instance.length == 10
    assert model_instance.width == 20
    assert model_instance.thickness == 30
    # Further assertions
    

    
def test_model_negative_values(tb):
    # Assuming you have a function or code block in your notebook
    # that would raise a ValueError when passed negative dimensions.
    # This code assumes the function call is made in a notebook cell.

    params = [
        (-10, 20, 30),
        (10, -20, 30),
        (10, 20, -30)
    ]

    for param in params:
        injected_code = f"""
            try:
                Model{param}
            except ValueError as e:
                print("Success: ValueError raised as expected")
            """

        # Execute the injected code in the notebook
        tb.inject(injected_code)

        # Fetch the last cell output to see if the exception was caught
        output = tb.cell_output_text(-1)  # Assuming the injected cell is the last one

        # Assert that the output indicates a ValueError was successfully raised
        assert "Success: ValueError raised as expected" in output, "ValueError was expected but not raised or not caught correctly." 
        
        
def test_lshaped_block(tb):
    LShapedBlock = tb.ref("LShapedBlock")
    model_instance = LShapedBlock(120.0, 80.0, 40.0, 40.0, 80.0, 20)

    assert model_instance.length == 120
    assert model_instance.width == 80
    assert model_instance.thickness == 40
    assert model_instance.feature_b_length == 40
    assert model_instance.feature_b_width == 80
    assert model_instance.feature_b_thickness == 20
        
    # Further assertions
    
    
    
def test_lshaped_block_negative_values(tb):
    # Assuming you have a function or code block in your notebook
    # that would raise a ValueError when passed negative dimensions.
    # This code assumes the function call is made in a notebook cell.

    params = [
        (-120.0, 80.0, 40.0, 40.0, 80.0, 20.0),
        (120.0, -80.0, 40.0, 40.0, 80.0, 20.0),
        (120.0, 80.0, -40.0, 40.0, 80.0, 20.0),
        (120.0, 80.0, 40.0, -40.0, 80.0, 20.0),
        (120.0, 80.0, 40.0, 40.0, -80.0, 20.0),
        (120.0, 80.0, 40.0, 40.0, 80.0, -20.0)
    ]

    for param in params:
        injected_code = f"""
            try:
                LShapedBlock{param}
            except ValueError as e:
                print("Success: ValueError raised as expected")
            """

        # Execute the injected code in the notebook
        tb.inject(injected_code)

        # Fetch the last cell output to see if the exception was caught
        output = tb.cell_output_text(-1)  # Assuming the injected cell is the last one

        # Assert that the output indicates a ValueError was successfully raised
        assert "Success: ValueError raised as expected" in output, "ValueError was expected but not raised or not caught correctly." 
        
        
        
        
def test_l_shaped_extrude_creation(tb):
    LShapedExtrude = tb.ref("LShapedExtrude")
    # Instantiate with specific dimensions
    model_instance = LShapedExtrude(120.0, 80.0, 40.0, 40.0, 20.0)

    assert model_instance.length == 120
    assert model_instance.width == 80
    assert model_instance.thickness == 40
    assert model_instance.side_width == 40
    assert model_instance.side_thickness == 20
        
    # Further assertions        


    
def test_lshaped_extrude_negative_values(tb):
    # Assuming you have a function or code block in your notebook
    # that would raise a ValueError when passed negative dimensions.
    # This code assumes the function call is made in a notebook cell.

    params = [
        (-120.0, 80.0, 40.0, 40.0, 20.0),
        (120.0, -80.0, 40.0, 40.0, 20.0),
        (120.0, 80.0, -40.0, 40.0, 20.0),
        (120.0, 80.0, 40.0, -40.0, 20.0),
        (120.0, 80.0, 40.0, 40.0, -20.0)
    ]

    for param in params:
        injected_code = f"""
            try:
                LShapedExtrude{param}
            except ValueError as e:
                print("Success: ValueError raised as expected")
            """

        # Execute the injected code in the notebook
        tb.inject(injected_code)

        # Fetch the last cell output to see if the exception was caught
        output = tb.cell_output_text(-1)  # Assuming the injected cell is the last one

        # Assert that the output indicates a ValueError was successfully raised
        assert "Success: ValueError raised as expected" in output, "ValueError was expected but not raised or not caught correctly."    
        
        
def test_refactoring_test(tb):
    # Create instances of the Model class
    models = {
        "reference": ("LShapedExtrude", (120.0, 80.0, 40.0, 40.0, 20.0)), 
        "tests": [ 
            ("LShapedExtrude", 
             (120.0, 80.0, 40.0, 40.0, 20.0), 
             True, 
             "The models are expected to be identical, but they are not."),
            ("LShapedExtrude", 
             (100.0, 80.0, 40.0, 40.0, 20.0), 
             False, 
             "2The models are expected to be different, but they are not."),
            ("LShapedBlock", 
             (120.0, 80.0, 40.0, 40.0, 80.0, 20.0),  
             True, 
             "3The models are expected to be identical, but they are not."),
            ("LShapedBlock", 
             (100.0, 80.0, 40.0, 40.0, 80.0, 20.0),  
             False, 
             "4The models are expected to be different, but they are not."),
            ("Model", 
             (100, 50, 25),  
             False, 
             "5The models are expected to be different, but they are not.")
        ]
    }
    reference_model = tb.ref(models["reference"][0])(*models["reference"][1])

    # Create an instance of RefactoringTest
    refactoring_test = tb.ref("RefactoringTest")(reference_model)


    for m in models["tests"]:
        refactored_model = tb.ref(m[0])(*m[1])
        # Run the test and capture the result
        test_result = refactoring_test.run(refactored_model)
        print(test_result)
        assert test_result is m[2], m[3]