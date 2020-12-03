from tortoise import fields
from tortoise.models import Model

class Tournament(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

