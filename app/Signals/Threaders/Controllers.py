from typing import Optional, Generator, NamedTuple
from threading import Thread
from dataclasses import dataclass, field
from abc import ABCMeta, abstractmethod
from Constants import CONTROLLER_TYPES
from queue import PriorityQueue
from uuid import UUID, uuid4


class Controller(metaclass=ABCMeta):
    """_summary_
    Controller class is an ABSTRACT BASE CLASS

    _description_
    Uses to ABCMeta as the metaclass for Counter types. Subclassing different counter objects from this class as a convenience.

    NOTE:Conventions used are "_" indicates that the variable is should really be handled or changed in this class. "CAPITALIZATION" is a constant.Possible refactoring can be done to use the attrs library instead of dataclass for improved flexibility, if needed

    """

    val: int

    step: int

    max: int

    min: int

    threader: Optional[str]

    _name: str

    _COUNT_TYPE: CONTROLLER_TYPES

    _IDENTITY: UUID

    @abstractmethod
    def __post_init__(self) -> None:
        """_summary_
        These controllers need to be able to send information back to the threader. Here is where final set up is done where we can link the
        """
        pass

    @abstractmethod
    def __increment__(self, scalar: int) -> Optional[Generator[int, None, None]]:
        """_summary_
        The formal interface for the ThreadCounter class must implement a function that defines a generator that takes an integer to increment or decrement the counter by handling options and things are handled in a function wrapping this one.

        NOTE:This is an abcmetaclass object that inherits from type. Abstracts complicated type-related meta. Will throw an error if you implement the counter wrong. If running MyPy, static checking will reinforce class signatures.

        Args:
        scalar -> int:

        _description_
        Takes an optional integer to move the counter up or down by.

        Returns:
            Optional[Generator[int,None,None]]: This is literally how to write the return type for the generator

            _description_
            The counter "lazy loads" the next value from the Generator function. May be None.
        """
        pass

    @abstractmethod
    def load_controller(self) -> None:
        """_summary_
        The formal interface requires a function that loads relevant threader information - triggers, errors, callbacks, etc. - into a Priority Queque for the threader to process.
        """
        pass

    @classmethod
    def __subclasscheck__(cls, subclass: type) -> bool:
        """_summary_
        Checks the subclass to identify that they are of the same type. If multiple controller are used, checks can be done to discriminate between the controller.

        NOTE: Other Controller could be Retry Controller for controlling reattempt behavior, Session Controller to track on going user sessions, and Error Controller for capturing information on errors happening in individual threads.

        Args:
            subclass -> type:
            _description_
            The class that is being checked.

        Returns:
            bool
        """
        return (
            hasattr(subclass, "__increment__")
            and callable(subclass.__increment__)
            and hasattr(subclass, "val")
            and hasattr(subclass, "step")
            and hasattr(subclass, "max")
            and hasattr(subclass, "min")
            and hasattr(subclass, "_name")
            and hasattr(subclass, "_COUNT_TYPE")
            and hasattr(
                subclass,
                "_IDENTITY",
            )
        )


# Thread Counter Implementation
@dataclass(slots=True, order=True)
class ThreadController(Controller):
    """ThreadController is an implementation of the Counter class"""

    # Additional Identification Variables
    _IDENTITY: UUID = field(init=True, default_factory=uuid4)

    _CONTROLLER_TYPE: CONTROLLER_TYPES = CONTROLLER_TYPES.THREAD

    # Threader Components
    threader: Optional[str] = None

    thread_PQ: Optional[PriorityQueue] = None

    # Basic Defaults for the Thread Counter
    name: str = (
        field(init=True, default=f"{_CONTROLLER_TYPE}:\t{_IDENTITY}")
        if threader is None
        else field(init=True, default=f"Thread Controller {_IDENTITY} of {threader}")
    )

    val: int = 1

    min: int = 0

    step: int = 1

    max: int = 10

    def __post_init__(self) -> None:
        # TODO: Implement the __post_init__ function to attach the Priority Queue to the

        pass

    def __increment__(self, scalar: int) -> Generator[int, None, None]:

        if self.min >= self.val:
            raise ValueError(
                "Threader attempted to decremenet below minimum value. Closing Thread Resource"
            )

        elif self.val == self.max:
            raise ValueError(
                "Threader attempted to increment above maximum value. Waiting until thread can be initialized"
            )

        elif self.val > self.max:
            raise ValueError(
                "Thread attempting initializing too many threads. Shutting threader down"
            )

        while self.min < self.val < self.max:
            self.val += scalar
            yield self.val

    # Wrapping the __increment__ function to encapsulate optional logic handling

    def scale(self, adjustment: Optional[int] = None) -> None:
        """Scale the counter up and down"""

        adjust = adjustment if adjustment is not None else self.step
        self.val = next(self.__increment__(adjust))

    def load_controller(self) -> None:
        """Load data to Threader"""
        # TODO: Implement load_counter_info to
        pass
