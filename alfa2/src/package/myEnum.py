from enum import Enum

class Status(Enum):
    """
        Enum for different status that can in program appears.
    """
    ERROR='error'
    SUCCESS='success'

class Mode(Enum):
    """
        Enum for different modes that can by in program called.
    """
    ENCODE='encode'
    DECODE='decode'
    LOGS='logs'
    def get_values():
        """
        public Method that returns value of all attributes. 
        """
        return [
            Mode.DECODE.value,
            Mode.ENCODE.value,
            Mode.LOGS.value
        ]