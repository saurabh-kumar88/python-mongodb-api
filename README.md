# python-mongodb-api
General purpose api for basic read, write and filter operations with mongo database
------------------------------------------About Mongo DB-------------------------------------------------------------------

Mongodb is a NoSQL type data base, unlike traditional Relational db where concept of rows and col are use
NoSql uses collections, they are considered as columns and each of them have documents which are considered 
as data, which are stored in the form of has-table or dictionary {_id : 454, 'title' : 'Jack ryan'}
In mongo db some basic terminology used are as follows.

                                        Database
                            (or column)     |
                            collection1, collection2, collection3
                                |           |              |
                            document1    document1    document1
                            document2    document2    document2
                            document3    document3    document3
                            json object
                        e.g {'title' : 'foo'}

Note : To create new db or new column in existing db, we must write some data to document after initialization
otherwise db will not create

Importatnt links:

MongoDB Cheatsheet:
https://www.opentechguides.com/how-to/article/mongodb/118/mongodb-cheatsheat.html

MOngoDB Comparison operators: completey different then relational db lke '==', '=>' or '=<'
https://docs.mongodb.com/manual/reference/operator/query-comparison/

MOngoDB exceptions and Errors:
https://api.mongodb.com/python/current/api/pymongo/errors.html#pymongo.errors.ConnectionFailure
