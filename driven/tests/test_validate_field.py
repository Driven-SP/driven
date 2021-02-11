from driven.db import get_db

import pytest

@pytest.fixture
def validate_field_test():
    pass

def test_simple():
    assert 1+1==2, "one plus one is two"

