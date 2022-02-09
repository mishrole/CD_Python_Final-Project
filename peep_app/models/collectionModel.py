from peep_app.config.mysqlconnection import connectToMySQL

class Collection:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_by_owner(cls, data):
        query = "SELECT * FROM collections WHERE owner_id = %(ownerId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        collections = []

        if results:
            if len(results) > 0:
                for collection in results:
                    collections.append(cls(collection))

        return collections

    @classmethod
    def save(cls, data):
        query = "INSERT INTO collections (name, description, created_at, updated_at) VALUES (%(name)s, %(description)s, NOW(), NOW());"
        return connectToMySQL('peep_app_schema').query_db(query, data)