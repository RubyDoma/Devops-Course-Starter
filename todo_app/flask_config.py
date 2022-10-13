


class Config:
    def __init__(self):
        """Base configuration variables."""
        if not self.SECRET_KEY:
           raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")