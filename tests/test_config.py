import configparser


class Configuration:
    """
    Load settings from file.
    """
    def __init__(self, settings_file: str = "test_config.ini") -> object:
        self.config = configparser.ConfigParser()
        self.config.read(settings_file)
        
        self.base_url = self.config["testing"]["base_url"]
        self.username = self.config["testing"]["username"]
        self.password = self.config["testing"]["password"]
