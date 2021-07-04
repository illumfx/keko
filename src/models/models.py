from tortoise.models import Model
from tortoise import fields

from src.fields import BigIntArrayField, TextArrayField

class Prefixes(Model):
    guild_id = fields.BigIntField(pk=True)
    prefix = fields.TextField()
    
class SelfAssignableRoles(Model):
    guild_id = fields.BigIntField(pk=True)
    roles = BigIntArrayField()