# coding=utf-8
import datetime

from vote.models import VoterInfo, VoteActivity
from weixin.models import WeixinConfig

from django.contrib.auth.models import User

root = User.objects.create(username="root")
root.set_password("root")
root.is_superuser = True
root.is_staff = True
root.save()
weixin_config = WeixinConfig.objects.create(name="account1", weixin_id='gh_18e1e6751caf', token="virusdefender")

activity = VoteActivity.objects.create(weixin_config=weixin_config, name="test activity",
                                       signup_start_time=datetime.datetime.now() - datetime.timedelta(days=1),
                                       vote_start_time=datetime.datetime.now() + datetime.timedelta(days=1),
                                       vote_end_time=datetime.datetime.now() + datetime.timedelta(days=100))

VoterInfo.objects.create(vote_activity=activity,
                         name="1",
                         pic="http://vote1.b0.upaiyun.com/1423551952e7cd7b899e510fb36c1ec2d7da33c895d1430c6e.jpg")


VoterInfo.objects.create(vote_activity=activity,
                         name="2",
                         pic="http://vote1.b0.upaiyun.com/1423551952e7cd7b899e510fb36c1ec2d7da33c895d1430c6e.jpg")