import json
import random
import uuid
import time
from pprint import pprint

import requests

word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

response = requests.get(word_site)
WORDS = list(map(lambda i: i.decode(), response.content.splitlines()))

COURSES = [
    'course-v1:Appsembler+001+2017',
    'course-v1:ASU+ASUxx+2017-1',
    'course-v1:ASU+BB01+2017-1',
    'course-v1:ASU+BBDT02+2017-1',
    'course-v1:ASU+CME01+2017-1',
    'course-v1:ASU+JILL_2018+2018_FA',
    'course-v1:ASU+MM100+2017_1',
    'course-v1:ASU+TBWFC100+2019',
    'course-v1:Canada+TBW100+2019',
    'course-v1:edX+DemoX+Demo_Course',
    'course-v1:PR+CA300BC+2019',
    'course-v1:PR+CME01+2018-1',
]

USERS = list(range(1, 4))


def create_course_structure():
    courses = list()
    for course_id in COURSES[:3]:
        course = dict()
        course['id'] = course_id
        course['sections'] = list()
        for i in range(random.randint(5, 7)):
            section_name = 'Week {0}: {1}'.format(i + 1, random.choice(WORDS).title())
            sub_sections = list()
            for j in range(random.randint(3, 6)):
                sub_sections.append(dict(name=random.choice(WORDS), units=list(range(1, random.randint(4, 7) + 1))))
            course['sections'].append(dict(name=section_name, subsections=sub_sections))
        courses.append(course)

    return courses


def generate_payload(course, amount=10):
    for _ in range(amount):
        section = random.choice(course['sections'])
        subsection = random.choice(section['subsections'])
        paylod = dict(cid=course['id'], c=section['name'], s=subsection['name'], u=random.choice(subsection['units']))
        yield json.dumps(paylod)


def generate_links():
    result = []
    count = 1
    for course_structure in create_course_structure():
        for i in generate_payload(course_structure, amount=10):
            result.append({"link_id": i, 'id': count})
            count += 1

    return result


def generate_visits(quantity):
    # uuid.uuid4().hex

    # timestamp=1574430006&user_id=6da5ef054977cb2691eff7ae4094c469
    delta = 0
    for _ in range(quantity):
        yield {"visit_id": 'timestamp={}&user_id={}'.format(int(time.time()) + delta, random.choice(USERS))}
        delta += 10


def generate_engagement_data(quantity):
    delta = 0
    for _ in range(quantity):
        yield {
            "engagement": random.uniform(0.0, 99.9),
            "emo_anger": random.uniform(0.0, 99.9),
            "timestamp": int(time.time()),
            "emo_fear": random.uniform(0.0, 99.9),
            "attention": random.uniform(0.0, 99.9),
            "focus": random.uniform(0.0, 99.9),
            "emo_happy": random.uniform(0.0, 99.9),
            "emo_sadness": random.uniform(0.0, 99.9),
            "wasm": "wasm-cybert-0.7",
            "emo_contempt": random.uniform(0.0, 99.9),
            "offset": random.randint(0, 100),
            "emo_surprise": random.uniform(0.0, 99.9),
        }
        delta += 10


foo = {
    'id': 'course-v1:Appsembler+001+2017',
    'sections': [
        {
            'name': 'foo',
            'subsections': [
                {'name': 'bla', 'units': [1, 2, 2, 3, 4]},
                {'name': 'bla', 'units': [1, 2, 2, 3, 4]},
                {'name': 'bla', 'units': [1, 2, 2, 3, 4]},
            ],
        }
    ],
}


def main():
    links = generate_links()
    links_data = dict(links=links)
    visits = []
    for link in links:
        visits.append(dict(id=link['id'] + 1, visits=list(generate_visits(random.randint(4, 6)))))
    visits_data = dict(visits=visits)

    engagements = []
    for visit in visits:
        for i in visit['visits']:
            engagements.append(
                dict(id=i['visit_id'], engagements=list(generate_engagement_data(random.randint(4, 6))))
            )

    engagement_data = dict(engagements=engagements)

    with open('db.json', 'w', encoding='utf-8') as f:
        # links_data.update(visits_data)
        # links_data.update(engagement_data)
        json.dump(links_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()

foo = {"links": [{"id": 1, "title": "hello"}], "profile": {"name": "typicode"}}

posts = {"posts": [{"id": 1, "title": "hello"}], "profile": {"name": "typicode"}}

post = {"id": 1, "title": "hello"}
