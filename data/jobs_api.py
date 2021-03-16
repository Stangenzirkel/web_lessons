import flask
from flask import jsonify
from flask import request

from .jobs import Jobs
from . import db_session

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id',
                                    'team_leader',
                                    'job',
                                    'work_size',
                                    'collaborators',
                                    'start_date',
                                    'end_date',
                                    'is_finished',
                                    'type'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id',
                                       'team_leader',
                                       'job',
                                       'work_size',
                                       'collaborators',
                                       'start_date',
                                       'end_date',
                                       'is_finished',
                                       'type'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader',
                  'job',
                  'work_size',
                  'collaborators',
                  'start_date',
                  'end_date',
                  'is_finished',
                  'type']):
        return jsonify({'error': 'Bad request'})

    try:
        db_sess = db_session.create_session()
        jobs = Jobs(
            team_leader=request.json['team_leader'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            is_finished=request.json['is_finished'],
            type=request.json['type']
        )
        db_sess.add(jobs)
        db_sess.commit()
        print('ok')

    except Exception as error:
        print('error')
        print(str(error))
        return jsonify({'error': str(error)})

    else:
        print('ok')
        return jsonify({'success': 'OK'})