class User:
    def __init__(self, **kwargs):
        self.city: str = kwargs["city"]
        self.country: str = kwargs["country"]
        self.first_name: str = kwargs["firstName"]
        self.last_name: str = kwargs["lastName"]
        self.email: str = kwargs["email"]
        self.linkedin_url: str = kwargs.get("linkedinUrl", "")
        self.github_url: str = kwargs.get("githubUrl", "")
        self.github_username: str = kwargs.get("githubUsername", "")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def location(self) -> str:
        return f"{self.city}, {self.country}"
