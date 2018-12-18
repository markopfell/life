import requests
import json

job_url = 'https://www.google.com/search?q=jobs&oq=jobs&aqs=chrome..69i57j69i61l2j69i60j0l2.582j1j7&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwjN4qabsqjfAhWuHTQIHfCxDl4Qp4wCMAJ6BAgBECo#fpstate=tldetail&htidocid=viEGMcI6rAZUtNMYAAAAAA%3D%3D&htitab=save&htivrt=jobs'

r = requests.get(job_url)

if r.status_code == 200:
    r.text



