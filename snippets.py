import logging
import argparse
import psycopg2

# set the log file name and the logging level
logging.basicConfig(filename = "snippets.log", level = logging.DEBUG)

# connect to the PostgreSQL database
logging.debug("Connecting to the PostgreSQL database")
connection = psycopg2.connect(database = "snippets")
logging.debug("Database conncetion successful")

# create the four CRUD functions for snippets skeleton
def put(name, snippet):
    """
    STORE a snippet with the associated name.

    RETURNS the name and the snippet
    """
#    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    #cursor = connection.cursor()
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute("insert into snippets values (%s, %s)", (name,snippet))
    except psycopg2.IntegrityError as e:
        with connection, connection.cursor() as cursor:
            cursor.execute("update snippets set message = %s where keyword = %s", (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """ Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the Snippet.
    """
    #logging.error("FIXME: Unimplemented - get({!r})".format(name))
    logging.debug("Retrieving snippet {!r}".format(name))
    #cursor = connection.cursor()
    #command = "select message from snippets where keyword = (%s)"
    #cursor.execute(command, (name,))
    #message = cursor.fetchone()
    #connection.commit()
    with connection, connection.cursor() as cursor:
        command = "select message from snippets where keyword = (%s)"
        cursor.execute(command, (name,))
        message = cursor.fetchone()
    logging.debug("Snippet retrieved successfully")
    if not message:
        return "404: Snippet not found"
    return message[0]

def catalog():
    """ Display a list of all keywords in the database"""
    logging.debug("Displaying list of all keywords in database")
    cursor = connection.cursor()
    command = "select * from snippets order by keyword"
    cursor.execute(command)
    all_keys = [each[0] for each in cursor.fetchall()]
    print "The following keys are currently in the snippets database:"
    i = 1
    for key in all_keys:
        print "{}) {}".format(str(i), key)
        i += 1
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
    
    # Subparser for the get command
    logging.debug("Constrcuting the get parser")
    get_parser = subparsers.add_parser("get", help = "Retrieve a snippet")
    get_parser.add_argument("name", help  = "Name of the snippet")
    
    # subparser for the lookup command
    logging.debug("Constructing the catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help = "Retrieve list of all keywords")
    
    arguments = parser.parse_args()
    
    # convert the parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name,snippet = put(**arguments)
        print "Stored {!r} as {!r}".format(snippet,name)
    elif command == "get":
        snippet = get(**arguments)
        print "Retrieved snippet: {!r}".format(snippet)
    elif command == "catalog":
        catalog()
    
if __name__ == "__main__":
    main()
    
    