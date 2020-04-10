from pymongo import MongoClient
from pymongo import errors
from bson.objectid import ObjectId

class Mongodb_handler:
    """
    This Class implemented some of the most frequented database operations used in any program, using
    python - mongodb adapter "pymongo"
    
    Methods
    -------
    __init__()
        Looks for host address and port number for connection setup

    check_db()
        Checks if database present
    write_record()
        write data to document
    read_record()
        read data from document
    filters_and_Queries()
        read, and delete data from document using filters and queries
    
    Exceptions and Errors
    ---------------------
    ConnectionFailure
        checks whenever a new connection is made with database, 
        raised when new connection failed or existing one get lost.
    
    CollectionInvalid
        raised whe user enters some invalid collection name.
    
    NetworkTimeout
        raised if write operation get failed,  
        In case of a write operation, you cannot know whether it succeeded or failed.

    ValueError
        raised during read operation, If user provide invalid or empty list of search fields
    
    """

    def __init__(self, host_address, port_number):
        """
        When class Mongo_handler instantiated then this method looks for two important parameters. 

        Parameters
        ----------
        host_address : str
        Address of connecting host, for local server e.g localhost or 127.0.0.1        
        
        port_number : int
        Port address number, default value for mongodb is 27017 
        
        Return value
        ------------
        None
        """
        self.host_address = host_address
        self.port_number = port_number
             

    def check_db(self, db_name ):
        """
        Checks if database name is present. 

        Parameters
        ----------
        db_name : str
        Database name to searched        
        
        Return value : bool
        ------------
        True if db exists else False
        """
        self.db_name = db_name

        try:
            client = MongoClient( self.host_address, self.port_number )
        except errors.ConnectionFailure as err:
            raise errors.ConnectionFailure(message='Connection to the database cannot be made or is lost', error_labels=None)
        
        db_list = client.list_database_names()
        if db_name in db_list:
            return True
        else:
            return False


    def write_record(self, db_name, col_name, data, insert_method ):
        """ 
            This method is used to insert data into specified collection and its column, with insert method as option.

            Parameters
            ----------
            db_name  : Name of database or collection        
            
            col_name : str
            Name of the column, you want to search.
            
            data : list of dictionaries
            Pack your data into this format e.g [{'title', 'Author', 'Publication date'},... ]
                    
            insert_method: str
            Defines method of data insertion, 'single' or 'multiple' 

            Return value
            ------------
            result_list : An iterable object of pymongo.cursor.Cursor

        """
        self.db_name = db_name
        self.col_name = col_name
        self.data = data
        self.insert_method = insert_method
        
        try:
            client = MongoClient( self.host_address, self.port_number )
        except errors.ConnectionFailure as err:
            raise errors.ConnectionFailure(message='Connection to the database cannot be made or is lost', error_labels=None)

        # Create if not exists
        mydb = client[ db_name ]
        try:
            mycol = mydb[ col_name ]
        except errors.CollectionInvalid as err:
            raise errors.CollectionInvalid(message='Invalid collection name', error_labels=None)
        
        # check write method type 
        try:
            if insert_method == 'single':
                result_list = mycol.insert_one(data)
            elif insert_method == 'multiple':
                result_list = mycol.insert_many(data)
            else:
                raise ValueError('data list is might be empty or incorrect data fields')
        except errors.NetworkTimeout as err:
            raise errors.errors.NetworkTimeout(message='Last write operation failed, an open connection exceeded socketTimeoutMS', errors=None)
            
    def read_record(self, db_name, col_name, find_method, attr='_id' ):

        """ 
            This function reads specified fields only.

            Parameters
            ----------
            db_name  : Name of database or collection        
            
            col_name : str
            Name of the column, you want to search.
            
            find_method : str
            Methods to search, 
            'one' -->  to read only one record,
            'all' -->  to read every record, 
            'some'-->  to read read only specified fields.

            
            
            attr : a list of strings, to specified search document fields e.g attr=['title', 'Author']
            Default value of attr is set to '_id'. If document fields does misspalled or does not 
            found then by default only list of _ids will be returned.
            
                    
            Return value
            ------------
            result_list : An iterable object of pymongo.cursor.Cursor
            
        """
        self.db_name = db_name
        self.col_name = col_name
        self.find_method = find_method
        self.attr = attr

        try:
            client = MongoClient( self.host_address, self.port_number )
        except errors.ConnectionFailure as err:
            raise errors.ConnectionFailure(message='Connection to the database cannot be made or is lost', error_labels=None)

        mydb = client[ db_name ]
        try:
            mycol = mydb[ col_name ]
        except errors.CollectionInvalid as err:
            raise errors.CollectionInvalid(message='Invalid collection name', error_labels=None)
        
        if find_method == "one":
            record = mycol.find_one()
        elif find_method == "all":
            record = mycol.find()
        elif find_method == "some":
            if attr[0] == '_id':
                record = mycol.find({}, {'_id'} )
            else:
                find_attr = {}
                for i in range(len(attr)):
                    find_attr[ str(attr[i]) ] = str(i)      
                record = mycol.find({}, find_attr )
                if record.count == 0:
                    return [" ------ / /------ No such record found --------/ / -----"]
                    return None
        else:
            raise ValueError("find method should be either 'one', 'all' or 'some' with attr.")
            return None
        return record



    def filters_and_Queries(self, db_name, col_name, operation ,query ):

        """
        read or delete data from documents, supports queries and filters 

        Parameters
        ----------
        db_name : str
        Name of the database        
        
        col_name : str
        column or document name

        operation : str
        Type of operation need to be performed
        'find'   --> To search data 
        'delete' --> To delete data

        query : dict
        A dictionary having query to be applied 
        e.g search price greater then 100 -- > {'price': {"$gt" : 120.0} }
        e.g search title --> { 'title' : 'Jack ryan'}
        
        Return value
        ------------
        If operation = 'find'   --> An iterable object of pymongo.cursor.Cursor
        If operation = 'delete' --> None
        """
        self.db_name = db_name
        self.col_name = col_name
        self.operation = operation
        self.query = query
        

        try:
            client = MongoClient( self.host_address, self.port_number )
        except errors.ConnectionFailure as err:
            raise errors.ConnectionFailure(message='Connection to the database cannot be made or is lost', error_labels=None)

        mydb = client[ db_name ]
        try:
            mycol = mydb[ col_name ]
        except errors.CollectionInvalid as err:
            raise errors.CollectionInvalid(message='Invalid collection name', error_labels=None)

        if operation == 'find':
            record = mycol.find(query)
            return record
            # Check if document exists 
            if record.count() == 0:
                return [" ------ / /------ No such record found --------/ / -----"]
        elif operation == 'delete':
            record = mycol.delete_many(query)
            return None
        
