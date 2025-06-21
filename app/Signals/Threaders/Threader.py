from threading import Thread, ThreadError, Lock
from typing import Optional, List, NamedTuple
from dataclasses import dataclass, field
from abc import ABCMeta, abstractmethod
from Constants import THREADER_TYPES
from queue import PriorityQueue
from Controllers import ThreadController
from uuid import UUID, uuid4


class Threader(Thread, metaclass=ABCMeta):
    """Formal Threader interface class. Inherits from threading.Thread class and uses ABCMeta as the metaclass"""

    _IDENTITY: UUID

    _THREADER_TYPE: THREADER_TYPES

    name: str

    thread_val: int

    thread_step: int

    thread_max: int

    thread_min: int

    queue_size: Optional[int]

    work_thread: Optional[function]

    threader_PQ: Optional[PriorityQueue]

    _thread_list: List[NamedTuple]

    _THREAD_CONTROLLER: Optional[ThreadController]

    @abstractmethod
    def __post_init__(self) -> None:
        """Implement any additional setup or actions that class should handle after the instance has been created"""
        pass

    @abstractmethod
    def worker(self, func: function, threader_queue: PriorityQueue) -> None:
        """Implement a wrapper or decorator for injected functions"""
        pass

    @abstractmethod
    def generate_worker(self) -> None:
        """Implement a function that generates the worker thread"""
        pass

    @abstractmethod
    def add_worker(self) -> None:
        """Implement a function that takes the generated worker and adds it to a List of NamedTuples"""
        pass


#  Master Threader Implementation
@dataclass(slots=True, order=True)
class MasterThreader(Threader):
    "MasterThreader class inherits from the Threader Abstract Base Class"

    # Whether or not this function is needed is TBD
    def __post_init__(self) -> None:
        pass

    def getThread(self, id: UUID, name: str) -> Optional[NamedTuple]:
        # TODO: Make method to search for threads by _IDENTITY. NOTE: Intention naive implementation of for loops
        pass

    def worker(self, func: function, threader_queue: PriorityQueue) -> None:
        # TODO: Make an internal Thread decorator for thread functions
        pass

    def generate_worker(self) -> None:
        """Create and start work thread"""
        thread: Thread = Thread(
            target=self.worker, name=self.name, args=(self.threader_PQ,)
        )

    def add_worker(self) -> None:
        pass

    def getPQ(self) -> Optional[PriorityQueue]:
        return self.threader_PQ

    def generate_PQ(self) -> None:
        self.threader_PQ = PriorityQueue(maxsize=15)

    # Additional Identification
    _IDENTITY: UUID = field(init=False, default_factory=uuid4)

    _THREADER_TYPE: THREADER_TYPES = field(
        init=True, default=THREADER_TYPES.MASTER_THREADER
    )

    # Basic Default Variables for Master Threaders
    name: str = field(init=True, default=f"{__name__} {_THREADER_TYPE}:\t{_IDENTITY}")

    thread_val: int = field(init=False, default=1)

    thread_step: int = field(init=True, default=1)

    thread_max: int = field(init=True, default=10)

    thread_min: int = field(init=True, default=0)

    queue_size: Optional[int] = None

    work_thread: Optional[function] = None

    threader_PQ: Optional[PriorityQueue] = None

    _thread_list: List[NamedTuple] = field(init=False, default=[])

    # Threader Constants
    _THREAD_LOCK: Lock = Lock()

    _THREAD_ERROR: ThreadError = ThreadError()

    _THREAD_CONTROLLER: Optional[ThreadController] = ThreadController(
        threader=name, val=thread_val, step=thread_step, max=thread_max, min=thread_min
    )
    # TODO: Test and debug MasterThreader implementation
    # Handle emitted errors from ThreadCounter
    # Implement SubThreader
    # Implement thread_generate function


# SubThreader implementation
class SubThreader(Threader):
    # TODO: Create Implementation of a subThreader
    pass
