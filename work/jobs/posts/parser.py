import nltk
import numpy
import matplotlib
# TODO get remote working?
import requests

from nltk.book import *

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
    post_file = open(file_name).read()
    post = post_file.read()
    post_file.close()
    is_post = True

if is_post:
    post = post.split('\n')
    cleaned_post = []

    for line in post:
        cleaned_post.append(line.strip())

    cleaned_post_key_words = []

    sorted(set())

    for line in cleaned_post:
        line.strip()

    line = list(set(cleaned_post))

    # for line in cleaned_post:
    #     print(line)

# text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
print(sorted(set(text3)))

