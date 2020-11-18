from enum import Enum


class JobStatusEnum(str, Enum):
    INITIAL = "INITIAL"
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    FAILURE = "FAILURE"


ALLOWED_JOB_STATUS_TRANSITIONS = {
    JobStatusEnum.INITIAL: {JobStatusEnum.QUEUED, JobStatusEnum.FAILURE},
    JobStatusEnum.QUEUED: {JobStatusEnum.IN_PROGRESS, JobStatusEnum.FAILURE},
    JobStatusEnum.IN_PROGRESS: {JobStatusEnum.FINISHED, JobStatusEnum.FAILURE},
    JobStatusEnum.FINISHED: {},
    JobStatusEnum.FAILURE: {}
}
