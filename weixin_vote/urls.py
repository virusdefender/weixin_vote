from django.conf.urls import patterns, include, url

import xadmin
xadmin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weixin_vote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'admin/', include(xadmin.site.urls)),

    url(r"^(?P<weixin_id>\d+)/$", "weixin.views.weixin_main"),

    url(r"^signup/(?P<vote_activity_id>\d+)/$", "vote.views.signup_page"),

    url(r"^show/(?P<vote_activity_id>\d+)/$", "vote.views.show_page"),

    url(r"^upload/$", "vote.views.upload"),

    url(r"^chart/(?P<activity_id>\d+)/", "vote.views.activity_chart"),
)
