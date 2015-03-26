# coding=utf-8
import datetime
from django.db import models

from weixin.models import WeixinConfig


class VoteActivity(models.Model):
    weixin_config = models.ForeignKey(WeixinConfig, verbose_name=u"微信账号")
    name = models.CharField(u"活动名称", max_length=100)
    content = models.TextField(u"说明", blank=True, null=True)
    vote_id_prefix = models.CharField(u"选手编号前缀", max_length=10, blank=True, null=True)
    vote_id_start= models.IntegerField(default=1)
    signup_start_time = models.DateTimeField(u"报名开始时间")
    vote_start_time = models.DateTimeField(u"投票开始时间", help_text=u"也就是报名结束时间")
    vote_end_time = models.DateTimeField(u"投票结束时间")
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    class Meta:
        db_table = "VoteActivity"
        verbose_name = u"投票活动"
        verbose_name_plural = u"投票活动"

    def __unicode__(self):
        return self.name


class VoterInfo(models.Model):
    vote_activity = models.ForeignKey(VoteActivity, verbose_name=u"投票活动")
    name = models.CharField(u"姓名", max_length=50, blank=True, null=True)
    phone = models.CharField(u"手机", max_length=11, blank=True, null=True)
    pic = models.CharField(u"图片地址", max_length=300, blank=True, null=True)
    address = models.CharField(u"地址", max_length=200, blank=True, null=True)

    vote_number = models.IntegerField(u"票数", default=0)

    vote_id = models.CharField(u"投票序号", help_text=u"正在进行的活动中不要有重复的",  max_length=10, blank=True, null=True)
    is_valid = models.BooleanField(u"是否有效", help_text=u"反选代表删除，不能投票", default=True)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True)

    class Meta:
        db_table = "voter_info"
        verbose_name = u"选手信息"
        verbose_name_plural = u"选手信息"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            vote_id = str(self.vote_activity.vote_id_start)

            if self.vote_activity.vote_id_start <= 99:
                vote_id = "0" * (2 - len(vote_id)) + vote_id
            elif self.vote_activity.vote_id_start > 99 and self.activity.vote_id_start <= 9999:
                vote_id = "0" * (4 - len(vote_id)) + vote_id
            else:
                vote_id = "0" * (8 - len(vote_id)) + vote_id

            if self.vote_activity.vote_id_prefix:
                vote_id = self.vote_activity.vote_id_prefix + vote_id
            self.vote_id = vote_id
            self.vote_activity.vote_id_start += 1
            self.vote_activity.save()
        super(VoterInfo, self).save(*args, **kwargs)


class VoteLog(models.Model):
    vote_activity = models.ForeignKey(VoteActivity, verbose_name=u"投票活动")
    create_time = models.DateTimeField(u"创建时间", default=datetime.datetime.now)
    open_id = models.CharField(u"openid", max_length=100)
    voter_info = models.ForeignKey(VoterInfo, verbose_name=u"选手信息")

    class Meta:
        db_table = "vote_log"
        verbose_name = u"投票记录"
        verbose_name_plural = u"投票记录"

    def __unicode__(self):
        return self.open_id
