from peep_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import datetime, timedelta
from peep_app.constants import roles_enum, user_status_enum
from peep_app.models import user_statusModel, postModel

TEXT_REGEX = re.compile(r'^[A-Za-z\u00C0-\u017F\.\-\s]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])[a-zA-Z\d]{8,}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.birthday = data['birthday']
        self.gender = data['gender']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.status = None
        self.country = None
        self.role = None
        self.followers = []
        self.following = []
        self.followed = False
        self.posts = []

    # Followers and Following data
    @classmethod
    def getFollowersByUserId(cls, data):
        query = "Select * from users follower inner join followers F on F.follower = follower.id inner join users followed on F.followed = followed.id where followed.id = %(userId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        followers = []

        if results:
            if len(results) > 0:
                for user in results:
                    followers.append(cls(user))

        return followers

    @classmethod
    def getFollowingByUserId(cls, data):
        query = "Select * from users followed inner join followers F on F.followed = followed.id inner join users following on F.follower = following.id where following.id = %(userId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        following = []

        if results:
            if len(results) > 0:
                for user in results:
                    following.append(cls(user))

        return following


    # FollowedId is followed by current user
    @classmethod
    def userIsFollower(cls, data):
        query = "Select * from followers where followers.followed = %(followedId)s and followers.follower = %(userId)s"
        results = connectToMySQL('peep_app_schema').query_db(query, data)
        current = [d for d in results if d['follower'] == data['userId']]

        isFollower = False
        
        if current:
            if len(current) > 0:
                isFollower = True

        return isFollower
    
    # Follow and unfollow
    @classmethod
    def follow_user(cls, data):
        query = "Insert into followers (follower, followed) VALUES (%(followerId)s, %(followedId)s);"
        return connectToMySQL('peep_app_schema').query_db(query, data)


    @classmethod
    def unfollow_user(cls, data):
        query = "Delete from followers where follower = %(followerId)s and followed = %(followedId)s;"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    # Users data
    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM users U INNER JOIN user_status US ON US.id = U.status_id WHERE U.status_id NOT LIKE {user_status_enum.User_status.Blocked.value} order by id asc;"
        results = connectToMySQL('peep_app_schema').query_db(query)

        users = []

        if results:
            if len(results) > 0:
                for user in results:
                    current_user = cls(user)

                    status_data = {
                        'id': user['US.id'],
                        'name': user['US.name']
                    }

                    current_user.status = status_data
                    current_user.followers = cls.getFollowersByUserId({'userId': current_user.id})
                    current_user.following = cls.getFollowingByUserId({'userId': current_user.id})
                    current_user.posts = postModel.Post.get_all_by_author({'userId': current_user.id, 'requesterId': current_user.id})
                    users.append(current_user)

        return users
    
    @classmethod
    def register_user(cls, data):
        query = f"INSERT INTO users (firstname, lastname, email, password, birthday, country_id, created_at, updated_at, status_id, role_id) VALUES (%(firstname)s,%(lastname)s,%(email)s,%(password)s,%(birthday)s,%(countryId)s, NOW(), NOW(), {user_status_enum.User_status.Pending.value}, {roles_enum.Roles.User.value})"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (firstname, lastname, birthday, gender, email, password, created_at, updated_at, status_id, role_id, country_id) VALUES (%(firstname)s, %(lastname)s, %(birthday)s, %(gender)s, %(email)s, %(password)s, NOW(), NOW(), %(statusId)s, %(roleId)s, %(countryId)s);"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def findUserByEmail(cls, data):
        query = "SELECT * FROM users U INNER JOIN user_status US ON US.id = U.status_id WHERE U.email = %(email)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        user = None

        if results:
            if len(results) > 0:
                user = cls(results[0])

                status_data = {
                    'id': results[0]['US.id'],
                    'name': results[0]['name']
                }

                user.status = user_statusModel.User_Status(status_data)

        return user

    @classmethod
    def findUserById(cls, data):
        query = "SELECT * FROM users U INNER JOIN user_status US ON US.id = U.status_id INNER JOIN countries C on U.country_id = C.id INNER JOIN roles R on U.role_id = R.id WHERE U.id = %(userId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)

        user = None

        if results:
            if len(results) > 0:
                user = cls(results[0])

                user.followers = cls.getFollowersByUserId({'userId': user.id})
                user.following = cls.getFollowingByUserId({'userId': user.id})
                user.posts = postModel.Post.get_all_by_author({'userId': user.id, 'requesterId': user.id})

                country_data = {
                    'id': results[0]['C.id'],
                    'name': results[0]['C.name']
                }
                
                role_data = {
                    'id': results[0]['R.id'],
                    'name': results[0]['R.name']
                }

                status_data = {
                    'id': results[0]['US.id'],
                    'name': results[0]['name']
                }

                user.status = user_statusModel.User_Status(status_data)
                user.role = role_data
                user.country = country_data

        return user

    @classmethod
    def blockUser(cls, data):
        query = f"UPDATE users SET users.status_id = {user_status_enum.User_status.Blocked.value}, updated_at = NOW() WHERE users.id = %(userId)s"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(userId)s"
        return connectToMySQL('peep_app_schema').query_db(query, data)

    @staticmethod
    def validateRegister(user):
        is_valid = True

        firstname = user['firstname']
        lastname = user['lastname']
        email = user['email']
        password = user['password']
        confirmation = user['password_confirmation']
        birthday = user['birthday']
        country = user['country']

        if len(birthday) == 0:
            flash('Birthday must be selected.', 'register_error')
            is_valid = False
        else:
            today = datetime.now()
            birthdayConverted = datetime.strptime(birthday, "%Y-%m-%d")
    
            if birthdayConverted > today:
                flash('Birthday must be a date in the past', 'register_error')
                is_valid = False
            else:
                age = (today - birthdayConverted) // timedelta(days=365.2425)
                if age < 18:
                    flash('You must be at least 18 years old.', 'register_error')
                    is_valid = False

        if len(firstname) < 2:
            flash('First name must be at least 2 characters long', 'register_error')
            is_valid = False

        if not TEXT_REGEX.match(firstname):
            flash('First name must only contain letters and . -', 'register_error')
            is_valid = False

        if len(lastname) < 2:
            flash('Last name must be at least 2 characters long', 'register_error')
            is_valid = False

        if not TEXT_REGEX.match(lastname):
            flash('Last name must must only contain letters and . -', 'register_error')
            is_valid = False

        if not EMAIL_REGEX.match(email):
            flash('Invalid email address!', 'register_error')
            is_valid = False

        if not PASSWORD_REGEX.match(password):
            flash('Password must be at least 8 characters long and contain 1 uppercase letter and 1 number without special characters', 'register_error')
            is_valid = False

        if password != confirmation:
            flash('Password and confirmation do not match!', 'register_error')
            is_valid = False

        if len(country) < 1:
            flash('Country must be selected.', 'register_error')
            is_valid = False
        
        if User.findUserByEmail({'email': email}) != None:
            flash('Email address is already taken!', 'register_error')
            is_valid = False

        return is_valid


    @staticmethod
    def validateLogin(user):
        is_valid = True

        email = user['email']

        if not EMAIL_REGEX.match(email):
            flash('Invalid email address!', 'login_error')
            is_valid = False

        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long', 'login_error')
            is_valid = False

        if User.findUserByEmail({'email': email}) == None:
            flash('Invalid Email / Password', 'login_error')
            is_valid = False
        else:
            if User.findUserByEmail({'email': email}):
                findUser = User.findUserByEmail({'email': email})

                if(findUser.status.id == user_status_enum.User_status.Blocked.value):
                    flash('Your account is blocked!', 'login_error')
                    is_valid = False

        return is_valid



    # API

    # Followers and Following data
    @classmethod
    def getFollowersByUserIdAPI(cls, data):
        query = "Select * from users follower inner join followers F on F.follower = follower.id inner join users followed on F.followed = followed.id where followed.id = %(userId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)
        return results

    @classmethod
    def getFollowingByUserIdAPI(cls, data):
        query = "Select * from users followed inner join followers F on F.followed = followed.id inner join users following on F.follower = following.id where following.id = %(userId)s;"
        results = connectToMySQL('peep_app_schema').query_db(query, data)
        return results

