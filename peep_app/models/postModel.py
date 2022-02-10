from peep_app.config.mysqlconnection import connectToMySQL
from flask import flash
from peep_app.models import userModel, collectionModel
from datetime import datetime

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author = None
        self.time_ago = ""
        self.likes = 0
        self.isLiked = False
        self.users_who_like = []
        self.in_collections = []

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM posts P INNER JOIN users U on U.id = P.author_id order by P.id desc"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        posts = []

        userId = data['userId']

        if results:
            if len(results) > 0:
                for post in results:
                    currentPost = cls(post)
                    currentPost.time_ago = Post.ago(currentPost.created_at)

                    author_data = {
                        'id' : post['U.id'],
                        'firstname' : post['firstname'],
                        'lastname' : post['lastname'],
                        'birthday' : post['birthday'],
                        'gender' : post['gender'],
                        'email' : post['email'],
                        'username': post['username'],
                        'password' : post['password'],
                        'created_at' : post['U.created_at'],
                        'updated_at' : post['U.updated_at'],
                        'status' : None,
                        'country' : None,
                        'role' : None,
                    }

                    collections =  collectionModel.Collection.get_collections_of_saved_post({'postId': currentPost.id})
                    in_collections = []

                    if collections:
                        for collection in collections:
                            collection_data = {
                                'id': collection['id'],
                                'name': collection['name'],
                                'description': collection['description'],
                                'created_at' : collection['created_at'],
                                'updated_at' : collection['updated_at']
                            }

                            in_collections.append(collectionModel.Collection(collection_data))
                            

                    currentPost.in_collections = in_collections

                    likes_request = {
                        'userId' : userId,
                        'postId' : currentPost.id
                    }

                    currentPost.author = userModel.User(author_data)
                    currentPost.likes = cls.count_all_likes(likes_request)
                    currentPost.users_who_like = cls.get_users_who_like(likes_request)

                    currentUserLikes = cls.count_likes_by_user_and_post(likes_request)

                    if currentUserLikes > 0:
                        currentPost.isLiked = True

                    posts.append(currentPost)

        return posts


    @classmethod
    def get_all_by_author(cls, data):
        query = "SELECT * FROM posts P INNER JOIN users U on U.id = P.author_id WHERE U.id = %(userId)s order by P.id desc;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        posts = []
        userId = data['userId']
        requesterId = data['requesterId']

        if results:
            if len(results) > 0:
                for post in results:
                    currentPost = cls(post)
                    currentPost.time_ago = Post.ago(currentPost.created_at)

                    author_data = {
                        'id' : post['U.id'],
                        'firstname' : post['firstname'],
                        'lastname' : post['lastname'],
                        'birthday' : post['birthday'],
                        'gender' : post['gender'],
                        'username': post['username'],
                        'email' : post['email'],
                        'password' : post['password'],
                        'created_at' : post['U.created_at'],
                        'updated_at' : post['U.updated_at'],
                        'status' : None,
                        'country' : None,
                        'role' : None,
                    }

                    collections =  collectionModel.Collection.get_collections_of_saved_post(currentPost.id)
                    in_collections = []

                    if collections:
                        for collection in collections:
                            collection_data = {
                                'id': collection['C.id'],
                                'name': collection['name'],
                                'description': collection['description'],
                                'created_at' : collection['C.created_at'],
                                'updated_at' : collection['C.updated_at']
                            }

                            in_collections.append(collectionModel.Collection(collection_data))


                    currentPost.in_collections = in_collections

                    likes_request = {
                        'userId' : userId,
                        'postId' : currentPost.id
                    }

                    current_user_like_request = {
                        'userId': requesterId,
                        'postId' : currentPost.id
                    }

                    currentPost.author = userModel.User(author_data)
                    currentPost.likes = cls.count_all_likes(likes_request)
                    currentPost.users_who_like = cls.get_users_who_like(likes_request)

                    currentUserLikes = cls.count_likes_by_user_and_post(current_user_like_request)

                    if currentUserLikes > 0:
                        currentPost.isLiked = True

                    posts.append(currentPost)

        return posts



    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, author_id, created_at, updated_at) VALUES (%(content)s, %(authorId)s, NOW(), NOW());"
        return connectToMySQL('peep_app_schema').query_db(query, data)


    @classmethod
    def count_likes_by_user_and_post(cls, data):
        query = "SELECT COUNT(*) as likes FROM posts_has_likes WHERE user_id = %(userId)s AND post_id = %(postId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        count = 0

        if results:
            if len(results) > 0:
                count = results[0]['likes']

        return count


    @classmethod
    def count_all_likes(cls, data):
        query = "SELECT COUNT(*) as likes FROM posts_has_likes WHERE post_id = %(postId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        count = 0

        if results:
            if len(results) > 0:
                count = results[0]['likes']

        return count


    @classmethod
    def get_users_who_like(cls, data):
        query = "Select * from users U INNER JOIN posts_has_likes PL on PL.user_id = U.id INNER JOIN posts P on P.id = PL.post_id WHERE P.id = %(postId)s"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        users = []

        if results:
            if len(results) > 0:
                for user in results:
                    users.append(userModel.User(user))

        return users


    @classmethod
    def get_users_who_like_API(cls, data):
        query = "Select * from users U INNER JOIN posts_has_likes PL on PL.user_id = U.id INNER JOIN posts P on P.id = PL.post_id WHERE P.id = %(postId)s"
        results = connectToMySQL('peep_app_schema').query_db(query, data)
        return results


    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO posts_has_likes (post_id, user_id) VALUES (%(postId)s, %(userId)s);"
        return connectToMySQL('peep_app_schema').query_db(query, data)


    @classmethod
    def remove_like(cls, data):
        query = "DELETE FROM posts_has_likes WHERE post_id = %(postId)s and user_id = %(userId)s;"
        return connectToMySQL('peep_app_schema').query_db(query, data)


    @staticmethod
    def validatePost(post):
        is_valid = True

        content = post['content']
        
        if len(content) == 0:
            flash('Post must be at least 1 character long', 'post_error')
            is_valid = False

        return is_valid


    @staticmethod
    def ago(input_date):
        result = "0 seconds ago"
        total_seconds = abs((input_date - datetime.now()).total_seconds())

        sec_value = total_seconds % (24 * 3600)
        hours = sec_value // 3600
        sec_value %= 3600
        min = sec_value // 60
        sec_value %= 60
        days = hours / 24
        years = days / 365.25

        if int(years) > 0:
            result = f"{int(years)} year ago"
            if int(years) > 1:
                result = f"{int(years)} years ago"
        elif int(days) > 0:
            result = f"{int(days)} day ago"
            if int(days) > 1:
                result = f"{int(days)} days ago"
        elif int(hours) > 0:
            result = f"{int(hours)} hour ago"
            if int(hours) > 1:
                result = f"{int(hours)} hours ago"
        elif int(min) > 0:
            result = f"{int(min)} minute ago"
            if int(min) > 1:
                result = f"{int(min)} minutes ago"
        elif int(sec_value) > 0:
            result = f"{int(sec_value)} second ago"
            if int(sec_value) > 1:
                result = f"{int(sec_value)} seconds ago"

        return result
        