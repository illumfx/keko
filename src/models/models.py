from .fields import BigIntArrayField, TextArrayField
from tortoise import fields
from tortoise.models import Model
    
class Prefixes(Model):
    guild_id = fields.BigIntField(pk=True, unique=True)
    prefix = fields.TextField()
    
class SelfAssignableRoles(Model):
    guild_id = fields.BigIntField(pk=True, unique=True)
    roles = BigIntArrayField()
    
class Colors(Model):
    guild_id = fields.BigIntField(pk=True, unique=True)
    neutral = fields.IntField(null=True)
    error = fields.IntField(null=True)
    success = fields.IntField(null=True)
    
