from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    banner_image = models.ImageField(upload_to='courses/', blank=True, null=True)
    banner_image_url = models.URLField(blank=True, null=True, help_text="Alternative URL for course banner image")
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2)
    instructor_name = models.CharField(max_length=150)
    duration = models.CharField(max_length=100, help_text="e.g. 6 Weeks")
    course_overview = models.TextField(blank=True, help_text="Detailed overview of the course content")
    last_remarks = models.TextField(blank=True, help_text="Final remarks or review comments")
    
    # UI Metadata Fields
    category = models.CharField(max_length=150, default='LEADERSHIP AND PERSONAL DEVELOPMENT')
    level = models.CharField(max_length=100, default='Advanced')
    modules_count = models.IntegerField(default=6)
    students_count = models.IntegerField(default=5)

    def __str__(self):
        return self.title

    @property
    def discount_percentage(self):
        if self.original_price > 0:
            discount = ((self.original_price - self.payable_amount) / self.original_price) * 100
            return int(round(discount))
        return 0
