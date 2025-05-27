#!/usr/bin/env python3
""" to manage the API authentication.
"""

from flask import request
from typing import TypeVar, List, Iterable


class Auth():
    """
    Template for all authentication system you will implement.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths
            that are excluded from authentication.

        Returns:
            bool: True if authentication is required
            False otherwise.
        """

        if path is None and excluded_paths is None:
            return True
        elif not excluded_paths:
            return True
        normalized_path = path.rstrip('/')
        normalized_excluded_paths = [ep.rstrip('/') for ep in excluded_paths]

        return normalized_path not in normalized_excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header for the given request.

        Args:
            request (Optional): The request object. Defaults to None.

        Returns:
            str: The authorization header.
        """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current authenticated user.

        Args:
            request (Optional[Request]):
            The request object representing
            the current HTTP request.

        Returns:
            User: The current authenticated user.

        """
        return None
