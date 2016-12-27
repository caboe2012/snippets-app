import logging

#set the log file name and level
logging.basicConfig(filename = "snippets.log", logging.level = DEBUG)

def put(name, snippet):
    """
    Store a snippet with the associated name.
    Returns the name and the snippet.
    """
    logging.error("FIXME - Unimplemented put({!r}, {!r})".format("name, snippt))
    return name, snippet

def get(name):
    """ Retrieve the snippet with the given name.
    If there is no such snippet, return '404: Snippet not Found".
    Returns the snippet.
    """
    logging.error("FIXME - Unimplemented - get({!r})".format(name))
    return ""
