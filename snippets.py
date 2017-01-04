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
def put(name, snippet, hide, show):
    """
    STORE a snippet with the associated name.

    RETURNS the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    if not hide and not show:
        try:
            with connection, connection.cursor() as cursor:
                cursor.execute("insert into snippets values (%s, %s)", (name,snippet))
        except psycopg2.IntegrityError as e:
            with connection, connection.cursor() as cursor:
                cursor.execute("update snippets set message = %s where keyword = %s", (snippet,name))
    elif hide and show:
        return float('-inf'), float('-inf')
    else:
        try: 
            with connection, connection.cursor() as cursor:
                cursor.execute("insert into snippets values (%s, %s, %s)", (name,snippet, hide))
        except psycopg2.IntegrityError as e: #existing snippet
            with connection, connection.cursor() as cursor:
                cursor.execute("update snippets set message = %s, hidden = %s where keyword = %s", (snippet,hide,name))
    logging.debug("Snippet stored successfully.")
    return name, snippet

def get(name):
    """ Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'.
    Returns the Snippet.
    """
    #logging.error("FIXME: Unimplemented - get({!r})".format(name))
    logging.debug("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        command = "select * from snippets where keyword = (%s)"
        cursor.execute(command, (name,))
        message = cursor.fetchone()
    logging.debug("Snippet retrieved successfully")
    if not message:
        print "404: Snippet not found"
        return -1
    return message

def catalog():
    """ Display a list of all unhidden keywords in the database"""
    logging.debug("Displaying list of all keywords in database")
    cursor = connection.cursor()
    command = "select * from snippets where not hidden order by keyword"
    cursor.execute(command)
    all_keys = [each[0] for each in cursor.fetchall()]
    return all_keys

def search(word):
    """ Display list of snippets that contain the desired word"""
    logging.debug("Displaying a list of all like snippets")
    cursor = connection.cursor()
    command = "select * from snippets where message like '%{}%' and not hidden order by keyword".format(word)
    cursor.execute(command)
    messages = cursor.fetchall()
    if len(messages) > 0:
        return messages
    else:
        print "No matches found for '{}'".format(word)
        return ""
        
def show_table():
    """ Show Entire Contents of Table"""
    logging.debug("Displaying all rows and columns of table")
    cursor = connection.cursor()
    command = "select * from snippets"
    cursor.execute(command)
    messages = cursor.fetchall()
    return messages
        
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
    put_parser.add_argument("--hide", help = "Boolean option to hide the snippet", action = "store_true")
    put_parser.add_argument("--show", help = "Boolean option to show the snippet", action = "store_true")
    
    # Subparser for the get command
    logging.debug("Constrcuting the get parser")
    get_parser = subparsers.add_parser("get", help = "Retrieve a snippet")
    get_parser.add_argument("name", help  = "Name of the snippet")
    
    # subparser for the catalog command
    logging.debug("Constructing the catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help = "Retrieve list of all keywords")
    
    # subparser for the search command
    logging.debug("Constructing the seach subparser")
    search_parser = subparsers.add_parser("search", help = "Retrieve list of all snippets contaiing the desired word")
    search_parser.add_argument("word", help = "similarity being searched")
    
    #subparser for show_table command
    logging.debug("Constrcuting the display_table subparser")
    table_parser = subparsers.add_parser("show_table", help = "Display all table contents")
    
    arguments = parser.parse_args()
    
    # convert the parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name,snippet = put(**arguments)
        if name == float('-inf') and snippet == float('-inf') :
            print "Error 104: Conflicting arguments set."
            print "Please try entering the snippet again with only one optional argument set."
        else:
            print "Stored {!r} as {!r}".format(snippet,name)
            if arguments['hide']:
                print "This snippet will be hidden."
            elif arguments['show']:
                print "This snippet will be shown."
    elif command == "get":
        results = get(**arguments)
        if results == -1:
            pass
        else:
            if results[2]:
                print "This snippet is hidden."
                print "Contact your adminstrator to inquire about access."
            else:
                print "Retrieved snippet: {!r}".format(results[1])
    elif command == "catalog":
        keys = catalog()
        print "The following keys are currently in the snippets database:"
        i = 1
        for key in keys:
            print "{}) {}".format(str(i), key)
            i += 1
    elif command == "search":
        similar = search(**arguments)
        if len(similar) > 0:
            print "Found the following matches:"
            j = 1
            for match in similar:
                print "{}) {}: {}".format(str(j), match[0], match[1])
                j += 1
    elif command == "show_table":
        contents = show_table()
        k = 1
        for row in contents:
            print "{} - {}".format(str(k),row)
            k+=1
        
if __name__ == "__main__":
    main()
    
    