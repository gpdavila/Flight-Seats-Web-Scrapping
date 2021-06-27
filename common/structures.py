from enum import Enum

#mapping HTML references to seats letter
column_group = {'A': 0, 'B': 0, 'C': 0, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 2,'J': 2, 'K': 2}
column_seat = {'A': 0, 'B': 1, 'C': 2, 'D': 0, 'E': 1, 'F': 2, 'G': 3, 'H': 0,'J': 1, 'K': 2}

class ErrorMessage(Enum):
    INVALID = "Oops! Looks like this seat does not exist."
    OCCUPIED = "Oops! Looks like this seat is taken."

class MyError(Exception):
    # Constructor or Initializer
    def __init__(self, value):
        self.value = value
  
    # __str__ is to print() the value
    def __str__(self):
        return(self.value.value)
    