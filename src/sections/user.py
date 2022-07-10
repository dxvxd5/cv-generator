from utils.json import check_dict


class User:
    expected_fields = [
        "city",
        "country",
        "firstName",
        "lastName",
        "email",
        "linkedinUrl",
        "githubUrl",
        "githubUsername",
    ]

    def __init__(self, **kwargs):
        check_dict(self.expected_fields, kwargs)

        self.user: str = kwargs["user"]
        self.city: str = kwargs["city"]
        self.country: str = kwargs["country"]
        self.first_name: str = kwargs["firstName"]
        self.last_name: str = kwargs["lastName"]
        self.email: str = kwargs["email"]
        self.linkedin_url: str = kwargs["linkedinUrl"]
        self.github_url: str = kwargs["githubUrl"]
        self.github_username: str = kwargs["githubUsername"]
