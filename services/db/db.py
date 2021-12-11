from mongoengine import DynamicDocument, DateTimeField, ListField


class Ticker(DynamicDocument):
    time = DateTimeField()
    info = ListField()
    volume = ListField()
