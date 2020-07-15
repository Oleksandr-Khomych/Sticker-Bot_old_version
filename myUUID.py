import uuid
import random


def get_uuid():
    myuuid = uuid.uuid4()
    return myuuid


def get_id():
    return random.randint(100000, 999999)