# test data            
"""
movies_data = [
    {'title' : 'Golden Eye', 'release' : '1995', 'Imdb ratings' : 8.5 },
    {'title' : 'World is not enough', 'release' : '1998', 'Imdb ratings' : 7.5 },
    {'title' : 'Die another day', 'release' : '2000', 'Imdb ratings' : 6.3 },
    {'title' : '1917', 'release' : '2020', 'Imdb ratings' : 9.5 },
    {'title' : 'Shoot them up', 'release' : '2005', 'Imdb ratings' : 6.9 },
    {'title' : 'Never say never again', 'release' : '1971', 'Imdb ratings' : 8.9 },

]
"""
    

"""
if __name__ == "__main__":
    
    # create connection
    obj = Mongodb_handler('localhost', 27017)
    
    # write multiple records
    #obj.write_record(db_name='Movies', col_name='Action', data=movies_data[4], insert_method='single')
    
    # check if db name 'Movies' exists
    #print(obj.check_db('Movies'))
    
    # find record and show only 'title' and 'release'
    #data = obj.read_record(db_name='Movies', col_name='Action', find_method='all')
    
    # find movies with Imdb ratings greater then 7
    #data = obj.filters_and_Queries(db_name='Movies', col_name='Action', operation='find', query=( {'Imdb ratings': {"$gt" : 7.0} } ) )
    
    # delete movie title 'Die another die'
    #obj.filters_and_Queries(db_name='Movies', col_name='Action', operation='delete', query=( {'title': 'Shoot them up'}  ) )
    #data = obj.read_record(db_name='Movies', col_name='Action', find_method='all')
    

    flag = True
    if flag:
        for i in data:
            print("\n", i)

"""

     
    
    




