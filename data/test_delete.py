from requests import delete, get

# 405
print(delete('http://localhost:5000/api/jobs').json())

# ok
print(delete('http://localhost:5000/api/jobs/1').json())

# нет id
print(delete('http://localhost:5000/api/jobs/999').json())

# строка
print(delete('http://localhost:5000/api/jobs/q').json())

print(get('http://localhost:5000/api/jobs').json())
print(len(get('http://localhost:5000/api/jobs').json()['jobs']))
