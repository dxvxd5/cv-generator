from sections.cv import CV

MINIMAL_USER = {
    "firstName": "Ada",
    "lastName": "Lovelace",
    "city": "London",
    "country": "United Kingdom",
    "email": "ada@example.com",
}


def test_cv_defaults_missing_sections_to_empty_lists():
    cv = CV(user=MINIMAL_USER)
    assert cv.education == []  # nosec B101
    assert cv.experiences == []  # nosec B101
    assert cv.projects == []  # nosec B101
    assert cv.skills == []  # nosec B101


def test_cv_keeps_provided_sections():
    cv = CV(
        user=MINIMAL_USER,
        skills=[{"area": "Languages", "skills": ["Python"]}],
    )
    assert cv.education == []  # nosec B101
    assert len(cv.skills) == 1  # nosec B101
    assert cv.skills[0].area == "Languages"  # nosec B101
