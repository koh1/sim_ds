from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sim_dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ## my applications
    url(r'^$', 'result_manager.views.index'),
    url(r'^exec/$', 'result_manager.views.exec_index'),
    url(r'^view/get_nwk_traffic/(?P<pkid>\w+)/(?P<nwk_name>\w+)/$', 'result_manager.views.get_nwk_traffic'),
    url(r'^view/$', 'result_manager.views.view_index'),

    url(r'^exec_process$', 'result_manager.views.exec_process'),
    url(r'^view_detail_config/(?P<pkid>\w+)/$', 'result_manager.views.view_detail_config'),
    url(r'^delete_sim_result/(?P<pkid>\w+)/$', 'result_manager.views.delete_sim_result'),
    url(r'^search_results/$', 'result_manager.views.search_results'),
#    url(r'^/main/get_topology_data/(?P<db_name>\w+)/(?P<coll_name>/w+)/$', 'main.views.get_topology_data'),
#    url(r'^analyzer/$', 'analyzer.views.index'),
#    url(r'^analyzer/analyze/(?P<sim_id>\w+)/$', 'analyzer.views.analyze_index'),
#    url(r'^analyzer/get_df_sample/$', 'analyzer.views.get_df_sample'),
#    url(r'^get_nwk_chart_data/$', 'analyzer.views.get_nwk_chart_data'),
#    url(r'^result_viewer/(?P<sim_id>\w+)/$', 'result_viewer.views.index'),
#    url(r'^result_viewer/network/(?P<sim_id>\w+)/$', 'result_viewer.views.nwk_index'),
#    url(r'^result_viewer/message/(?P<sim_id>\w+)/$', 'result_viewer.views.msg_index'),
#    url(r'^result_viewer/node/(?P<sim_id>\w+)/$', 'result_viewer.views.nd_index'),
#    url(r'^series_manager/$', 'series_manager.views.index'),
#    url(r'^series_manager/make_df_from_mdb/$', 'series_manager.views.make_df_from_mdb'),
#    url(r'^series_manager/get_series_from_dfd/$', 'series_manager.views.get_series_from_dfd'),

                       


    ## admin
    url(r'^admin/', include(admin.site.urls)),

    ## authentication and authorization
    
    url(r'^account/login/$', 'django.contrib.auth.views.login', {'template_name':'account/login.html'}),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^account/changepw/$', 'django.contrib.auth.views.password_change'),
    url(r'^account/changepw/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^account/resetpw/$', 'django.contrib.auth.views.password_reset'),
    url(r'^account/resetpw/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^account/resetpw/confirm/(?P<uidb36>.+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^account/resetpw/complete/$', 'django.contrib.auth.views.password_reset_complete'),
)

urlpatterns += staticfiles_urlpatterns()
