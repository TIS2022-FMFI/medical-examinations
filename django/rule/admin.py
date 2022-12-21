from django.contrib import admin
from .models import Rule, HiddenRule # , RuleType, Locality

admin.site.register(Rule)
admin.site.register(HiddenRule)
# admin.site.register(RuleType)
# admin.site.register(Locality)
