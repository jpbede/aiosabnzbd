"""Exceptions for SABnzbd."""


class SABnzbdError(Exception):
    """Generic error occurred in SABnzbd package."""


class SABnzbdConnectionError(SABnzbdError):
    """Error occurred while communicating to the SABnzbd API."""


class SABnzbdConnectionTimeoutError(SABnzbdError):
    """Timeout occurred while connecting to the SABnzbd API."""


class SABnzbdInvalidAPIKeyError(SABnzbdError):
    """Given API Key is invalid."""


class SABnzbdMissingAPIKeyError(SABnzbdError):
    """API Key is missing."""
