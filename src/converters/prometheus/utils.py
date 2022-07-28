def to_period(start_date: str | int, end_date: str | int):
    return f"{start_date} - {end_date}"


def to_location(city: str, country: str):
    return f"{city}, {country}"


def to_with_location(label: str, location: str):
    return f"{label} - {location}"
