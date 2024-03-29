from unittest.mock import patch, MagicMock
import pytest
from testbook import testbook


@testbook('notebooks/refactoring-unit-test.ipynb', execute=['imports', 'model'])
def test_model_functionality(tb):
    Model = tb.ref("Model")
    model_instance = Model(10, 20, 30)

    assert model_instance.length == 10
    assert model_instance.width == 20
    assert model_instance.thickness == 30
    # Further assertions
        
        
@testbook('notebooks/refactoring-unit-test.ipynb', execute=['imports', 'model', 'lshapedblock'])
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
        
        
@testbook('notebooks/refactoring-unit-test.ipynb', execute=['imports', 'model', 'lshapedextrude'])
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

