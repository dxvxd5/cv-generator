import pytest

from utils.json import check_dict


@pytest.fixture
def complete_education():
    return {
        "startDate": 2018,
        "endDate": 2022,
        "city": "Valence",
        "country": "France",
        "school": "Grenoble INP Esisar",
        "degree": "Master degree, Computer Science, Cybersecurity, Networks",
        "description": ["Major: Computer Science and networks", "Minor: Cybersecurity"],
    }


@pytest.fixture
def imcomplete_education():
    return {
        "startDate": 2018,
        "endDate": 2022,
        "city": "Valence",
        "country": "France",
    }


@pytest.fixture
def expected_education_fields():
    return [
        "startDate",
        "endDate",
        "city",
        "country",
        "school",
        "degree",
        "description ",
    ]


def test_check_dict_complete(expected_education_fields, complete_education):
    assert check_dict(expected_education_fields, complete_education)


def test_check_dict_imcomplete(expected_education_fields, imcomplete_education):
    with pytest.raises(ValueError):
        check_dict(expected_education_fields, imcomplete_education)
