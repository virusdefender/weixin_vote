# coding=utf-8
import time
import random
import hashlib
import datetime

import requests
from pytz import timezone
from lxml import etree

from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import MultipleObjectsReturned

from weixin_vote.config import domain
from vote.models import VoterInfo, VoteLog
from .message import TextMessage, NewsMessage
from .models import WeixinConfig


@csrf_exempt
def weixin_main(request, weixin_id):
    """所有的消息都会先进入这个函数进行处理，函数包含两个功能，如果请求时get，说明是微信接入验证，如果是post就是微信正常的收发消息。
    """
    try:
        config = WeixinConfig.objects.get(pk=weixin_id)
    except WeixinConfig.DoesNotExist:
        return HttpResponse("Weixin does not exist")

    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)


        tmp_list = [config.token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("weixin  index")
    else:
        return HttpResponse(reply(request, config))


def forward_message(weixin_config, message):
    timestamp = str(int(time.time()))

    # I don't know how Weixin generate the 9-digit nonce, so I turn to random.
    nonce = hashlib.md5(str(time.time())).hexdigest()[:9]

    l = [timestamp, nonce, weixin_config.forward_token]
    l.sort()
    signature = hashlib.sha1("".join(l)).hexdigest()

    url = weixin_config.forward_url

    if "?" in url:
        url += "&signature=%s&timestamp=%s&nonce=%s" % (signature, timestamp, nonce)
    else:
        url += "?signature=%s&timestamp=%s&nonce=%s" % (signature, timestamp, nonce)

    print "Forward to", url

    try:
        r = requests.post(url, data=message, headers={"Content-Type": "text/xml"})
    except Exception:
        return "Request error"
    return r.content


def reply(request, weixin_config):
    xml_str = smart_str(request.body)
    request_xml = etree.fromstring(xml_str)

    msg_type = request_xml.find("MsgType").text
    open_id = request_xml.find("FromUserName").text

    if msg_type == "text":
        content = request_xml.find("Content").text

        now = timezone("Asia/Shanghai").localize(datetime.datetime.now())

        try:
            voter_info = VoterInfo.objects.get(vote_activity__weixin_config=weixin_config,
                                               vote_id=content,
                                               vote_activity__vote_start_time__lte=now,
                                               vote_activity__vote_end_time__gte=now)
        except VoterInfo.DoesNotExist:
            if weixin_config.forward:
                return HttpResponse(forward_message(weixin_config, request.body))
            else:
                return TextMessage(open_id, weixin_config, u"选手id不存在").data

        except MultipleObjectsReturned:
            return TextMessage(open_id, weixin_config, u"存在多个重复的投票id，请联系管理员")

        try:
            VoteLog.objects.get(voter_info=voter_info, open_id=open_id, vote_activity=voter_info.vote_activity)
            # return TextMessage(open_id, u"您已经给该选手投过票了").data
        except VoteLog.DoesNotExist:
            VoteLog.objects.create(open_id=open_id, voter_info=voter_info, vote_activity=voter_info.vote_activity)

        voter_info.vote_number += 1
        voter_info.save()

        rank = VoterInfo.objects.filter(vote_activity__weixin_config=weixin_config, vote_number__gt=voter_info.vote_number).count() + 1

        m = ""
        if rank > 1:
            pre = VoterInfo.objects.all()[rank - 2]
            m = u"上一名" + str(pre.vote_number) + u"票"

        return NewsMessage(open_id, weixin_config,
                           [{"title": u"您已经成功投票",
                             "description": u"票数" + str(voter_info.vote_number) + u";排名" + str(rank) + ";" + m,
                             "pic_url": voter_info.pic,
                             "url": "http://" + domain + "/show/" + str(voter_info.vote_activity.id)}]).data
    else:
        if weixin_config.forward:
            return forward_message(weixin_config, request.body)
        else:
            return TextMessage(open_id, weixin_config, u"不支持的消息类型").data