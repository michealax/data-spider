import json


class CustomerEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__
