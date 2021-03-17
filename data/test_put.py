from requests import put, get

# ok
print(put('http://localhost:5000/api/jobs/3',
          json={'collaborators': '',
                'is_finished': True,
                'job': 'test_put_8',
                'team_leader': 1,
                'type': 3,
                'work_size': 99}).json())


# строка
print(put('http://localhost:5000/api/jobs/q',
          json={'collaborators': '',
                'is_finished': True,
                'job': 'test_put_8',
                'team_leader': 1,
                'type': 3,
                'work_size': 99}).json())

# пустой запрос
print(put('http://localhost:5000/api/jobs/3').json())

# не хватает полей
print(put('http://localhost:5000/api/jobs/3',
          json={'job': 'test_post_failure'}).json())

# id не существует
print(put('http://localhost:5000/api/jobs/999',
          json={'collaborators': '',
                'is_finished': True,
                'job': 'test_put_1',
                'team_leader': 1,
                'type': 3,
                'work_size': 11}).json())

print(get('http://localhost:5000/api/jobs').json())
print(len(get('http://localhost:5000/api/jobs').json()['jobs']))
