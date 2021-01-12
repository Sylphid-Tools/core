class SylphidError(Exception):
    """Root Exception for all Sylphid APIs."""


class ContextError(SylphidError):
    """Error raised when a context error is encountered."""
