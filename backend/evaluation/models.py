from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Mentor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    sub1 = models.IntegerField(default=0)
    sub2 = models.IntegerField(default=0)
    sub3 = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    locked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.total = self.sub1 + self.sub2 + self.sub3
        super(Evaluation, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} evaluated by {self.mentor.name}"
