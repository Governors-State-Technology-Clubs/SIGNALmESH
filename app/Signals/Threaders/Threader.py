from threading import Thread, ThreadError, Lock
from typing import Optional, List, NamedTuple
from dataclasses import dataclass, field
from abc import ABCMeta, abstractmethod
from Constants import THREADER_TYPES
from queue import PriorityQueue
from Counters import ThreadCounter
import uuid


class Threader(Thread, metaclass=ABCMeta):
    """Formal Threader interface class. Inherits from threading.Thread class and uses ABCMeta as the metaclass"""

    _THREADER_TYPE: THREADER_TYPES

    _THREADER_ERROR: ThreadError

    _IDENTITY: uuid.UUID

    _thread_counter: Optional[ThreadCounter]

    _threader_PQ: PriorityQueue

    _thread_list: List[NamedTuple]

    _name: str

    _thread_val: int

    _thread_step: int

    _thread_max: int

    _thread_min: int

    _thread_lock: Lock


# Threader Implementation
@dataclass(slots=True, order=True)
class MasterThreader(Threader):
    "MasterThreader class inherits from the Threader Abstract Base Class"

    # default behaivor when instance is called like a function
    def __call__(self):
        # TODO: Make default behaivor
        pass

    def threadGenerate(self, _thread_list: List[NamedTuple]) -> List[NamedTuple]:
        """Generate a list of tuples"""
        # TODO:Implement thread_generate function
        # Create thread and generate

        return []

    # Additional Identification
    _IDENTITY: uuid.UUID = field(init=True, default_factory=uuid.uuid4)

    _THREADER_TYPE: THREADER_TYPES = THREADER_TYPES.MASTER_THREADER

    # Basic Default Variables for Master Threaders
    _name: str = field(init=True, default=f"{_THREADER_TYPE}:\t{_IDENTITY}")

    _threader_PQ: PriorityQueue = PriorityQueue(maxsize=15)

    _THREAD_LOCK: Lock = Lock()

    _THREADER_ERROR: ThreadError = ThreadError()

    _thread_obj: Thread = Thread(
        target=threadGenerate, name=f"Child Thread of :{_name}", args=(_threader_PQ,)
    )

    _thread_counter: Optional[ThreadCounter] = ThreadCounter(
        threader_parent=_thread_obj,
        thread_counter_PQ=_threader_PQ,
    )

    _thread_list: List[NamedTuple] = []

    # TODO: Test and debug MasterThreader implementation
    # Handle emitted errors from ThreadCounter
    # Implement WorkerThreader
    # Implement thread_generate function
    # Attach Priority Queue to subordinate threads

    @classmethod
    def getThreader(cls, id: uuid.UUID) -> Optional[NamedTuple]:
        # TODO: Make class method to search for threads by _IDENTITY
        pass

    def getPQ(self) -> PriorityQueue:
        return self._threader_PQ


# Threader implementation
class WorkerThreader(Threader):
    # TODO:
    pass
