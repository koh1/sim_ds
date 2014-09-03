from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sim_dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'result_manager.views.index'),
    url(r'^/main/get_topology_data/(?P<db_name>\w+)/(?P<coll_name>/w+)/$', 'main.views.get_topology_data'),
    url(r'^nwk_vis/$', 'nwk_vis.views.index'),
    url(r'^nwk_vis/get_nwk_traffic/(?P<db_name>\w+)/(?P<coll_name>\w+)/(?P<time>\d+)/$', 'nwk_vis.views.get_nwk_traffic'),
    url(r'^search_results/$', 'result_manager.views.search_results'),
    url(r'^analyzer/(?P<sim_id>\w+)/$', 'analyzer.views.index'),
    url(r'^analyzer/analyze/(?P<sim_id>\w+)/$', 'analyzer.views.analyze_index'),
    url(r'^get_nwk_chart_data/$', 'analyzer.views.get_nwk_chart_data'),
    url(r'^analyzer/network/(?P<sim_id>\w+)/$', 'analyzer.views.nwk_index'),
    url(r'^analyzer/message/(?P<sim_id>\w+)/$', 'analyzer.views.msg_index'),
    url(r'^analyzer/node/(?P<sim_id>\w+)/$', 'analyzer.views.nd_index'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
