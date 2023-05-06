from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.core.exceptions import ValidationError


# Create your models here.
from datetime import datetime, timedelta

def format_timeinterval(timeinterval):
    start_hour, end_hour = timeinterval.split('-')
    start = datetime.now().replace(hour=int(start_hour), minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=int(end_hour) - int(start_hour))
    return f"{start.isoformat()}/{'-04:00'.join(['', end.isoformat()])}"


class Days(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class Nurses(models.Model):
    NURSE_ID_CHOICES = [(i, str(i)) for i in range(1, 18)]
    SHIFT_TYPE_CHOICES = [("day", "Day"), ("night", "Night")]

    nurse_id = models.IntegerField(choices=NURSE_ID_CHOICES, unique=True)
    available_days = models.ManyToManyField(Days)
    shift_type = models.CharField(max_length=200, choices=SHIFT_TYPE_CHOICES, default="day")
    assignments = models.IntegerField(default=0)
    hours_available = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def clean(self):
        # Check if the nurse has already been assigned six times
        if self.assignments >= 6:
            raise ValidationError('Nurse cannot be assigned more than six times.')
        
    def can_work(self, shift_type):
        if shift_type == "day" and self.shift_type == "day":
            return True
        elif shift_type == "night" and self.shift_type == "night":
            return True
        else:
            return False
        
    def is_available(self, timeinterval):
        # Parse the time interval into start and end times
        start, end = timeinterval.split('-')
        start = datetime.strptime(start.strip(), '%H')
        end = datetime.strptime(end.strip(), '%H')

        # Convert the start and end times to datetimes for the current day
        now = datetime.now()
        start = now.replace(hour=start.hour, minute=0, second=0, microsecond=0)
        end = now.replace(hour=end.hour, minute=0, second=0, microsecond=0)

        # Check if the nurse is available during the time interval
        return self.hours_available >= (end - start).total_seconds() / 3600

    def __str__(self):
        return f"{self.nurse_id}"    


class Availability(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ]
    nurse = models.ForeignKey(Nurses, on_delete=models.CASCADE)
    day = models.ForeignKey(Days, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nurse}: {self.get_day_display()}"
    
class Shifts(models.Model):
    CONSTRAINT_CHOICES = [("soft", "Soft"), ("hard", "Hard")]
    SHIFT_CHOICES = [("day", "Day"), ("night", "Night")]
    PENALTY_CHOICES = [(20, 20), (10, 10)]
    user = models.ForeignKey(Nurses, on_delete=models.CASCADE) 
    timeinterval = models.CharField(max_length=200, blank=True)

    shifttype = models.CharField(max_length=200, choices=SHIFT_CHOICES, default="day")
    coverage_demand = models.IntegerField(default=7)
    constraints = models.CharField(max_length=200, choices=CONSTRAINT_CHOICES, default='soft')
    penalty_cost = models.IntegerField(choices=PENALTY_CHOICES, default=20)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)    

    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    shifttime = models.CharField(max_length=200, choices=SHIFT_CHOICES, default="day")

    def __str__(self):
        return f"{self.get_shifttype_display()} Shift"


class ShiftAssignment(models.Model):
    SHIFT_TYPE_CHOICES = [("day", "Day"), ("night", "Night")]
    nurse = models.ForeignKey(Nurses, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    shift_type = models.CharField(max_length=200, choices=SHIFT_TYPE_CHOICES, default="day")
    penalty_cost = models.IntegerField(default=10)

    days = models.ManyToManyField(Days)

    class Meta:
        unique_together = ('nurse', 'shift')

    def clean(self):
        # Check if the nurse has the required skill level to work the given shift type
        if not self.nurse.can_work(self.shift.shifttype):
            raise ValidationError('Nurse does not have the required skill level for this shift type.')

        # Check if the nurse is available during the time interval
        if not self.nurse.is_available(self.shift.timeinterval):
            raise ValidationError('Nurse is not available during this time interval.')

        # Check if the minimum coverage demand is met
        count = ShiftAssignment.objects.filter(shift=self.shift).count()
        if count < self.shift.coverage_demand:
            raise ValidationError('Minimum coverage demand is not met for this shift.')

        # Check if the nurse has already been assigned six times
        count = ShiftAssignment.objects.filter(nurse=self.nurse).count()
        if count >= 6:
            raise ValidationError('Nurse cannot be assigned more than six times.')
