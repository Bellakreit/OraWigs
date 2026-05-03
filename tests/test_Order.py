import pytest
from Order import buildEmailBody

#testing order page, pytest tests/test_Order.py -v

def test_build_email_body_success():  # just making sure it takes the info in
    result = buildEmailBody("brown", "12", "straight", "European(finer/silky)", "Full lace", "no lining", "55", "13", "14")
    assert "brown" in result
    assert "12 inches" in result
    assert "55 cm" in result

def test_build_email_body_empty_field():  # if even one field is empty
    with pytest.raises(ValueError):
        buildEmailBody("", "12", "straight", "European(finer/silky)", "Full lace", "no lining", "55", "13", "14")