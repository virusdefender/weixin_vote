# coding=utf-8
import datetime
from pytz import timezone

import xadmin
from xadmin import views

from .models import VoterInfo, VoteLog, VoteActivity


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": u"首页", "content": "<h3>投票管理系统<h3>"},
        ],
        [
            {"type": "qbutton", "title": u"快速查看", "btns": [{'model': VoterInfo}, {'model':VoteLog}]}
        ]
    ]
xadmin.site.register(views.website.IndexView, MainDashboard)


class BaseSetting(object):
    enable_themes = False
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    global_search_models = [VoteLog, VoterInfo]
    global_models_icon = {
        VoteLog: 'fa fa-laptop', VoterInfo: 'fa fa-cloud'
    }
    menu_style = 'accordion'
xadmin.site.register(views.CommAdminView, GlobalSetting)


class VoteActivityAdmin(object):
    def result_link(self, instance):
        return '<a href="/signup/%s/">报名</a>&nbsp;<a href="/show/%s/">排名</a>&nbsp;' \
               '<a href="/chart/%s/">图表</a>&nbsp;<a href="/admin/vote/votelog/?_p_vote_activity__id__exact=%s">投票记录</a>' % \
               (str(instance.id), str(instance.id), str(instance.id), str(instance.id))
    result_link.short_description = "结果"
    result_link.allow_tags = True
    result_link.is_column = True

    def status(self, instance):
        now = timezone("Asia/Shanghai").localize(datetime.datetime.now())
        print now
        if instance.signup_start_time > now:
            return u"报名未开始"
        if instance.signup_start_time <= now and instance.vote_start_time > now:
            return u"正在报名"
        if instance.vote_start_time <= now and instance.vote_end_time > now:
            return u"正在投票"
        return u"活动结束"

    status.short_description = u"状态"
    status.is_column = True

    search_fields = ["name"]
    list_display = ["id", "name", "signup_start_time", "vote_start_time", "vote_end_time", "status", "result_link"]
    exclude = ["vote_id_start"]


class VoterInfoAdmin(object):
    def my_log(self, instance):
        return "<a href='/admin/vote/votelog/?_p_voter_info__id__exact=%s'>投票记录</a>&nbsp;<a href='/chart/%s/?voter_id=%s'>图表</a>" % (str(instance.id), str(instance.vote_activity.id), str(instance.id))
    my_log.short_description = u"投票记录"
    my_log.allow_tags = True
    my_log.is_column = True

    list_display = ["id", "vote_activity", "name", "phone", "vote_number", "vote_id", "my_log"]
    list_filter = ["vote_activity"]
    search_fields = ["name", "phone", "address"]


class VoteLogAdmin(object):
    list_filter = ["vote_activity", "voter_info"]
    list_display = ["id", "open_id", "vote_activity", "voter_info", "create_time"]
    search_fields = ["open_id"]


xadmin.site.register(VoterInfo, VoterInfoAdmin)
xadmin.site.register(VoteLog, VoteLogAdmin)
xadmin.site.register(VoteActivity, VoteActivityAdmin)
