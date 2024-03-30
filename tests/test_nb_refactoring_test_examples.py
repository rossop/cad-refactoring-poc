from unittest.mock import patch, MagicMock
import pytest
from testbook import testbook


@pytest.fixture(scope='module')
def tb():
    """
    A pytest fixture that sets up a Testbook environment by initialising a session
    with a specific Jupyter notebook. This fixture ensures the notebook is executed
    within a controlled test context, facilitating the testing of notebook cells and
    the Python objects they define. It's scoped to 'module', meaning the setup occurs
    once per test module, not for every test function, improving test suite efficiency.

    This particular setup executes a series of initial cells that are essential for
    the subsequent tests. These cells import necessary Python modules and define various
    classes that are under test, such as Model, LShapedBlock, LShapedExtrude, and the
    mechanisms for refactoring tests. By doing so, it prepares the notebook environment
    by ensuring all dependencies and definitions are loaded and available for testing.

    The fixture utilises the 'with' statement to manage the lifecycle of the Testbook
    client, ensuring resources are properly managed and the notebook session is closed
    after the tests complete. The 'execute' parameter explicitly lists the cells to run
    upon fixture initialisation, targeting only those necessary for the test context and
    thus optimising the test setup process.

    Returns:
        testbook.testbook.TestbookNotebookClient: An instance of the Testbook client
        preconfigured with the notebook environment, ready for interaction in test cases.
    
    Usage:
        The fixture is automatically applied to test functions within the same module
        that declare 'tb' as an argument. It abstracts the notebook setup process, allowing
        test functions to focus on asserting behaviours and outcomes.

    Note:
        This fixture is designed for use in a testing suite focused on verifying the
        functionality and integrity of notebook-defined Python objects and their interactions.
        It is an integral part of a testing strategy that incorporates notebooks as first-class
        citizens in software development and testing practices.
    """
    with testbook('notebooks/refactoring-unit-test.ipynb', 
                  execute=['imports', 'model', 'lshapedblock', 
                           'lshapedextrude', 'refactoring-test', 
                           'RefactoringTest']) as tb:
        yield tb


def test_model_functionality(tb):
    """
    Verifies the initialisation and attribute accuracy of the Model class. This test
    confirms that the Model instance is correctly initialised with specified dimensions 
    and that these dimensions are accurately reflected in the instance attributes.

    This function specifically tests:
    - The successful creation of a Model instance with predetermined dimensions.
    - Correct assignment of length, width, and thickness attributes based on the input 
      parameters provided during initialisation.

    Assertions made in this test:
    - The length attribute of the model instance equals 10.
    - The width attribute of the model instance equals 20.
    - The thickness attribute of the model instance equals 30.

    These assertions collectively ensure the Model class's fundamental functionality 
    related to initialisation and attribute management is operating as expected.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): A testbook client instance, 
            providing the interface to interact with and execute code within a 
            Jupyter notebook environment.

    Note:
    The test assumes the 'Model' class and its initialisation logic are correctly 
    implemented and accessible within the notebook referenced by the 'tb' client. 
    Further assertions, beyond those for basic attribute checks, could include 
    validations of the model's internal state or behaviour as appropriate for 
    comprehensive testing.
    """
    Model = tb.ref("Model")
    model_instance = Model(10, 20, 30)
    assert model_instance.length == 10
    assert model_instance.width == 20
    assert model_instance.thickness == 30
    # Further assertions could include checking the model's internal representation.
    

@pytest.mark.parametrize("dimensions, expected_exception", [
    ((-10, 20, 30), 'ValueError'),
    ((10, -20, 30), 'ValueError'),
    ((10, 20, -30), 'ValueError'),
    ((10, 20,   0), 'ValueError'),
    ((10,   0, 30), 'ValueError'),
    ((  0, 20, 30), 'ValueError')
])

