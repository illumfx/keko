from src.fields import BigIntArrayField, TextArrayField
from tortoise import fields
from tortoise.models import Model


class Prefixes(Model):
    guild_id = fields.BigIntField(pk=True)
    prefix = fields.TextField()


class SelfAssignableRoles(Model):
    guild_id = fields.BigIntField(pk=True)
    roles = BigIntArrayField()
