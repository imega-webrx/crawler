import json


class BaseModelMeta(type):
    model = None


class BaseSerializer(metaclass=BaseModelMeta):
    def __init__(self, data):
        self._data = data
        self.opts = self.Meta

    @property
    def data(self):
        if isinstance(self._data, self.opts.model):
            self._data = self.serialize_to_json()
            return self._data
        elif isinstance(self._data, dict):
            self._data = self.serialize_to_model()
            return self._data
        return

    def serialize_to_json(self, value=None):
        data = dict()
        for field in self.opts.model._fields:
            key, value = field, getattr(self._data, field)
            data.update({key: value})
        return json.dumps(data)

    def serialize_to_model(self):
        data: dict = json.loads(self._data)
        return self.opts.model(**data)