def test_model_negative_values(tb, dimensions, expected_exception):
    """
    Ensures that attempting to initialise the Model class with any negative
    dimensions results in a ValueError. This test affirms the robustness of
    the model's validation logic, which is designed to reject invalid
    states that would not make sense in a physical or CAD environment.

    The test operates by dynamically injecting Python code into a Jupyter
    notebook environment using the testbook client. The injected code
    attempts to create an instance of the Model class with a set of
    dimensions, some of which are negative, to trigger a ValueError.
    The test asserts whether the ValueError is correctly raised as
    anticipated, ensuring the integrity of the model's initialisation logic.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): A client instance for
            interacting with and executing code within a Jupyter notebook.
        dimensions (tuple): A tuple representing the dimensions (length, width,
            height) with which an attempt to initialise the Model class will
            be made. The test cases include negative values to test the
            validation logic.
        expected_exception (str): The name of the exception expected to be
            raised by attempting to initialise the model with invalid
            dimensions. This is hard-coded as 'ValueError' for all test cases,
            reflecting the expected behaviour of the Model class when faced
            with invalid input.

    The function utilises the pytest framework to parametrise the test, enabling
    multiple sets of dimensions to be tested in a single test function. This
    approach enhances test coverage and efficiency by consolidating similar
    validation checks into a streamlined testing process.
    """
    code = f"""
        try:
            Model{dimensions}
            print("No Error")  # This line should not be reached if ValueError is raised
        except ValueError:
            print("ValueError raised as expected")
        """

    tb.inject(code)
    output = tb.cell_output_text(-1)  # Assumes the injected code cell is the last cell
    assert expected_exception in output, "ValueError was not raised when expected"
        
        
def test_lshaped_block(tb):
    """
    Validates the LShapedBlock class's ability to correctly initialise and create
    an L-shaped block model with specified dimensions. This test checks if the class
    successfully assigns the provided dimensions to its attributes and potentially
    constructs the correct L-shaped block representation in the CadQuery environment.

    The test instantiates the LShapedBlock class with a predefined set of dimensions
    and asserts that the initialised object accurately reflects these dimensions through
    its length, width, thickness, feature_b_length, feature_b_width, and feature_b_thickness
    attributes. The purpose is to ensure the class's initialisation logic accurately
    handles input values and correctly sets up the model for further operations.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): A client instance for interacting
            with and executing code within a Jupyter notebook. It provides access to the
            notebook's environment and allows for testing code defined in notebook cells.

    The test could be extended with further assertions to examine the internal representation
    of the model within the CadQuery environment, ensuring that not only the attributes are
    correctly set but also the model's geometry accurately represents an L-shaped block.
    This would require interacting with CadQuery's API to inspect the constructed geometry.
    """
    LShapedBlock = tb.ref("LShapedBlock")
    model_instance = LShapedBlock(120.0, 80.0, 40.0, 40.0, 80.0, 20)
    assert model_instance.length == 120
    assert model_instance.width == 80
    assert model_instance.thickness == 40
    assert model_instance.feature_b_length == 40
    assert model_instance.feature_b_width == 80
    assert model_instance.feature_b_thickness == 20
    # Further assertions could include checking the model's internal representation.
    

@pytest.mark.parametrize("dimensions, expected_exception", [
    ((-120.0, 80.0, 40.0, 40.0, 80.0, 20.0), 'ValueError'),
    ((120.0, -80.0, 40.0, 40.0, 80.0, 20.0), 'ValueError'),
    ((120.0, 80.0, -40.0, 40.0, 80.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, -40.0, 80.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 40.0, -80.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 40.0, 80.0, -20.0), 'ValueError'),
    ((0, 80.0, 40.0, 40.0, 80.0, 20.0), 'ValueError'),
    ((120.0, 0, 40.0, 40.0, 80.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 0, 40.0, 80.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 0, 80.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 40.0, 0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 40.0, 80.0, 0), 'ValueError')
    
])

def test_lshaped_block_negative_values(tb, dimensions, expected_exception):
    """
    Ensures the LShapedBlock class adheres to its constraint that all dimensions
    must be positive by testing its initialisation with negative values for each
    dimension in turn. This test iterates over a set of dimensions, injecting code
    into a Jupyter notebook environment to initialise an LShapedBlock instance with
    these dimensions and catching the expected ValueError.

    Utilising the pytest's parametrize decorator, this function systematically
    verifies the model's robustness against invalid input, specifically negative
    values, which should not be permissible for the physical dimensions of a CAD
    model. The test provides coverage for each dimension individually, ensuring
    comprehensive validation.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): A client for interacting with
            and executing code within a Jupyter notebook, facilitating the test of
            code in a live notebook environment.
        dimensions (tuple): A tuple of six floats representing the dimensions to
            instantiate the LShapedBlock model with. This includes the length, width,
            thickness of the main block, and the length, width, and thickness of
            the feature block (feature_b).
        expected_exception (str): The type of exception expected to be raised by
            attempting to instantiate the model with invalid (negative) dimensions.
            This is hard-coded to 'ValueError' as the test expects this specific
            exception to be raised for negative dimension values.

    The test dynamically injects Python code into the notebook to attempt model
    instantiation with the provided dimensions and explicitly checks for the
    raising of a ValueError. It asserts that such an exception is indeed raised,
    with the output message confirming this, thus ensuring that the class properly
    validates its inputs against invalid (negative) dimensions.
    """
    code = f"""
        try:
            LShapedBlock{dimensions}
            print("No Error")  # This line should not be reached if ValueError is raised
        except ValueError:
            print("ValueError raised as expected")
        """

    tb.inject(code)
    output = tb.cell_output_text(-1)  # Assumes the injected code cell is the last cell
    assert expected_exception in output, "ValueError was not raised when expected"

        
        
