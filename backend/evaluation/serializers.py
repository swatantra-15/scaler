from rest_framework import serializers
from .models import Student, Mentor, Evaluation

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']

class MentorSerializer(serializers.ModelSerializer):
    assigned_students = serializers.SerializerMethodField()

    class Meta:
        model = Mentor
        fields = ['id', 'name', 'assigned_students']  

    def get_assigned_students(self, mentor):
        evaluations = Evaluation.objects.filter(mentor=mentor)
        student_ids = evaluations.values_list('student_id', flat=True)
        return list(student_ids)

class EvaluationSerializer(serializers.ModelSerializer):
    student = serializers.IntegerField(source='student.id', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    class Meta:
        model = Evaluation
        fields = ['id', 'student','student_name', 'mentor', 'sub1', 'sub2', 'sub3', 'total', 'locked']
        read_only_fields = ['total', 'locked']  # Prevent direct modification
