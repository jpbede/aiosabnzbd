"""Exceptions for SABnzbd."""


class SabnzbdError(Exception):
    """Generic error occurred in SABnzbd package."""


class SabnzbdConnectionError(SabnzbdError):
    """Error occurred while communicating to the SABnzbd API."""


class SabnzbdConnectionTimeoutError(SabnzbdError):
    """Timeout occurred while connecting to the SABnzbd API."""


class SabnzbdInvalidAPIKeyError(SabnzbdError):
    """Given API Key is invalid."""


class SabnzbdMissingAPIKeyError(SabnzbdError):
    """API Key is missing."""
