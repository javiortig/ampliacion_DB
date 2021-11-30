import json
import random
import string
import datetime

FIRST_NAMES=('John','Andy','Joe', 'Lucas', 'Juan', 'Ekaitz', 'Javi', 'Miguel', 'Maria', 'Josefa', 'Juana', 'Meri', 'Margarita', 'Angela')
SECOND_NAMES=('Johnson','Smith','Williams', 'Arriola', 'Orti, Garcia', 'Mayoral', 'Valdes', 'G', 'F', 'W', 'O', 'P', 'Q', 'Z', 'X', 'C', 'V')

person_names = set()

UNIVERSITY_NAMES = ['University of Seville', 'University of Malaga', 'International University of Andalusia', 'Pablo de Olavide University', 'Loyola', 'University of Zaragoza', 'University of Oviedo', 'University of the Balearic Islands'
    'IE University', 'Universidad Isabel I', 'Pontifical University of Salamanca', 'Autonomous University of Barcelona', 'University of Girona', 'Open University of Catalonia', 'University of Vic', 'University of Vigo', 
    'Universidad Carlos III de Madrid', 'Universidad Rey Juan Carlos (URJC)', ' Universidad de Alcala de Henares (UAH)', 'Autonomous University of Barcelona', 'Universidad Complutense de Madrid (UCM)', 'UTAD', 'UFV', 'EAE']


COMPANY_NAMES = ['A&M Records', 'Apple', 'IBM', 'Microsoft', 'Oracle', 'Sqw', 'Coca cola', 'Google', 'Bezoya', 
    'Lanjaron', 'Metro', 'Endesa', 'Waste co', 'Doors inc', 'Hiphonic', 'MetConnect', 
    'Rentoor', 'Kiddily', 'Jumpsync', 'Conceptial co', 'VisionSwipe inc', 'Drivemo', 'Deductly', 
    'Shipplier', 'TechTack', 'Digimail', 'asic', 'ABC', 'Acer ', 'Nvidia']

def generate_names_list(n):
    for i in range(n):
        person_names.add(random.choice(FIRST_NAMES) + ' ' + random.choice(SECOND_NAMES))

def generate_random_string(len) -> str:
    cs = string.ascii_lowercase
    return ''.join(random.choice(cs) for i in range(len)) 

def generate_random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

def get_person_name()-> str:
    res = None
    try:
        res = person_names.pop()
    finally:
        if not res:
            return generate_random_string(random.randint(6, 19))
        else:
            return res

def get_university_name() -> str:
    res = None
    try:
        res = UNIVERSITY_NAMES.pop()
    finally:
        if not res:
            return generate_random_string(random.randint(8, 16))
        else:
            return res

def get_company_name() -> str:
    res = None
    try:
        res = UNIVERSITY_NAMES.pop()
    finally:
        if not res:
            return generate_random_string(random.randint(6, 16))
        else:
            return res



n = int(input("Data size:"))
result = {}
result['users'] = []
result['relations'] = []
result['chats'] = []
result['publishings'] = []

generate_names_list(n)

# Generate user:
for i in range(n):
    user = {}
    type_choise = random.randint(0, 3)

    if type_choise < 2:
        user['username'] = get_person_name()
        user['type'] = 'basic'

    elif type_choise == 2:
        user['username'] = get_university_name()
        user['type'] = 'university'

    elif type_choise == 3:
        user['username'] = get_company_name()
        user['type'] = 'company'

    # Append results
    if user:
        result['users'].append(user)

# Generate relations between users:
for u in result['users']:
    count_choise = random.randint(0, 3)
    to_list = random.sample(result['users'], count_choise)

    if (u in to_list):
        continue
    else:
        for t in to_list:
            relation = {}
            relation['from'] = u['username']
            relation['to'] = t['username']
            if (t['type'] == 'company'):
                relation['type'] = 'work'

            elif (t['type'] == 'university'):
                relation['type'] = 'academic'

            else:
                k = random.randint(0, 1)
                if (k == 0):
                    relation['type'] = 'family'
                else:
                    relation['type'] = 'friend'

            result['relations'].append(relation)
                
# Generate publishings:
d1 = datetime.datetime.strptime('1/1/2001 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')
for u in result['users']:
    has_pubs = random.randint(0, 2)

    if (has_pubs > 1):
        count_choise = random.randint(0, 5)
        for i in range(count_choise):
            pub = {}
            pub['author'] = u['username']
            pub['title'] = generate_random_string(9)
            pub['body'] = generate_random_string(40)
            pub['date'] = str(generate_random_date(d1,d2)).replace(' ', 'T') + '[Europe/Madrid]'
            count_choise = random.randint(1, 5)
            mention_list = random.sample(result['users'], count_choise)
            mention_list = [u['username'] for u in mention_list]
            pub['mentions'] = mention_list

            result['publishings'].append(pub)
    else:
        continue

# Generate chats:
n_chats = random.randint(1, n)
users = [u['username'] for u in result['users']]
random.shuffle(users)
for i in range(n_chats):
    chat = {}
    chat['messages'] = []
    print(i)
    if (len(users) <= 2):
        break

    chat['from'] = users.pop()
    chat['to'] = users.pop()

    if chat['from'] == chat['to']:
        continue

    chat_starting_date = generate_random_date(d1,d2)
    n_messages = random.randint(1, 25)
    for j in range(n_messages):
        mes = {}
        mes['body'] = generate_random_string(20)
        mes['sec'] = j
        mes['date'] = str(chat_starting_date + datetime.timedelta(hours=j)).replace(' ', 'T') + '[Europe/Madrid]'

        r_bit = random.randint(0, 1)
        if r_bit == 0:
            mes['from'] = chat['to']
            mes['to'] = chat['from']
        else:
            mes['from'] = chat['from']
            mes['to'] = chat['to']

        chat['messages'].append(mes)

    chat['sec'] = j
    result['chats'].append(chat)

print('n_chats = ' + str(n_chats))

with open('data.json', 'w') as fp:
    json.dump(result, fp)