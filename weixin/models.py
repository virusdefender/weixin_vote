# coding=utf-8
import time
import hashlib
from django.db import models


def get_token():
    return hashlib.md5(str(time.time())).hexdigest()[:15]


class WeixinConfig(models.Model):
    name = models.CharField(u"公众号名称", max_length=30)
    weixin_id = models.CharField(u"公众号id", max_length=30)
    token = models.CharField("token", default=get_token, max_length=30)
    forward = models.BooleanField(u"是否开启转发", help_text=u"如果开启转发，非投票编号的消息都会转发出去", default=False)
    forward_url = models.CharField(u"第三方平台的url", max_length=200, blank=True, null=True)
    forward_token = models.CharField(u"第三方平台token", max_length=100, blank=True, null=True)

    class Meta:
        db_table = "weixin_config"
        verbose_name = u"平台设置"
        verbose_name_plural = u"平台设置"

    def __unicode__(self):
        return self.name