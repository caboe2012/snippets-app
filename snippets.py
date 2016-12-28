import logging
import argparse

# set the log file name and the logging level
logging.basicConfig(filname = "snippets.log", level = logging.DEBUG)


# create the four CRUD functions for snippets skeleton
def put(name, snippet):
    """
    STORE a snippet with the associated name.

    RETURNS the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """ Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the Snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return '404: Snippet Not Found'

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
    parser = argparse.ArgumentParser(description = "Store and retrieve snippets of text.")
    
    subparsers = parser.add_subparsers(dest = "command", help = "Available Commands")
    
    #Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help ="Store a snippet")
    put_parser.add_argument("name", help = "Name of the snippet")
    put_parser.add_argument("snippet", help = "Snippet text")
    
    arguments = parser.parse_args()
    
if __name__ == "__main__":
    main()
    
    