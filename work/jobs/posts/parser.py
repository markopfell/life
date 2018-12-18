# TODO use these librarys and get remote working?
import nltk
import numpy
import matplotlib
# TODO get remote working?
import requests
job_url = 'https://g.co/kgs/1QVgZR'
r = requests.get(job_url)

is_remote = False
is_post = False
post = False
file_name = '0,software_engineer_rf_test.txt'

if r.status_code != 200 and is_remote:
    is_post = False

elif r.status_code == 200 and is_remote:
    post = r.text
    is_post = True

elif not is_remote:
    post = open(file_name).read()
    is_post = True

if is_post:
    post = post.split('\n')
    vocabulary = []
    for sentence in post:
        phrases = sentence.split(' ')
        for phrase in phrases:
            vocabulary.append(phrase.lower())

    unique_vocabulary = sorted(list(set(vocabulary)))

    for token in unique_vocabulary:
        print(token)


