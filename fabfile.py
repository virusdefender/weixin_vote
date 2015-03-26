# coding=utf-8
from fabric.api import local, abort, settings, env, cd, run
from fabric.colors import *
from fabric.contrib.console import confirm

env.hosts = ["root@**.com"]
env.password = "***"


def deploy():
    with cd("/mnt/source/weixin_vote"):
        print green("将在远程仓库下载代码")
        run("git pull origin master")
        print red("重建数据库？")
        r = raw_input()
        if r == "yes":
            run("sh restore.sh")
        # del pyc
        # run('find /mnt/source/tm/ -name "*.pyc" | xargs rm -rf')

        print green("代码部署成功！！！")
