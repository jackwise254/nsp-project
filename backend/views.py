from django.shortcuts import render, redirect
from .models import Nurses, Shifts, ShiftAssignment
from django.contrib import messages
from django.shortcuts import render
from .forms import ShiftsForm, NurseForm
from datetime import datetime
from .models import Days

def Home(request):
    nurses = Nurses.objects.all()
    shifts = Shifts.objects.all()
    shift_assignments = ShiftAssignment.objects.all()
    context = {"nurse_shifts": nurses, "assignments":shift_assignments}
    
    template_name = "nurses/home.html"
    return render(request, template_name, context)


from django.shortcuts import redirect
import sys
def NurseView(request):
    nurses = Nurses.objects.all()
    days_available = None
    tracy = []
    check_days = []

    for nurse in nurses:
        days_available = nurse.available_days.all()
        for day in days_available:
            tracy.append(day)
        
    form = NurseForm()
    context = {
        "nursess": nurses,
        "forms": form,
    }
    template_name = "nurses/nurses.html"
    weekend = ['Saturday', 'Sunday']

    if request.method == 'POST':
        try:
            d_name = None
            selected_days = request.POST.getlist('available_days')
            shift_type = request.POST.get('shift_type')
            for s in selected_days:
                for t in tracy:
                    d = Days.objects.get(id=s)
                    if t.name == d.name:
                        d_name = d.name
                        check_days.append(d)
            if len(check_days) > 6 and d_name not in weekend and any(nurse.shift_type == shift_type for nurse in nurses):
            
            # if len(check_days) > 6 and d_name not in weekend and all(shift_type == nurse.shift_type for nurse in nurses):


                messages.add_message(request, messages.INFO, f"{d_name} cannot be selected more than 7 times")
                return redirect('/nurses')
            elif len(check_days) > 7 and d_name in weekend:
                messages.add_message(request, messages.INFO, f"{d_name} cannot be selected more than 8 times")
                return redirect('/nurses')
            
            nurse = request.POST.get('nurse_id')
            exist = Nurses.objects.filter(nurse_id=nurse)
            if exist:
                messages.add_message(request, messages.INFO, 'Nurse id selected already exist')
                return redirect('nurses')
            en = Nurses(shift_type=shift_type, nurse_id=nurse)
            en.save()
            en.available_days.set(selected_days)
            return redirect('nurses')
        except Exception as e:
            print("An error occurred:", str(e))
            print("Traceback:", sys.exc_info())


    return render(request, template_name, context)


def ShiftsView(request):
    form = ShiftsForm()
    asigns = ShiftAssignment.objects.all()
    nursess = Nurses.objects.all()
    shifts = Shifts.objects.all()
    nurses = {}
    for nursesd in nursess:
        for shift in shifts:
            if nursesd.id == shift.user_id:
                nurses[nursesd] = {
                    'day':nursesd.available_days.all(),
                    "shift":nursesd.shift_type,
                    "penalty_cost":shift.penalty_cost,
                    "nurse_id": nursesd
                } 

    shifts = Shifts.objects.all()
    template = 'nurses/shifts.html'
    if request.method == 'POST':
        form = ShiftsForm(request.POST)
        if form.is_valid():
            form.save()

    context ={
       "forms":form, 
       "nurses":nurses,
       "nursess":nursess,
       "asigns":asigns,
       "shifts":shifts, 
    }

    return render(request, template, context)



from django.shortcuts import render, redirect
from .models import Nurses, Shifts, ShiftAssignment
from django.contrib import messages
from django.shortcuts import render
from .forms import ShiftsForm, NurseForm
from datetime import datetime
from .models import Days

def SchduleView(request):
    nurses = Nurses.objects.all()
    Shifts.objects.all().delete()
    ShiftAssignment.objects.all().delete()

    for n in nurses:
        en = Shifts(
            user = n,
            shifttype = n.shift_type,
            coverage_demand = len(n.available_days.all()),
            priority = 10,
            timeinterval = '7-15',
            shifttime = n.shift_type
        )
        en.save()
    shifts = Shifts.objects.all()

    # Initialize a dictionary to hold the shift assignments for each nurse
    nurse_shifts = {nurse: [] for nurse in nurses}

    # Sort the shifts by priority (e.g., based on demand, qualification, etc.)
    shifts = sorted(shifts, key=lambda x: x.priority)

    # Assign shifts to each nurse in turn
    for shift in shifts:
        assigned = False

        # Try to assign the shift to each nurse in turn
        for nurse in nurses:
            # Check if the nurse is available and can work the shift
            if nurse.is_available(shift.timeinterval) and nurse.can_work(shift.shifttype):
                # Assign the shift to the nurse
                nurse_shifts[nurse].append(shift)
                assigned = True
                try:
                    shift_assignment = ShiftAssignment.objects.get(nurse=nurse, shift=shift, shift_type=shift.shifttype)
                    shift_assignment.days.set(nurse.available_days.all())
                except ShiftAssignment.DoesNotExist:
                    shift_assignment = ShiftAssignment.objects.create(nurse=nurse, shift=shift)
                    shift_assignment.days.set(nurse.available_days.all())

            # If the shift has been assigned, break out of the loop
            if assigned:
                break

        # If no nurse can work the shift, add a penalty to the shift
        if not assigned:
            shift.penalty_cost += 10
            shift.save()

    return redirect('/')


def SchduleViews(request):
    nurses = Nurses.objects.all()
    shifts = Shifts.objects.all()
    ShiftAssignment.objects.all().delete()
    shift_assignments = ShiftAssignment.objects.all()
    nurse_shifts = {nurse: [] for nurse in nurses}
    shifts = sorted(shifts, key=lambda x: x.priority)
    for shift in shifts:
        assigned = False
        for nurse in nurses:
            if nurse.is_available(shift.timeinterval) and nurse.can_work(shift.shifttype):
                nurse_shifts[nurse].append(shift)
                assigned = True
                try:
                    shift_assignment = ShiftAssignment.objects.get(nurse=nurse, shift=shift, shift_type=shift.shifttype, penalty_cost=shift.penalty_cost)
                    shift_assignment.days.set(nurse.available_days.all())
                except ShiftAssignment.DoesNotExist:
                    shift_assignment = ShiftAssignment.objects.create(nurse=nurse, shift=shift, shift_type=shift.shifttype, penalty_cost=shift.penalty_cost)
                    shift_assignment.days.set(nurse.available_days.all())

                break
        if not assigned:
            shift.penalty_cost += shift.priority * 10
            shift.save()

    return redirect('/')

