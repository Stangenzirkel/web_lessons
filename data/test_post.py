from requests import post, get

# все ок (без id)
print(post('http://localhost:5000/api/jobs',
           json={'collaborators': '',
                 'is_finished': True,
                 'job': 'test_post',
                 'team_leader': 1,
                 'type': 3,
                 'work_size': 11}).json())

# все ок (c id)
print(post('http://localhost:5000/api/jobs',
           json={'id': 9,
                 'collaborators': '',
                 'is_finished': True,
                 'job': 'test_post_8',
                 'team_leader': 1,
                 'type': 3,
                 'work_size': 11}).json())

# пустой запрос
print(post('http://localhost:5000/api/jobs').json())

# не хватает полей
print(post('http://localhost:5000/api/jobs',
           json={'job': 'test_post_failure'}).json())

# id существует
print(post('http://localhost:5000/api/jobs',
           json={'id': 1,
                 'collaborators': '',
                 'is_finished': True,
                 'job': 'test_post_1',
                 'team_leader': 1,
                 'type': 3,
                 'work_size': 11}).json())

print(get('http://localhost:5000/api/jobs').json())
print(len(get('http://localhost:5000/api/jobs').json()['jobs']))
