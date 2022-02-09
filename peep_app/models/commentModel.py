from peep_app.config.mysqlconnection import connectToMySQL
from peep_app.models import userModel

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.post_id = data['post_id']
        self.author = None
        self.likes = []
        self.isLiked = False

    @classmethod
    def get_all_by_post_id(cls, data):
        query = "SELECT * FROM comments C INNER JOIN posts P ON C.post_id = P.id INNER JOIN users U ON U.id = C.author_id WHERE P.id like %(postId)s"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        comments = []

        if results:
            if len(results) > 0:
                for comment in results:
                    currentComment = cls(comment)

                    author_data = {
                        'id' : comment['U.id'],
                        'firstname' : comment['firstname'],
                        'lastname' : comment['lastname'],
                        'birthday' : comment['birthday'],
                        'gender' : comment['gender'],
                        'email' : comment['email'],
                        'password' : comment['password'],
                        'created_at' : comment['U.created_at'],
                        'updated_at' : comment['U.updated_at'],
                        'status' : None,
                        'country' : None,
                        'role' : None,
                    }

                    currentComment.author = userModel.User(author_data)

                    comments.append(currentComment)

        return comments

    @classmethod
    def get_likes(cls, data):
        query = "SELECT COUNT(*) AS likes FROM comments_has_likes WHERE comment_id = %(commentId)s"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        count = 0

        if results:
            if len(results) > 0:
                count = cls(results[0]['likes'])

        return count

