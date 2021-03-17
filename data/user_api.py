import flask
from flask import jsonify
from flask import request

from data.users import User
from data import db_session

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user', methods=['GET'])
def get_user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {
            'user':
                [item.to_dict(only=('id',
                                    'surname',
                                    'name',
                                    'age',
                                    'position',
                                    'speciality',
                                    'address',
                                    'email',
                                    'hashed_password',
                                    'modified_date',
                                    'city_from'))
                 for item in user]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'user': user.to_dict(only=('id',
                                       'surname',
                                       'name',
                                       'age',
                                       'position',
                                       'speciality',
                                       'address',
                                       'email',
                                       'hashed_password',
                                       'modified_date',
                                       'city_from'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'email',
                  'hashed_password',
                  'city_from']):
        return jsonify({'error': 'Bad request'})

    if 'id' in request.json:
        ids = list(map(lambda x: x.id, db_sess.query(User).all()))

        if request.json['id'] in ids:
            return jsonify({'error': 'Id already exists'})

        else:
            user = User(
                id=request.json['id'],
                surname=request.json['surname'],
                name=request.json['name'],
                age=request.json['age'],
                position=request.json['position'],
                speciality=request.json['speciality'],
                address=request.json['address'],
                email=request.json['email'],
                hashed_password=request.json['hashed_password'],
                city_from=request.json['city_from']
            )

    else:
        user = User(
            surname=request.json['surname'],
            name=request.json['name'],
            age=request.json['age'],
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['address'],
            email=request.json['email'],
            hashed_password=request.json['hashed_password'],
            city_from=request.json['city_from']
        )

    db_sess.add(user)
    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'email',
                  'hashed_password',
                  'city_from']):

        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()

    if not user:
        return jsonify({'error': 'Not found'})

    user.surname = request.json['surname'],
    user.name = request.json['name'],
    user.age = request.json['age'],
    user.position = request.json['position'],
    user.speciality = request.json['speciality'],
    user.address = request.json['address'],
    user.email = request.json['email'],
    user.hashed_password = request.json['hashed_password']
    user.city_from = request.json['city_from']
    db_sess.commit()

    return jsonify({'success': 'OK'})