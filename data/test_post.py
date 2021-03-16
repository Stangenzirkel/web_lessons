from requests import post
print(post('http://localhost:5000/api/jobs').json())

print(post('http://localhost:5000/api/jobs',
           json={'job': 'test_post_failure'}).json())

print(post('http://localhost:5000/api/jobs',
           json={'collaborators': '',
                 'is_finished': True,
                 'job': 'test_post',
                 'team_leader': 1,
                 'type': 3,
                 'work_size': 10}))
