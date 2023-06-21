from django.urls import path, re_path
from app import views
from buscamascota import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('pets/', views.PetAdoptionListAPIView.as_view(), name='pet-adoption-list'),
    path('', views.index, name='index'),
    path('colaborar/', views.colaborate, name='colaborar'),
    path('map/<int:page>', views.map, name='map'),
    path('map/', views.map, name='map'),
    path('publicar/', views.publish, name='publicar'),
    path('terminos/', views.terms, name='terminos'),
    path('licencia/', views.license, name='licencia'),
    path('exito/<int:report_id>', views.success, name='success'),
    re_path(r'^reporte/(?P<report_id>[0-9]+)$', views.report, name='report'),
    path('lista_reportes', views.report_list, name="lista_reportes"),
    re_path(r'^adopcion/(?P<adopt_id>[0-9]+)$', views.adopt, name='adopt'),
    path('detalle_adopcion', views.PetAdoptionModel, name="detalle_adopcion"),  #Url para guardar una adopción
path('reportesget/<int:pk>/', views.ReportGetAPIView.as_view(), name='report-get'),
    path('adopciones-publicar/', views.publicar_adopcion, name="adopciones-publicar"),
    path('reportes-publicar/', views.publicar_reporte, name="reportes-publicar"),

    #API
    path('api/reportes/', views.ReportListAPIView.as_view(), name='report_list_json'),
    re_path(r'^api/reporte/(?P<report_id>[0-9]+)$', views.ReportDetail, name='report_detail_json'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
