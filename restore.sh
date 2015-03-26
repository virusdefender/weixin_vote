#!/bin/bash
rm db.sqlite3
echo "no\n" | python manage.py syncdb
echo "from weixin_vote.fake_data import *" | python manage.py shell

echo "成功创建数据"