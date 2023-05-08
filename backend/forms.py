from django import forms
from .models import Nurses, Shifts, Days

from django import forms
from .models import Shifts, Nurses

class ShiftsForm(forms.ModelForm):
    CONSTRAINT_CHOICES = [("soft", "Soft"), ("hard", "Hard")]
    SHIFT_CHOICES = [("day", "Day"), ("night", "Night")]
    # PENALTY_CHOICES = [(20, 20), (10, 10)]

    shifttype = forms.ChoiceField(choices=SHIFT_CHOICES)
    coverage_demand = forms.IntegerField(min_value=1)
    constraints = forms.ChoiceField(choices=CONSTRAINT_CHOICES)
    # penalty_cost = forms.ChoiceField(choices=PENALTY_CHOICES)
    priority = forms.IntegerField(min_value=1, max_value=10)
    user = forms.ModelChoiceField(queryset=Nurses.objects.all())
    timeinterval = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Shifts
        fields = ['user','shifttype', 'coverage_demand', 'constraints', 'priority', 'timeinterval']

        labels = {
            'user': 'Nurse',
            'shifttype': 'Shift Type',
            'coverage_demand': 'Coverage Demand',
            'constraints': 'Constraints',
            # 'penalty_cost': 'Penalty Cost',
            'priority': 'Priority',
            'timeinterval': 'Time Interval',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'shifttype': forms.Select(attrs={'class': 'form-control'}),
            'coverage_demand': forms.NumberInput(attrs={'class': 'form-control'}),
            'constraints': forms.Select(attrs={'class': 'form-control'}),
            # 'penalty_cost': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'timeinterval': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class NurseForm(forms.ModelForm):
    nurse_id = forms.IntegerField(min_value=1, max_value=17)
    shift_type = forms.ChoiceField(choices=[("day", "Day"), ("night", "Night")])
    available_days = forms.ModelMultipleChoiceField(
        queryset=Days.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Nurses
        fields = ['nurse_id', 'available_days', 'shift_type', 'hours_available']
        labels = {
            'nurse_id': 'Nurse ID',
            'hours_available': 'Hours Available',
            'available_days': 'Available Days',
            'shift_type': 'Shift Type',
        }
        widgets = {
            'nurse_id': forms.Select(attrs={'class': 'form-control'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nurse_id(self):
        nurse_id = self.cleaned_data['nurse_id']
        nurse_count = Nurses.objects.filter(nurse_id=nurse_id).count()
        if nurse_count >= 6:
            raise forms.ValidationError('Nurse cannot be selected more than 6 times.')
        return nurse_id

    def clean(self):
        cleaned_data = super().clean()
        nurse_id = cleaned_data.get('nurse_id')
        shift_type = cleaned_data.get('shift_type')

        if nurse_id and shift_type:
            day_count = Nurses.objects.filter(nurse_id=nurse_id, shift_type=shift_type).count()
            if shift_type == 'day':
                if day_count >= 7:
                    raise forms.ValidationError('Day shift can only be selected 7 times.')
            elif shift_type == 'night':
                if day_count >= 8:
                    raise forms.ValidationError('Night shift can only be selected 8 times.')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
