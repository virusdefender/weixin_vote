# coding=utf-8
import time
from .models import WeixinConfig


class TextMessage(object):
    def __init__(self, open_id, weixin_config, text):
        weixin_id = WeixinConfig.objects.all()[0].weixin_id
        self.xml = u"""
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>
                    """ % (open_id, weixin_config.weixin_id, str(int(time.time())), text)

    @property
    def data(self):
        return self.xml


class NewsMessage(object):
    def __init__(self, open_id, weixin_config, news):
        news_num = len(news)

        self.xml = u"""
                    <xml>
                    <ToUserName><![CDATA[{0}]]></ToUserName>
                    <FromUserName><![CDATA[{1}]]></FromUserName>
                    <CreateTime>{2}</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>{3}</ArticleCount>
                    <Articles>
                    """.format(open_id, weixin_config.weixin_id, str(int(time.time())), news_num)

        for num in range(0, news_num):
            item_xml = u"""
                        <item>
                        <Title><![CDATA[{0}]]></Title>
                        <Description><![CDATA[{1}]]></Description>
                        <PicUrl><![CDATA[{2}]]></PicUrl>
                        <Url><![CDATA[{3}]]></Url>
                        </item>
                        """.format(news[num]["title"], news[num]["description"], news[num]["pic_url"], news[num]["url"])
            self.xml += item_xml

        self.xml += u"""
                     </Articles>
                     </xml>
                     """

    @property
    def data(self):
        return self.xml