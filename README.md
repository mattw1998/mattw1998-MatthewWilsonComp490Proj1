# Matthew Wilson
#
# Three libraries are used in this sprint
# The json library allows for the json files to be read into a list much easier
# The sqlite3 library allows for sql database creation/editing/querying etc
# The pytest library allows for easy function testing
#
# There is no direct interaction with this program past running it
# The program has two different methods to read a json file into a list of items based on the formatting of the objects in the file
# Then an empty database is created (or a connection to it is called if it already exists) with all the attributes that exist from our two json files
# Because these two json files have different attributes, we use two different functions to populate each into the sql database
# The changes are then saved into the database and it is closed
#
# Was unable to get test 2 to pass
