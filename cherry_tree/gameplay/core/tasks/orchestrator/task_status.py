""""Class responsible to organize status from tasks"""

from enum import Enum


class TaskStatus(Enum):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    COMPLETED = "completed"
    TIMEOUT = "timeout"
    AWAITING_MANUAL_TERMINATION = "awaiting_manual_termination"
    AWAITING_DELAY_BEFORE_START = "awaiting_delay_before_start"
    AWAITING_DELAY_TO_COMPLETE = "awaiting_delay_to_complete"
