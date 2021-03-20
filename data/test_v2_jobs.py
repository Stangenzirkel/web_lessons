from requests import get, post, delete


print(get('http://localhost:5000/api/v2/jobs').json())
print(len(get('http://localhost:5000/api/v2/jobs').json()['jobs']))
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/999').json())
print(get('http://localhost:5000/api/v2/jobs/q').json())


print(delete('http://localhost:5000/api/v2/jobs/1').json())
print(delete('http://localhost:5000/api/v2/jobs/999').json())
print(delete('http://localhost:5000/api/v2/jobs/q').json())

print(get('http://localhost:5000/api/v2/jobs').json())

for i in range(20):
    print(post('http://localhost:5000/api/v2/jobs',
               json={'collaborators': '',
                     'is_finished': True,
                     'job': f'test{i}_job',
                     'team_leader': 2,
                     'type': 1,
                     'work_size': i}).json())

print(post('http://localhost:5000/api/v2/jobs',
           json={'job': 'test_F1'}).json())

print(post('http://localhost:5000/api/v2/jobs'))

for item in get('http://localhost:5000/api/v2/jobs').json()['jobs']:
    print(item)
