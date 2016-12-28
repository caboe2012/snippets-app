import logging
import argparse

#set the log file name and level
logging.basicConfig(filename = "snippets.log", level = logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with the associated name.
    Returns the name and the snippet.
    """
    logging.error("FIXME - Unimplemented put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """ Retrieve the snippet with the given name.
    If there is no such snippet, return '404: Snippet not Found".
    Returns the snippet.
    """
    logging.error("FIXME - Unimplemented - get({!r})".format(name))
    return ""

def update(name, snippet):
    """ Modify the snippet with the given name."""
    return name, snippet

def delete(name, snippet):
    """ Deletes the snippet with the given name."""
    print "Successfully deleted snippet {}.".format(name)
    return ""

def main():
    """ Main Function """
    logging.info("Constructing Parser")
    parser = argparse.ArgumentParser(description = "Store and retrieve snippets of text".)
    arguments = parser.parse_args()

