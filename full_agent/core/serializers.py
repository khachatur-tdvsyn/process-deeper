import dataclasses, json

DATACLASS_IDENTIFIER = 'dataclass_name'

class DataclassJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return {DATACLASS_IDENTIFIER: o.__class__.__name__} | dataclasses.asdict(o)
            return super().default(o)