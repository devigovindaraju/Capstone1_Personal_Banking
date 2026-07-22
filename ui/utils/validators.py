import json


def validate_json(data):

    try:

        return json.loads(data)


    except json.JSONDecodeError:

        return None