from django.shortcuts import render

# import view sets from the REST framework
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# import the TodoSerializer from the serializer file
from .serializers import StudentSerializer,MentorSerializer,EvaluationSerializer

# import the Todo model from the models file
from .models import Mentor,Student,Evaluation



class StudentListView(viewsets.ModelViewSet):
	serializer_class = StudentSerializer
	queryset = Student.objects.all()
	
class MentorListView(viewsets.ModelViewSet):
	serializer_class = MentorSerializer
	queryset = Mentor.objects.all()
	
class EvaluationListView(viewsets.ModelViewSet):
	serializer_class = EvaluationSerializer
	queryset = Evaluation.objects.all()

class UnassignedStudentListView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        assigned_students_ids = Evaluation.objects.all().values_list('student_id', flat=True)
        # print(assigned_students_ids)
        queryset = Student.objects.exclude(id__in=assigned_students_ids)
        return queryset

class StudentDataAPIView(APIView):
    # your implementation
    def post(self, request, *args, **kwargs):
        student_ids = request.data.get('student_ids', [])
        students = Evaluation.objects.filter(student__in=student_ids)
        serializer = EvaluationSerializer(students, many=True)
        return Response(serializer.data)
    
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Student, Mentor, Evaluation
# from .serializers import EvaluationSerializer

class AddStudentEvaluationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        mentor_id = request.data.get('mentor_id')
        sub1 = request.data.get('sub1', 0)
        sub2 = request.data.get('sub2', 0)
        sub3 = request.data.get('sub3', 0)

        # Check if student and mentor exist
        try:
            student = Student.objects.get(id=student_id)
            mentor = Mentor.objects.get(id=mentor_id)
        except (Student.DoesNotExist, Mentor.DoesNotExist):
            return Response({'error': 'Invalid student or mentor ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the mentor already has 4 students assigned
        current_students_count = Evaluation.objects.filter(mentor=mentor).count()
        if current_students_count >= 4:
            return Response({'alert': 'Mentor already has 4 students assigned. Cannot add more.'}, status=status.HTTP_200_OK)

        # Check if an evaluation already exists for this student-mentor pair
        if Evaluation.objects.filter(student=student, mentor=mentor).exists():
            return Response({'error': 'Student already assigned to the mentor.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create new Evaluation entry
        evaluation = Evaluation.objects.create(student=student, mentor=mentor, sub1=sub1, sub2=sub2, sub3=sub3)
        serializer = EvaluationSerializer(evaluation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class RemoveStudentAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         student_id = request.data.get('student_id')
#         mentor_id = request.data.get('mentor_id')

#         # Attempt to find and delete the Evaluation entry
#         try:
#             evaluation = Evaluation.objects.get(student_id=student_id, mentor_id=mentor_id)
#             evaluation.delete()
#             return Response({'message': 'Student removed successfully'}, status=status.HTTP_200_OK)
#         except Evaluation.DoesNotExist:
#             return Response({'error': 'Evaluation entry not found'}, status=status.HTTP_500_NOT_FOUND)
        
#          # Check the number of students assigned to the mentor after deletion
#         remaining_students_count = Evaluation.objects.filter(mentor_id=mentor_id).count()

#         if remaining_students_count < 3:
#             return Response({'message': 'Student removed successfully', 'alert': 'Number of students assigned to this mentor is less than 3!'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Student removed successfully'}, status=status.HTTP_200_OK)

class RemoveStudentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        mentor_id = request.data.get('mentor_id')

        # Check the current number of students assigned to the mentor
        current_students_count = Evaluation.objects.filter(mentor_id=mentor_id).count()

        # If deleting this student will drop the count to 3, send an alert
        if current_students_count == 3:
            return Response({'alert': 'Removing this student will result in the mentor having less than 3 students. Proceed with caution!'}, status=status.HTTP_200_OK)

        # Attempt to find and delete the Evaluation entry
        try:
            evaluation = Evaluation.objects.get(student_id=student_id, mentor_id=mentor_id)
            evaluation.delete()
            return Response({'message': 'Student removed successfully'}, status=status.HTTP_200_OK)
        except Evaluation.DoesNotExist:
            return Response({'error': 'Evaluation entry not found'}, status=status.HTTP_404_NOT_FOUND)


class SaveStudentMarksAPIView(APIView):
    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        mentor_id = request.data.get('mentor_id')
        marks_sub1 = request.data.get('sub1', 0)
        marks_sub2 = request.data.get('sub2', 0)
        marks_sub3 = request.data.get('sub3', 0)

        # Check if student exists
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid student ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Evaluation entry for given student_id exists
        try:
            evaluation = Evaluation.objects.get(student=student)
        except Evaluation.DoesNotExist:
            return Response({'error': 'No evaluation entry found for this student.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the marks
        evaluation.sub1 = marks_sub1
        evaluation.sub2 = marks_sub2
        evaluation.sub3 = marks_sub3
        evaluation.save()

        serializer = EvaluationSerializer(evaluation)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubmitStudentMarksAPIView(APIView):
    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        mentor_id = request.data.get('mentor_id')
        marks_sub1 = request.data.get('sub1', 0)
        marks_sub2 = request.data.get('sub2', 0)
        marks_sub3 = request.data.get('sub3', 0)

        # Check if student exists
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid student ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Evaluation entry for given student_id exists
        try:
            evaluation = Evaluation.objects.get(student=student)
        except Evaluation.DoesNotExist:
            return Response({'error': 'No evaluation entry found for this student.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the marks and set the locked field to true
        evaluation.sub1 = marks_sub1
        evaluation.sub2 = marks_sub2
        evaluation.sub3 = marks_sub3
        evaluation.locked = True
        evaluation.save()

        serializer = EvaluationSerializer(evaluation)
        return Response(serializer.data, status=status.HTTP_200_OK)