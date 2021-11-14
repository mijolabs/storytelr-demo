import configparser


class Configuration:
    """
    Load settings from file.
    """
    def __init__(self, settings_file: str = "storytelr.ini") -> object:
        self.config = configparser.ConfigParser()
        self.config.read(settings_file)
        
        self.title = self.config["common"]["title"]
        self.username = self.config["common"]["username"]
        self.password = self.config["common"]["password"]
        self.id_length = int(self.config["common"]["id_length"])
        self.validity_days = int(self.config["common"]["validity_days"])
        self.validity_seconds = self.validity_days * 86400
        self.min_length = int(self.config["common"]["min_length"])
        self.max_length = int(self.config["common"]["max_length"])
        
        self.redis = self.config["redis"]
