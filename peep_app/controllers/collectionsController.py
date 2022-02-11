from flask import Flask, request, jsonify, session, redirect, render_template, json
from peep_app import app
from peep_app.models import userModel, postModel, collectionModel

@app.route('/users/profile/<int:profileId>/collections', methods=['GET'])
def collections(profileId):

    userId = None

    if 'userId' in session:
        userId = session['userId']
        isLogged = True

        currentUser = userModel.User.findUserById({'userId': userId})

        # Si hay userId pero no encuentra un usuario, hace logout
        if currentUser == None:
            return redirect('/logout')
        
        user = userModel.User.findUserById({'userId': profileId})

        if user == None or currentUser.id != user.id:
            return redirect('/')
    
        return render_template(
            'collection.html',
            currentUser = currentUser,
            isLogged = isLogged,
            user = user
        )
    else:
        return redirect('/')


#  --------------------  API   -------------------- 

@app.route('/api/collections/<int:collectionId>/add/<int:postId>', methods=['POST'])
def add_post_to_collectionAPI(collectionId, postId):
    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        request_data = {
            'collectionId': collectionId,
            'ownerId': currentUser.id
        }
        
        collection = collectionModel.Collection.find_collection_by_owner_and_id(request_data)

        if collection != None:

            data = {
                'collectionId': collectionId,
                'postId': postId
            }

            collectionModel.Collection.add_post_to_collection(data)

            return jsonify({'message': 'Post saved to collection', 'status': 'success'}), 200
        else:
            return jsonify({'message': 'Something went wrong', 'status': 'danger'}), 404


@app.route('/api/collections/<int:collectionId>/remove/<int:postId>', methods=['POST'])
def remove_post_to_collectionAPI(collectionId, postId):
    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        request_data = {
            'collectionId': collectionId,
            'ownerId': currentUser.id
        }
        
        collection = collectionModel.Collection.find_collection_by_owner_and_id(request_data)

        if collection != None:

            data = {
                'collectionId': collectionId,
                'postId': postId
            }

            collectionModel.Collection.remove_post_from_collection(data)

            return jsonify({'message': 'Post removed from collection', 'status': 'success'}), 200
        else:
            return jsonify({'message': 'Something went wrong', 'status': 'danger'}), 404


@app.route('/api/collections/new', methods=['POST'])
def createCollectionAPI():
    userId = None

    if 'userId' in session:
        userId = session['userId']

    ownerId = userId

    new_data = json.loads(request.data.decode('UTF-8'))

    if collectionModel.Collection.validateCollection(new_data):
        data = {
            'name': new_data['name'],
            'description': new_data['description'],
            'ownerId': ownerId
        }

        result = collectionModel.Collection.save(data)

        if type (result) is int:
            return jsonify({'message': 'Post created successfully', 'status': 'success'}), 201
    else:
        return jsonify({'message': 'Something went wrong', 'status': 'danger'}), 404


@app.route('/api/collections/new/fast', methods=['POST'])
def createFastCollectionAPI():
    userId = None

    if 'userId' in session:
        userId = session['userId']

    ownerId = userId

    new_data = json.loads(request.data.decode('UTF-8'))

    if collectionModel.Collection.validateFastCollection(new_data):
        data = {
            'name': new_data['name'],
            'ownerId': ownerId
        }

        result = collectionModel.Collection.saveFast(data)

        if type (result) is int:
            return jsonify({'message': 'Post created successfully', 'status': 'success'}), 201
    else:
        return jsonify({'message': 'Something went wrong', 'status': 'danger'}), 404


@app.route('/api/collections/<int:ownerId>/search', methods=['GET'])
def search_by_name_and_ownerAPI(ownerId):

    name = request.args.get('name')
    limit = request.args.get('limit')

    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        request_data = {
            'search': name,
            'userId': ownerId,
            'limit': limit
        }

        collections = collectionModel.Collection.search_by_name_and_owner(request_data)
        collections_data = []

        for data in collections:
            current = {
                'id': data.id,
                'name': data.name,
                'description': data.description,
                'created_at': data.created_at,
                'updated_at': data.updated_at,
                'owner': {
                    'id': data.owner.id,
                    'firstname': data.owner.firstname,
                    'lastname': data.owner.lastname,
                    'username': data.owner.username
                },
            }

            posts_data = []

            for post in data.saved_posts:
                current_post = {
                    'id': post.id,
                    'content': post.content,
                    'created_at': post.created_at,
                    'updated_at': post.updated_at
                }

                posts_data.append(current_post)

            current['posts'] = posts_data
            collections_data.append(current)

        response = {
            'collections': collections_data
        }

        if currentUser == None:
            return jsonify({'message': 'User not found', 'status': 'danger'}), 404
        else:
            return jsonify({'data': response, 'status': 'success', 'currentUser': userId}), 200
  

@app.route('/api/collections/search', methods=['GET'])
def search_by_name_and_logged_userAPI():

    name = request.args.get('name')
    limit = request.args.get('limit')

    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        request_data = {
            'search': name,
            'userId': currentUser.id,
            'limit': limit
        }

        collections = collectionModel.Collection.search_by_name_and_owner(request_data)
        collections_data = []

        for data in collections:
            current = {
                'id': data.id,
                'name': data.name,
                'description': data.description,
                'created_at': data.created_at,
                'updated_at': data.updated_at,
                'owner': {
                    'id': data.owner.id,
                    'firstname': data.owner.firstname,
                    'lastname': data.owner.lastname,
                    'username': data.owner.username
                }
            }

            posts_data = []

            for post in data.saved_posts:
                current_post = {
                    'id': post.id,
                    'content': post.content,
                    'created_at': post.created_at,
                    'updated_at': post.updated_at
                }

                posts_data.append(current_post)

            current['posts'] = posts_data
            collections_data.append(current)

        response = {
            'collections': collections_data
        }

        if currentUser == None:
            return jsonify({'message': 'User not found', 'status': 'danger'}), 404
        else:
            return jsonify({'data': response, 'status': 'success', 'currentUser': userId}), 200


