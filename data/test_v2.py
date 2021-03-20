from requests import get, post, delete


print(get('http://localhost:5000/api/v2/users').json())
print(len(get('http://localhost:5000/api/v2/users').json()['user']))
print(get('http://localhost:5000/api/v2/users/1').json())
print(get('http://localhost:5000/api/v2/users/999').json())
print(get('http://localhost:5000/api/v2/users/q').json())


print(delete('http://localhost:5000/api/v2/users/1').json())
print(delete('http://localhost:5000/api/v2/users/999').json())
print(delete('http://localhost:5000/api/v2/users/q').json())

print(get('http://localhost:5000/api/v2/users').json())

for i in range(20):
    print(post('http://localhost:5000/api/v2/users',
               json={'surname': f'test{i}_surname',
                     'name': f'test{i}_name',
                     'age': i,
                     'position': f'test{i}_position',
                     'speciality': f'test{i}_speciality',
                     'address': f'test{i}_address',
                     'email': f'test{i}_email',
                     'hashed_password': f'test{i}_hashed_password',
                     'city_from': f'test{i}_city_from'}).json())

print(post('http://localhost:5000/api/v2/users',
           json={'surname': 'test_F1'}).json())

print(post('http://localhost:5000/api/v2/users'))

for item in get('http://localhost:5000/api/v2/users').json()['user']:
    print(item)
