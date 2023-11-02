from django.contrib import admin

# add include to the path
from django.urls import path, include

# import views from todo
from evaluation import views# Import the view here


# import routers from the REST framework
# it is necessary for routing
from rest_framework import routers

# create a router object
router = routers.DefaultRouter()

# register the router
router.register(r'student',views.StudentListView, 'student')
router.register(r'mentor', views.MentorListView, 'mentor')
router.register(r'evaluation', views.EvaluationListView, 'evaluation')
router.register(r'unassigned', views.UnassignedStudentListView, 'unassigned-students'),

urlpatterns = [
	path('admin/', admin.site.urls),

	# add another path to the url patterns
	# when you visit the localhost:8000/api
	# you should be routed to the django Rest framework
    path('api/', include(router.urls)),
    path('api/select-students/', views.StudentDataAPIView.as_view(), name='select-students'),
    path('api/add-student/', views.AddStudentEvaluationAPIView.as_view(), name='add-student'),
	path('api/remove-student/', views.RemoveStudentAPIView.as_view(), name='remove-student'),
    path('api/save-marks/', views.SaveStudentMarksAPIView.as_view(), name='save-marks'),
    path('api/submit-marks/', views.SubmitStudentMarksAPIView.as_view(), name='submit-marks'),
]
