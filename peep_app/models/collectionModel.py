from peep_app.config.mysqlconnection import connectToMySQL
from peep_app.models import userModel

class Collection:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    @classmethod
    def get_all_by_owner(cls, data):
        query = "SELECT * FROM collections C inner join users U on C.owner_id = U.id WHERE owner_id = %(ownerId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        collections = []

        if results:
            if len(results) > 0:
                for collection in results:
                    current = cls(collection)
                    
                    owner_data = {
                        'id' : collection['U.id'],
                        'firstname' : collection['firstname'],
                        'lastname' : collection['lastname'],
                        'birthday' : collection['birthday'],
                        'gender' : collection['gender'],
                        'username': collection['username'],
                        'email' : collection['email'],
                        'password' : collection['password'],
                        'created_at' : collection['U.created_at'],
                        'updated_at' : collection['U.updated_at'],
                        'status' : None,
                        'country' : None,
                        'role' : None,
                    }

                    current.owner = userModel.User(owner_data)
                    collections.append(current)

        return collections


    @classmethod
    def search_by_name_and_owner(cls, data):
        # Funciona
        # search = "'%" + data['search'] + "%'"
        search = "'" + data['search'] + "%'"
        userId = data['userId']
        query = "Select * from collections C inner join users U on C.owner_id = U.id where C.name like %s and C.owner_id like %i;" % (search, userId,)
        results = connectToMySQL('peep_app_schema').query_db(query)

        collections = []

        if results:
            if len(results) > 0:
                for collection in results:
                    current = cls(collection)

                    owner_data = {
                        'id' : collection['U.id'],
                        'firstname' : collection['firstname'],
                        'lastname' : collection['lastname'],
                        'birthday' : collection['birthday'],
                        'gender' : collection['gender'],
                        'username': collection['username'],
                        'email' : collection['email'],
                        'password' : collection['password'],
                        'created_at' : collection['U.created_at'],
                        'updated_at' : collection['U.updated_at'],
                        'status' : None,
                        'country' : None,
                        'role' : None,
                    }

                    current.owner = userModel.User(owner_data)
                    collections.append(current)

        return collections


    @classmethod
    def save(cls, data):
        query = "INSERT INTO collections (name, description, created_at, updated_at) VALUES (%(name)s, %(description)s, NOW(), NOW());"
        return connectToMySQL('peep_app_schema').query_db(query, data)