# coding=utf-8
import datetime
from pytz import timezone

import xadmin
from xadmin import views

from weixin_vote.config import domain
from .models import WeixinConfig


class WeixinConfigAdmin(object):
    def url(self, instance):
        return "http://" + domain + "/%s/" % (str(instance.id), )
    url.short_description = "url"
    url.allow_tags = True
    url.is_column = True

    list_display = ["name", "url", "token"]
    save_as = True


xadmin.site.register(WeixinConfig, WeixinConfigAdmin)