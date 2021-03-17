import flask
from flask import jsonify
from flask import request

from data.jobs import Jobs
from data import db_session

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
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['team_leader',
                  'job',
                  'work_size',
                  'collaborators',
                  'is_finished',
                  'type']):
        return jsonify({'error': 'Bad request'})

    if 'id' in request.json:
        ids = list(map(lambda x: x.id, db_sess.query(Jobs).all()))

        if request.json['id'] in ids:
            return jsonify({'error': 'Id already exists'})

        else:
            jobs = Jobs(
                id=request.json['id'],
                team_leader=request.json['team_leader'],
                job=request.json['job'],
                work_size=request.json['work_size'],
                collaborators=request.json['collaborators'],
                is_finished=request.json['is_finished'],
                type=request.json['type']
            )

    else:
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

    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def put_jobs(jobs_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    elif not all(key in request.json for key in
                 ['team_leader',
                  'job',
                  'work_size',
                  'collaborators',
                  'is_finished',
                  'type']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()

    if not job:
        return jsonify({'error': 'Not found'})

    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.type = request.json['type']
    job.is_finished = request.json['is_finished']
    db_sess.commit()

    return jsonify({'success': 'OK'})