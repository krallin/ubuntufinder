#coding:utf-8

class ImageNotFound(Exception):
    """
    Raised when no Image matching the query was found.
    """

class ReleaseNotFound(Exception):
    """
    Raised when the latest Release could not be identified.
    """