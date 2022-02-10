from flask import Flask, render_template, request, redirect, session, flash, jsonify, json
from peep_app import app
from peep_app.models import postModel, userModel

# @app.route('/new/post/<int:authorId>', methods=['POST'])
# def new_post(authorId):

#     if not postModel.Post.validatePost(request.form):
#         return redirect('/')

#     data = {
#         'content': request.form['content'],
#         'authorId': authorId
#     }

#     result = postModel.Post.save(data)

#     if type (result) is int and result > 0:
#         return redirect('/dashboard')
#     else:
#         flash('An error occurred. Please try again', 'post_error')
#         return redirect('/')


# @app.route('/like/add/<int:postId>/<int:userId>', methods=['POST'])
# def add_like(postId, userId):

#     data = {
#         'postId': postId,
#         'userId': userId
#     }

#     postModel.Post.add_like(data)
#     # return jsonify(),201
#     return redirect('/dashboard')

# @app.route('/like/remove/<int:postId>/<int:userId>', methods=['POST'])
# def remove_like(postId, userId):

#     data = {
#         'postId': postId,
#         'userId': userId
#     }

#     postModel.Post.remove_like(data)
#     # return jsonify(),201
#     return redirect('/')


#  --------------------  API   -------------------- 

@app.route('/api/posts/usersWhoLike/<int:postId>', methods=['GET'])
def usersWhoLikePost(postId):
    result = postModel.Post.get_users_who_like_API({'postId': postId})
    return jsonify(result), 200


@app.route('/api/posts/all', methods=['GET'])
def get_all_posts_API():
    userId = None

    if 'userId' in session:
        userId = session['userId']

        posts = postModel.Post.get_all({'userId': userId})

        mappedPosts = []

        for post in posts:
            current_post = {
                'id': post.id,
                'content': post.content,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'author': {
                    'id': post.author.id,
                    'firstname': post.author.firstname,
                    'lastname': post.author.lastname,
                    'username': post.author.username
                },
                'time_ago': post.time_ago,
                'likes': post.likes,
                'isLiked': post.isLiked
            }
            
            users_list = []

            for data in post.users_who_like:
                current_user = {
                    'id': data.id,
                    'firstname': data.firstname,
                    'lastname': data.lastname,
                    'username': data.username
                }

                users_list.append(current_user)

            collections_list = []

            for data in post.in_collections:
                current_collection = {
                    'id': data.id,
                    'name': data.name,
                    'description': data.description,
                    'created_at' : data.created_at,
                    'updated_at' : data.updated_at
                }

                collections_list.append(current_collection)

            current_post['in_collections'] = collections_list
            current_post['users_who_like'] = users_list
            mappedPosts.append(current_post)

        response = {
            'posts': mappedPosts
        }

        if posts == None:
            return jsonify({'message': 'Posts not found', 'status': 'danger'}), 404
        else:
            return jsonify({'data': response, 'status': 'success', 'currentUser': userId}), 200



@app.route('/api/posts/like/<int:postId>/by/<int:userId>', methods=['POST'])
def add_likeAPI(postId, userId):

    data = {
        'postId': postId,
        'userId': userId
    }

    postModel.Post.add_like(data)
    return jsonify({'message': 'Post liked'}), 200

@app.route('/api/posts/unlike/<int:postId>/by/<int:userId>', methods=['POST'])
def remove_likeAPI(postId, userId):

    data = {
        'postId': postId,
        'userId': userId
    }

    postModel.Post.remove_like(data)
    return jsonify({'message': 'Post unliked'}), 200

@app.route('/api/posts/new', methods=['POST'])
def new_postAPI():

    userId = None

    if 'userId' in session:
        userId = session['userId']

    authorId = userId

    new_data = json.loads(request.data.decode('UTF-8'))

    if postModel.Post.validatePost(new_data):
        data = {
            'content': new_data['content'],
            'authorId': authorId
        }

        result = postModel.Post.save(data)

        if type (result) is int:
            return jsonify({'message': 'Post created successfully', 'status': 'success'}), 201
    else:
        return jsonify({'message': 'Something went wrong', 'status': 'danger'}), 404