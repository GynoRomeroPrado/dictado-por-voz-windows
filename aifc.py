
# Dummy aifc module for Python 3.13+ compatibility
# SpeechRecognition uses this but we don't need AIFF support for this app

class Error(Exception):
    pass

def open(f, mode=None):
    raise Error("AIFF support is not available")
