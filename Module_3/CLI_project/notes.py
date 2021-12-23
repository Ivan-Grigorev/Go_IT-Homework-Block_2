import json
import difflib
from operator import itemgetter


class NoteRecord:
    counter = 0

    def __init__(self, note='', tag=None, title=''):
        self.note = note
        self.title = title
        self.tag = tag
        self.filename = 'data.json'
        self.record = {
            'id': NoteRecord.counter,
            'title': self.title,
            'note': self.note,
            'tag': self.tag
        }

    @staticmethod
    def tag_search(list_of_notes, input_tag):
        tag_list = []
        for i in map(lambda x: x['tag'], list_of_notes):
            tag_list.extend(i)
        tag_list = set(tag_list)
        tag_list_of_dict = []
        for item in tag_list:
            ratio = int(difflib.SequenceMatcher(None, str(input_tag), str(item)).ratio() * 100)
            if ratio > 50:
                for i in list_of_notes:
                    if item in i['tag']:
                        tag_list_of_dict.append({ratio: i['note']})
        sort_list = []
        for tag in tag_list_of_dict:
            for key, value in tag.items():
                sort_list.append({"ratio": key, "tag": value})
        new_list = sorted(sort_list, key=itemgetter('ratio'), reverse=True)
        return ([d["tag"] for d in new_list]) if len(new_list) > 0 else f"No such tags in notes"

    def note_serialize(self, list_of_notes):
        with open(self.filename, 'w') as file:
            json.dump(list_of_notes, file, sort_keys=True, indent=4)

    def deserialize(self):
        with open(self.filename, 'r') as file:
            return json.load(file, sort_keys=True, indent=4)