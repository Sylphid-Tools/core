class SylphidError(Exception):
    """Root Exception for all Sylphid APIs."""


class ContextError(SylphidError):
    """Error raised when a context error is encountered."""


class TemplateError(SylphidError):
    """Error raised when a path error is encountered."""
