from flask import Flask, jsonify,render_template, request, redirect, session, flash, json
from peep_app import app
from peep_app.models import userModel, postModel, countryModel
from flask_bcrypt import Bcrypt
from peep_app.constants import user_status_enum

bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    if not userModel.User.validateRegister(request.form):
        return redirect('/')

    encryptedPassword = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'email': request.form['email'],
        'password': encryptedPassword,
        'birthday': request.form['birthday'],
        'countryId': request.form['country'],
    }

    result = userModel.User.register_user(data)

    if type (result) is int and result > 0:
        session['userId'] = result
        return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    if not userModel.User.validateLogin(data):
        return redirect('/')

    user = userModel.User.findUserByEmail(data)

    if user != None:
        if user.status.id == user_status_enum.User_status.Blocked.value:
            return redirect('/blocked')

        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Invalid Email / Password', 'login_error')
            return redirect('/')
    
        session['userId'] = user.id
        return redirect('/dashboard')


@app.route('/users/profile/<int:profileId>/edit', methods=['GET'])
def edit_profile(profileId):
    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

        currentUser = userModel.User.findUserById({'userId': userId})
        user = userModel.User.findUserById({'userId': profileId})

        countries = countryModel.Country.get_all()

        if user.id != currentUser.id:
            return redirect('/')

        return render_template(
            'edit_profile.html',
            currentUser = currentUser,
            isLogged = isLogged,
            countries = countries
        )

    else:
        return redirect('/')


@app.route('/users/profile/<int:profileId>', methods=['GET'])
def profile(profileId):

    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

        currentUser = userModel.User.findUserById({'userId': userId})

        # Si hay userId pero no encuentra un usuario, hace logout
        if currentUser == None:
            return redirect('/logout')
        
        user = userModel.User.findUserById({'userId': profileId})

        isFollowed = userModel.User.userIsFollower({'followedId': profileId, 'userId': userId})

        if user == None:
            return redirect('/')
    
        return render_template(
            'profile.html',
            currentUser = currentUser,
            isLogged = isLogged,
            user = user,
            isFollowed = isFollowed
        )
    else:
        return redirect('/')
        

#  --------------------  API   -------------------- 

@app.route('/api/users/follow/<int:followedId>/by/<int:followerId>', methods=['POST'])
def followUserAPI(followedId, followerId):

    follow_data = {
        'followedId': followedId,
        'followerId': followerId
    }

    result = userModel.User.follow_user(follow_data)

    print(result)

    if type (result) is int:
        return jsonify({'message': 'User followed', 'status': 'success'}), 201
    else:
        return jsonify({'message': 'An error occurred', 'status': 'danger'}), 404


@app.route('/api/users/unfollow/<int:followedId>/by/<int:followerId>', methods=['POST'])
def unfollowUserAPI(followedId, followerId):

    follow_data = {
        'followedId': followedId,
        'followerId': followerId
    }

    followed = userModel.User.findUserById({'userId': followedId})
    follower = userModel.User.findUserById({'userId': followerId})

    if followed != None and follower != None:
        userModel.User.unfollow_user(follow_data)
        return jsonify({'message': 'User unfollowed', 'status': 'success'}), 201
    else:
        return jsonify({'message': 'User not found', 'status': 'danger'}), 404


# Test mapping (manual)
@app.route('/api/users/profile/<int:profileId>', methods=['GET'])
def profileAPI(profileId):

    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        user = userModel.User.findUserById({'userId': profileId})
        isFollowed = userModel.User.userIsFollower({'followedId': profileId, 'userId': currentUser.id})
        user.followed = isFollowed

        followers = userModel.User.getFollowersByUserId({'userId': user.id})
        following = userModel.User.getFollowingByUserId({'userId': user.id})
        posts = postModel.Post.get_all_by_author({'userId': user.id, 'requesterId': currentUser.id})

        followers_data = []
        following_data = []
        posts_data = []

        for data in followers:
            current = {
                'id': data.id,
                'firstname': data.firstname,
                'lastname': data.lastname,
                'username': data.username
            }
            followers_data.append(current)

        for data in following:
            current = {
                'id': data.id,
                'firstname': data.firstname,
                'lastname': data.lastname,
                'username': data.username
            }
            following_data.append(current)

        for data in posts:
            current = {
                'id': data.id,
                'content': data.content,
                'created_at': data.created_at,
                'updated_at': data.updated_at,
                'author': {
                    'id': data.author.id,
                    'firstname': data.author.firstname,
                    'lastname': data.author.lastname,
                    'username': data.author.username
                },
                'time_ago': data.time_ago,
                'likes': data.likes,
                'isLiked': data.isLiked,
                'isSaved': data.isSaved
            }

            in_collections_data = []

            for collection in data.in_collections:
                current_collection = {
                    'id': collection.id,
                    'name': collection.name,
                    'description': collection.description,
                    'created_at': collection.created_at,
                    'updated_at': collection.updated_at
                }
                in_collections_data.append(current_collection)

            current['in_collections'] = in_collections_data

            # if data.in_collections:
            #     if len(data.in_collections) > 0:
            #         current['isSaved'] = True

            posts_data.append(current)

        response = {
            'user': {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'birthday': user.birthday,
                'gender': user.gender,
                'email': user.email,
                'password': user.password,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'status': {
                    'id': user.status.id,
                    'name': user.status.name
                },
                'country': user.country,
                'role': user.role,
                'followers': followers_data,
                'following': following_data,
                'followed': user.followed,
                'posts': posts_data
            }
        }

        if user == None or currentUser == None:
            return jsonify({'message': 'User not found', 'status': 'danger'}), 404
        else:
            return jsonify({'data': response, 'status': 'success', 'currentUser': userId}), 200


@app.route('/api/users/<int:profileId>/edit', methods=['PUT'])
def updateUserAPI(profileId):
    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        user = userModel.User.findUserById({'userId': profileId})

        if currentUser.id != user.id:
            return jsonify({'message': 'You can not edit this user', 'status': 'danger'}), 403

        new_data = json.loads(request.data.decode('UTF-8'))

        if userModel.User.validateEditProfile(new_data):
            data = {
                'firstname': new_data['firstname'],
                'lastname': new_data['lastname'],
                'birthday' : new_data['birthday'],
                'countryId': new_data['country'],
                'userId': user.id
            }

            userModel.User.update_user(data)

            return jsonify({'message': 'User edited successfully', 'status': 'success'}), 201
        else:
            return jsonify({'message': 'Validation fails', 'status': 'danger'}), 404
    else:
        return jsonify({'message': 'User not logged', 'status': 'danger'}), 404