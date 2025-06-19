# Have been going back and forth between whether to just use string literals for some better readability and using auto. Unless there is a reason to need more than a logical grouping, just use auto.
from enum import Enum, auto


class THREADER_CODES(Enum):
    """String literals for Codes the threader can throw"""

    STARTED = "STARTED"
    START = "START"
    STOP = "STOP"
    STOPPED = "STOPPED"

    START_NEW_JOB = "START NEW JOB"
    JOB_PAUSED = "JOB PAUSED"
    JOB_FINISHED = "JOB FINISHED"
    JOB_ERROR = "JOB ERROR"

    LIBRARY_INTERRUPT = "LIBRARY INTERRUPT"
    PYTHON_INTERRUPT = "PYTHON INTERRUPT"

    ATTEMPT_FAILED = "ATTEMPT FAILED"
    REATTEMPT_TASK = "REATTEMPT JOB"
    NO_REATTEMPT = "NO REATTEMPT"
    ERROR_SHUTDOWN = "ERROR SHUTDOWN"
    _NONE = "NONE"


class COUNTER_TYPES(Enum):
    """List of Counter types"""

    THREADER = "Threader Counter"
    WORKER = "Worker Counter"
    TASK = "Task Counter"
    ERROR = "Error Counter"
    SESSION = "Session Counter"
    JOB = "Job Counter"


class THREADER_TYPES(Enum):
    """List of Threader types"""

    MASTER_THREADER = auto()
    CO_MASTER = auto()
    WORKER_THREADER = auto()

    # Thread group for testing, wasn't sure if needed
    TEST_THREAD = auto()


class PROCESS_TYPE(Enum):
    """List of process types"""

    MASTER_PROCESS = auto()
    CO_PROCESS = auto()
    CHILD_PROCESS = auto()

    # Process group for testing, wasn't sure if needed
    TEST_PROCESS = auto()
