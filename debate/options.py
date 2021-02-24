GEO_LOCATION = (
    ("SA", "South America"),
    ("NA", "North America"),
    ("AS", "Asia"),
    ("AF", "Africa"),
    ("EU", "Europe"),
)

LANGUAGE = (
    ('pt-br', "Português do Brasil"),
    ('en', "English")
)

class OptionSingleton:
    '''Room Options'''

    OPTIONS_LOADED = False
    CERTFILE = 'certfile.pem'
    KEYFILE = 'certfile.key'
    AUDIENCE_MIN = 0  # Min amount of participants per room
    AUDIENCE_MAX = 0  # Max amount of participants per room
    AUDIENCE_PERCENT_SCORE = 0.0  # Percentile of score count audience can reach
    GEO_LOCATION = ""  # Geo Location
    LANGUAGE = ""  # U18N Language

    def get_config_from_file(self, file="config.ini"):
        '''Load configuration from INI file'''
        pass

options = OptionSingleton()