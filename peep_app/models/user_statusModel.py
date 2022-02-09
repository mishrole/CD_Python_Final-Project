from peep_app.config.mysqlconnection import connectToMySQL

class User_Status:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user_status"
        results = connectToMySQL('peep_app_schema').query_db(query)

        all = []

        if results:
            if len(results) > 0:
                for status in results:
                    all.append(cls(status))

        return all