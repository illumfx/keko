from tortoise import fields
from tortoise.models import Model


class Mutes(Model):
    id = fields.IntField(pk=True)
    guild = fields.BigIntField()
    moderator = fields.BigIntField()
    receiver = fields.BigIntField()
    reason = fields.TextField()
    issued_at = fields.DatetimeField(auto_now=True)
    ends_at = fields.DatetimeField()