def test_l_shaped_extrude_creation(tb):
    """
    Evaluates the LShapedExtrude class's ability to accurately instantiate an L-shaped
    block model through an extrusion process. This test confirms that the class not
    only correctly interprets the dimensions provided at instantiation but also
    constructs the model in accordance with these dimensions. It further verifies
    that essential attributes of the model, such as length, width, thickness,
    side width, and side thickness, match the expected values based on the input
    parameters. This ensures the class's reliability in creating geometrically
    precise and dimensionally accurate models, which is critical for any CAD
    applications relying on accurate model representations.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): An instance of the testbook
            client. This facilitates interaction with and execution of code within
            the Jupyter notebook, allowing direct testing of notebook-defined classes
            and functions.

    The test specifically asserts the correctness of:
    - Model's length: Ensuring it matches the specified horizontal length of the L shape.
    - Model's width: Verifying it aligns with the vertical length of the L shape.
    - Model's thickness: Checking it reflects the thickness of the extruded shape.
    - Side width: Confirming it equals the defined height difference between the vertical sides.
    - Side thickness: Ensuring it matches the width of the L shape's sides.

    These assertions collectively confirm the class's capability to accurately
    model an L-shaped extruded block, which is fundamental for precise 3D modelling
    and simulations in engineering and design applications.
    """
    LShapedExtrude = tb.ref("LShapedExtrude")
    model_instance = LShapedExtrude(120.0, 80.0, 40.0, 40.0, 20.0)
    assert model_instance.length == 120
    assert model_instance.width == 80
    assert model_instance.thickness == 40
    assert model_instance.side_width == 40
    assert model_instance.side_thickness == 20
    # Further assertions could include checking the model's internal representation 


@pytest.mark.parametrize("dimensions, expected_exception", [
    ((-120.0, 80.0, 40.0, 40.0, 20.0), 'ValueError'),
    ((120.0, -80.0, 40.0, 40.0, 20.0), 'ValueError'),
    ((120.0, 80.0, -40.0, 40.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, -40.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 40.0, -20.0), 'ValueError'),
    ((0, 80.0, 40.0, 40.0, 20.0), 'ValueError'),
    ((120.0, 0, 40.0, 40.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 0, 40.0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 0, 20.0), 'ValueError'),
    ((120.0, 80.0, 40.0, 40.0, 0), 'ValueError')
])

def test_lshaped_extrude_negative_values(tb, dimensions, expected_exception):
    """
    Verifies that the LShapedExtrude class correctly raises a ValueError when 
    initialised with negative dimensional values. This test dynamically injects 
    Python code into a Jupyter notebook using the testbook library, attempting 
    to instantiate an LShapedExtrude object with specified dimensions. The test 
    expects a ValueError to be raised if any of the dimensions are negative, 
    reflecting the class's input validation mechanism.

    The approach taken here allows for testing the behaviour of notebook-defined 
    classes in response to invalid inputs, directly within their development 
    environment. It also demonstrates a method for interacting with Jupyter 
    notebook content programmatically in a testing context.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): A testbook client instance, 
            providing an interface to execute and interact with Jupyter notebook 
            content within test functions.
        dimensions (tuple): A tuple representing the dimensions to be used when 
            attempting to instantiate the LShapedExtrude class. Negative values 
            within this tuple are intended to trigger the expected ValueError.
        expected_exception (str): A string indicating the type of exception that 
            is expected to be raised by the test code. In this case, it should 
            always be 'ValueError', reflecting the specific error condition being 
            tested.

    This test serves both as a validation of input handling within the 
    LShapedExtrude class and as an example of applying dynamic code injection 
    techniques for testing Jupyter notebook-based software components. It 
    highlights the importance of robust input validation in software design, 
    particularly in the context of CAD modelling where geometric dimensions 
    must adhere to logical constraints.
    """
    
    code = f"""
        try:
            LShapedExtrude{dimensions}
            print("No Error")  # This line should not be reached if ValueError is raised
        except ValueError:
            print("ValueError raised as expected")
        """

    tb.inject(code)
    output = tb.cell_output_text(-1)  # Assumes the injected code cell is the last cell
    assert expected_exception in output, "ValueError was not raised when expected"


