from peep_app.config.mysqlconnection import connectToMySQL
from peep_app.models import userModel, postModel

class Collection:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None
        self.saved_posts = []

    @classmethod
    def get_all_by_owner(cls, data):
        query = "SELECT * FROM collections C inner join users U on C.owner_id = U.id WHERE owner_id = %(ownerId)s order by C.name asc;"
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

                    current.saved_posts = cls.get_posts_in_collection({'collectionId': current.id})
                    current.owner = userModel.User(owner_data)
                    collections.append(current)

        return collections


    @classmethod
    def search_by_name_and_owner(cls, data):
        # Funciona
        # search = "'%" + data['search'] + "%'"
        search = "'" + data['search'] + "%'"
        userId = data['userId']
        limit = data['limit']
        query = "Select * from collections C inner join users U on C.owner_id = U.id where C.name like %s and C.owner_id like %i order by C.name asc limit %s;" % (search, userId, limit,)
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

                    current.saved_posts = cls.get_posts_in_collection({'collectionId': current.id})
                    current.owner = userModel.User(owner_data)
                    collections.append(current)

        return collections


    @classmethod
    def get_posts_in_collection(cls,data):
        query = "Select * from posts P inner join collections_has_posts CP on P.id = CP.post_id where CP.collection_id = %(collectionId)s"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        posts = []

        if results:
            if len(results) > 0:
                for post in results:
                    post_data = {
                        'id': post['id'],
                        'content' : post['content'],
                        'created_at': post['created_at'],
                        'updated_at' : post['updated_at']
                    }

                    posts.append(postModel.Post(post_data))

        return posts


    @classmethod
    def save(cls, data):
        query = "INSERT INTO collections (name, description, owner_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(ownerId)s, NOW(), NOW());"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def saveFast(cls, data):
        query = "INSERT INTO collections (name, owner_id, created_at, updated_at) VALUES (%(name)s, %(ownerId)s, NOW(), NOW());"
        return connectToMySQL('peep_app_schema').query_db(query, data)
    
    @classmethod
    def add_post_to_collection(cls, data):
        query = "INSERT INTO collections_has_posts(collection_id, post_id) VALUES (%(collectionId)s, %(postId)s);"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def remove_post_from_collection(cls, data):
        query = "DELETE FROM collections_has_posts WHERE collection_id = %(collectionId)s and post_id = %(postId)s;"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def find_collection_by_owner_and_id(cls, data):
        query = "SELECT * from collections C WHERE C.id = %(collectionId)s and C.owner_id = %(ownerId)s;"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def get_collections_of_saved_post(cls, data):
        query = "Select * from collections C inner join collections_has_posts CP on C.id = CP.collection_id where CP.post_id = %(postId)s;"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def get_collections_of_saved_post_by_owner(cls, data):
        query = "Select * from collections C inner join collections_has_posts CP on C.id = CP.collection_id where CP.post_id = %(postId)s and C.owner_id = %(ownerId)s;"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @staticmethod
    def validateCollection(collection):
        is_valid = True

        name = collection['name']
        description = collection['description']

        if len(name) == 0:
            is_valid = False

        if len(description) == 0:
            is_valid = False

        return is_valid

    @staticmethod
    def validateFastCollection(collection):
        is_valid = True

        name = collection['name']

        if len(name) == 0:
            is_valid = False

        return is_valid