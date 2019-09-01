# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^test/test/', views.test, name='test_test'),
    url(r'^index/', views.index, name='bank_index'),
    url(r'^questionnaire/import/', views.questionnaire_import, name='questionnaire_import'),
    url(r'^questionnaire/tpl/', views.questionnaire_tpl, name='questionnaire_tpl'),    
      
    url(r'^inquire/into/', views.inquire_into, name='inquire_into'),
    url(r'^overall/evaluation/', views.overall_evaluation, name='overall_evaluation'),
    url(r'^all/investigation/', views.all_investigation, name='all_investigation'),    
    url(r'^all/investigationRanking/', views.all_investigationRanking, name='all_investigationRanking'),
    url(r'^user/questionnaire/(.+)', views.user_questionnaire, name='user_questionnaire'),                
    url(r'^help/(.+)', views.help, name='help'),
        
    url(r'^test/questionnaire/', views.test_questionnaire, name='test_questionnaire'),
    url(r'^analysis/report/', views.analysis_report, name='analysis_report'),
    url(r'^down/analysisReport/', views.down_analysisReport, name='down_analysis_report'),

    url(r'^create/excel/', views.create_excel, name='create_excel'),       
    url(r'^contactus/', views.contactus, name='contactus'),   
    url(r'^setting/value/', views.setting_value, name='setting_value'),
    url(r'^setting/list/', views.setting_list, name='setting_list'), 
    url(r'^upload/', views.upload, name='upload_word_tpl'),     
    url(r'^download/', views.download, name='download_word_tpl'),
]
