from peep_app.config.mysqlconnection import connectToMySQL

class Country:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM countries"
        results = connectToMySQL('peep_app_schema').query_db(query)

        countries = []

        if results:
            if len(results) > 0:
                for country in results:
                    countries.append(cls(country))

        return countries