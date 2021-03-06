from pymongo import MongoClient

client = MongoClient()

db = client.codr
users = db.users

def update_user(_id, name, token, avatar_url, languages, updated):
    users.save(
        {'_id': _id,
         'name': name,
         'access_token': token,
         'avatar': avatar_url,
         'languages':languages,
         'updated_at': updated
        }
    )

def get_user(_id):
    return users.find_one({'_id' : _id})

def like(source_id, target_id):
    user = get_user(source_id)

    if not user:
        raise ValueError('No user with id %d found' % (source_id, ))

    if not 'likes' in user:
        user['likes'] = []

    user['likes'].append(target_id)

    target = get_user(target_id)

    if not target:
        raise ValueError('No user with id %d found' % (target_id, ))

    if not 'likes' in target:
        target['likes'] = []

    # save changes to db
    users.save(user)

    # return if they are a match
    return source_id in target['likes']

def reject(source_id, target_id):
    user = get_user(source_id)

    if not user:
        raise ValueError('No user with id %d found' % (source_id, ))

    if 'rejects' not in user:
        user['rejects'] = []

    user['rejects'].append(target_id)

    users.save(user)

def get_matches(_id):
    user = get_user(_id)

    if not user:
        raise ValueError('No user with id %d found' % (_id, ))

    matches = []
    if 'likes' in user:
        for like in user['likes']:
            target = get_user(like)
            if 'likes' in target and _id in target['likes']:
                match = get_user(int(like))
                matches.append({'id':like, 'name':match['name']})

    return matches

def get_potential(_id):

    user = get_user(_id)

    if not user:
        raise ValueError('No user with id %d found' % (_id, ))

    if 'likes' not in user:
        user['likes'] = []
    if 'rejects' not in user:
        user['rejects'] = []

    for other in users.find():
        if (other['_id'] not in user['rejects']
            and other['_id'] not in user['likes']
            and other['_id'] != user['_id']):
            return other

    return None

def get_updated_at(_id):
    user = get_user(_id)

    if not user:
        raise ValueError('No user with id %d found' % (_id, ))

    return user['updated-at']
