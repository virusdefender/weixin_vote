# coding=utf-8
import datetime
import json

from pytz import utc
from pytz import timezone

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import VoterInfo, VoteActivity, VoteLog
from .upload_file import FileOperation


def signup_page(request, vote_activity_id):

    try:
        activity = VoteActivity.objects.get(pk=vote_activity_id)
    except VoteActivity.DoesNotExist:
        return render(request, "vote/error.html", {"error": u"活动不存在"})

    now = timezone("Asia/Shanghai").localize(datetime.datetime.now())
    if now < activity.signup_start_time.replace(tzinfo=utc):
        return render(request, "vote/error.html", {"error": u"活动报名还没有开始"})
    if now > activity.vote_start_time.replace(tzinfo=utc):
        return render(request, "vote/error.html", {"error": u"活动已经开始投票，不能报名"})

    if request.method == "GET":
        return render(request, "vote/signup.html", {"activity": activity})

    else:
        data = request.body
        try:
            data = json.loads(data)
        except Exception:
            return HttpResponse(json.dumps({"status": "error", "content": "Error"}), status=400)

        vote_info = VoterInfo.objects.create(vote_activity=activity, name=data["name"], phone=data["phone"],
                                             address=data["address"], pic=data["image"])

        return HttpResponse(json.dumps({"status": "success", "vote_id": vote_info.vote_id, "activity_id": activity.id}))


def show_page(request, vote_activity_id):
    try:
        activity = VoteActivity.objects.get(pk=vote_activity_id)
    except VoteActivity.DoesNotExist:
        return render(request, "vote/error.html", {"error": u"活动不存在"})

    info = VoterInfo.objects.filter(vote_activity=activity).order_by("-vote_number")
    return render(request, "vote/show.html", {"vote_info": info, "activity": activity})


@csrf_exempt
def upload(request):
    f = request.FILES["image"]
    fp = FileOperation(f)
    fp.save()
    return HttpResponse(fp.get_file_url())


def activity_chart(request, activity_id):
    try:
        activity = VoteActivity.objects.get(pk=activity_id)
    except VoteActivity.DoesNotExist:
        return render(request, "vote/error.html", {"error": u"活动不存在"})

    voter_id = request.GET.get("voter_id", None)
    if voter_id and voter_id != "None":
        try:
            voter_info = VoterInfo.objects.get(vote_activity=activity, pk=voter_id)
        except VoterInfo.DoesNotExist:
            return render(request, "vote/error.html", {"error": u"选手不存在"})
    else:
        voter_info = None

    data_format = request.GET.get("format", None)
    if not data_format:
        return render(request, "vote/activity_chart.html", {"activity": activity, "voter_info": voter_info})
    else:
        if not voter_info:
            logs = VoteLog.objects.filter(vote_activity=activity).order_by("create_time")
        else:
            logs = VoteLog.objects.filter(voter_info=voter_info, vote_activity=activity).order_by("create_time")

        start_time = request.GET.get("start_time", None)
        end_time = request.GET.get("end_time", None)
        limit = request.GET.get("limit", None)

        time_list = []
        vote_list = []

        try:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            limit = int(limit)
        except Exception:
            return HttpResponse(json.dumps({"time_list": time_list, "vote_list": vote_list}))

        if logs.exists():

            time_ptr = start_time

            while True:
                if time_ptr <= end_time:
                    time_list.append((time_ptr).strftime("%H:%M"))
                    vote_list.append(VoteLog.objects.filter(vote_activity=activity, create_time__lt=time_ptr).count())
                    time_ptr += datetime.timedelta(minutes=limit)
                else:
                    time_list.append((time_ptr).strftime("%H:%M"))
                    vote_list.append(VoteLog.objects.filter(vote_activity=activity, create_time__lt=time_ptr).count())
                    break

        return HttpResponse(json.dumps({"time_list": time_list, "vote_list": vote_list}))