from flask import Flask, request, jsonify, session
from peep_app import app
from peep_app.models import userModel, postModel, collectionModel

#  --------------------  API   -------------------- 

@app.route('/api/collections/<int:ownerId>', methods=['GET'])
def get_all_by_ownerAPI(ownerId):

    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        collections = collectionModel.Collection.get_all_by_owner({'ownerId': ownerId})
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

            collections_data.append(current)

        response = {
            'collections': collections_data
        }

        if currentUser == None:
            return jsonify({'message': 'User not found', 'status': 'danger'}), 404
        else:
            return jsonify({'data': response, 'status': 'success', 'currentUser': userId}), 200
  

@app.route('/api/collections/search', methods=['GET'])
def search_by_name_and_owner():

    name = request.args.get('name')
    print(name)

    userId = None

    if 'userId' in session:
        userId = session['userId']
        currentUser = userModel.User.findUserById({'userId': userId})

        request_data = {
            'search': name,
            'userId': currentUser.id
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

            collections_data.append(current)

        response = {
            'collections': collections_data
        }

        if currentUser == None:
            return jsonify({'message': 'User not found', 'status': 'danger'}), 404
        else:
            return jsonify({'data': response, 'status': 'success', 'currentUser': userId}), 200