@pytest.fixture(scope='module')
def reference_model(tb):
    """
    A pytest fixture that provides a reference model instance for testing.

    This fixture uses the `testbook` library to interact with a Jupyter notebook
    where the `LShapedExtrude` class is defined. It initialises an instance of
    `LShapedExtrude` with a predefined set of dimensions, suitable for use as
    a reference model in various test cases. The instance is created once per
    test session ('module' scope) to ensure efficiency in testing.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): The testbook client instance
        provided by the `testbook` pytest fixture. It is used to access and execute
        code within the target Jupyter notebook.

    Returns:
        An instance of the `LShapedExtrude` class, initialised with specific dimensions,
        ready for use in tests that require a reference model for comparison or further
        operations.
    
    Usage:
        This fixture is automatically used by pytest when included as a parameter in
        a test function. It simplifies the test setup process by abstracting the model
        instantiation logic.
    """
    ModelClass = tb.ref("LShapedExtrude")
    return ModelClass(120.0, 80.0, 40.0, 40.0, 20.0)



@pytest.mark.parametrize("model_class, dims, expected_result, failure_message", [
    ("LShapedExtrude", (120.0, 80.0, 40.0, 40.0, 20.0), 
        True, 
        "Expected identical models."),
    ("LShapedExtrude", (100.0, 80.0, 40.0, 40.0, 20.0), 
        False, 
        "Expected different models."),
    ("LShapedBlock", (120.0, 80.0, 40.0, 40.0, 80.0, 20.0), 
        True, 
        "Expected different models because of feature_b_thickness."),
    ("LShapedBlock", (100.0, 80.0, 40.0, 40.0, 80.0, 20.0), 
        False, 
        "Expected different models because of length."),
    ("Model", (100, 50, 25), 
        False, 
        "Expected different models due to basic model comparison."),
])
def test_refactoring_test(tb, reference_model, model_class, dims, expected_result, failure_message):
    """
    This test function leverages the pytest.mark.parametrize decorator to execute 
    a series of comparisons between a reference model and various model instances. 
    It assesses both geometric and locational equivalences of CAD models by invoking 
    the RefactoringTest's `run` method with different sets of model dimensions 
    and types. This approach aims to validate the integrity and effectiveness 
    of the refactoring process, ensuring that model refactoring does not inadvertently 
    alter the essential attributes or behavior of the models.

    Parameters:
        tb (testbook.testbook.TestbookNotebookClient): The testbook client 
            instance used to interact with and execute code in the Jupyter 
            notebook environment.
        reference_model (Model): An instance of the model class that serves as 
            the baseline for comparison with other refactored models.
        model_class (str): The class name of the model being tested. This 
            parameter specifies which model class to instantiate and compare 
            against the reference model.
        dims (tuple): A tuple containing the dimensions to be used for creating 
            the model instance. These dimensions are passed directly to the model 
            class constructor.
        expected_result (bool): The expected result of the comparison. A value 
            of True indicates that the models are expected to be geometrically 
            and locationally equivalent, while False indicates expected differences.
        failure_message (str): The message to be displayed in case the test fails, 
            providing context about the expected outcome versus the actual test result.

    The test dynamically creates an instance of the specified model class with 
    the given dimensions, then performs a refactoring test comparison against 
    the reference model. It asserts that the outcome of the comparison matches 
    the expected result, utilising the failure_message for enhanced clarity in 
    test reporting.
    """
    RefactoringTestClass = tb.ref("RefactoringTest")
    refactoring_test_instance = RefactoringTestClass(reference_model)
    
    ModelClass = tb.ref(model_class)
    model_instance = ModelClass(*dims)
    
    test_result = refactoring_test_instance.run(model_instance)
    assert test_result is expected_result, failure_message