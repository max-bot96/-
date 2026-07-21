class DecisionValidationError(Exception):
    pass


class InvalidRequestIDError(DecisionValidationError):
    pass


class EmptyPromptError(DecisionValidationError):
    pass


class NoModelsSelectedError(DecisionValidationError):
    pass


class InvalidConstraintsError(DecisionValidationError):
    pass


class UnsupportedVersionError(DecisionValidationError):
    pass


class PipelineError(Exception):
    pass


class StageFailedError(PipelineError):
    pass


class AllModelsFailedError(PipelineError):
    pass


class DecisionCancelledError(PipelineError):
    pass
