from enum import Enum

class Status(Enum):
    UNEXECUTED = -1
    PASS = 1
    FAIL = 2
    WIP = 3
    BLOCKED = 4
    PARTIALLY_PASSED = 5
    NOT_IMPLEMENTED = 6
