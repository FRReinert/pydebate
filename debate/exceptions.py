class BaseCommandException(Exception):
    '''Generic command exception'''

    def __init__(self, argument):
        self.argument = argument
    
    def __str__(self):
        return f"Generic command Error. Arguments: {self.argument}"


class ArgumentNotFound(BaseCommandException):
    '''Command Error: Argument not found'''
    
    def __str__(self):
        return f"Argument not found: <{self.argument}>"
