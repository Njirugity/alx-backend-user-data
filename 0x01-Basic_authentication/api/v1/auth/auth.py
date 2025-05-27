from flask import request
from typing import TypeVar, List, Iterable


class Auth():
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None and excluded_paths is None:
            return True
        elif not excluded_paths:
            return True
        normalized_path = path.rstrip('/')
        normalized_excluded_paths = [ep.rstrip('/') for ep in excluded_paths]

        return normalized_path not in normalized_excluded_paths
    
    def authorization_header(self, request=None) -> str: 
        return None
    def current_user(self, request=None) -> TypeVar('User'):
        return None