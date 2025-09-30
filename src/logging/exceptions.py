class FrameworkError(Exception):
    """Base exception for the test framework."""


class ApiError(FrameworkError):
    pass


class UiError(FrameworkError):
    pass