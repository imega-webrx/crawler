import json

from crawler.utils import save_in_json


class BaseModelMeta(type):
    model = None


class BaseSerializer(metaclass=BaseModelMeta):
    def __init__(self, data, many=False):
        self._data = data
        self.many = many
        self.opts = self.Meta
        self._data_to_save = None

    @property
    def data(self):
        obj = self._data
        if isinstance(obj, list):
            if obj:
                obj = obj[0]
            else:
                obj = None

        if isinstance(obj, self.opts.model):
            data = self.serialize_to_json()
            self._data_to_save = data
            return data
        elif isinstance(obj, (str, bytes)):
            data = self.serialize_to_model()
            self._data_to_save = data
            return data
        return

    def serialize_to_json(self, value=None):
        if self.many:
            all_data = []
            for obj in self._data:
                data = dict()
                for field in self.opts.model._fields:
                    key, value = field, getattr(obj, field)
                    data.update({key: value})
                all_data.append(data)
            return json.dumps(all_data, indent=4, ensure_ascii=False)
        data = dict()
        for field in self.opts.model._fields:
            key, value = field, getattr(self._data, field)
            data.update({key: value})
        return json.dumps(data, indent=4, ensure_ascii=False)

    def serialize_to_model(self):
        data: dict = json.loads(self._data)
        return self.opts.model(**data)

    def save(self, filename: str):
        if not self._data_to_save:
            self.data

        if isinstance(self._data_to_save, (str, bytes)):
            save_in_json(self._data_to_save, filename)
            return "OK"
        return "Data contain not a JSON-Object"
