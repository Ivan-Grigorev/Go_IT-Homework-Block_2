from abc import ABC, abstractmethod
import pickle
import json


class SerializationInterface(ABC):

    @abstractmethod
    def serialize(self, data, file):
        pass


class SerializeJson(SerializationInterface):
    def serialize(self, data, file):
        with open(file, 'wb') as f:
            return json.dump(data, f)


class SerializePickle(SerializationInterface):
    def serialize(self, data, file):
        with open(file, 'wb') as f:
            return pickle.dump(data, f)

