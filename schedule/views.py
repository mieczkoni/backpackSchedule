from django.shortcuts import render
from schedule.models import Subject, SubjectRating, User, UserSubject
from django.views.generic import RedirectView
from backpackSchedule import solver_class, user_subject_count_manager as random_manager


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_subjects = UserSubject.objects.filter(user__username=request.user.username)
        all_subjects = Subject.objects.all()
        all_ratings = SubjectRating.objects.all()
        all_users = User.objects.all()
        user_ratings = SubjectRating.objects.filter(user=request.user)
        if request.user.username == "admin":
            calculate_average_ratings()
            check_if_all_rated()
            context = {
                'all_subjects': all_subjects,
                'all_ratings': all_ratings,
                'all_users': all_users
            }
            return render(request, 'users.html', context=context)
        else:
            context = {
                'all_subjects': all_subjects,
                'user_ratings': user_ratings,
                'user_subjects': user_subjects,
                'user_subjects_count': user_subjects.count()
            }
            return render(request, 'index.html', context=context)
    else:
        return RedirectView.as_view(url='/schedule/login', permanent=True)(request)


def admin_users(request):
    all_subjects = Subject.objects.all()
    all_ratings = SubjectRating.objects.all()
    all_users = User.objects.all()
    context = {
        'all_subjects': all_subjects,
        'all_ratings': all_ratings,
        'all_users': all_users
    }
    return render(request, 'users.html', context=context)


def admin_subjects(request):
    all_subjects = Subject.objects.all()
    all_ratings = SubjectRating.objects.all()
    all_users = User.objects.all()
    context = {
        'all_subjects': all_subjects,
        'all_ratings': all_ratings,
        'all_users': all_users
    }
    return render(request, 'subjects.html', context=context)


def admin_subject_ratings(request):
    all_subjects = Subject.objects.all()
    all_ratings = SubjectRating.objects.all()
    all_users = User.objects.all()
    context = {
        'all_subjects': all_subjects,
        'all_ratings': all_ratings,
        'all_users': all_users
    }
    return render(request, 'subject_ratings.html', context=context)


def show_subject(request, parameter):
    subject_ratings = SubjectRating.objects.filter(subject_id__name=parameter)
    subject = Subject.objects.filter(name=parameter)
    context = {
        'subject_ratings': subject_ratings,
        'subject_name': parameter,
        'subject': subject
    }
    return render(request, 'subject.html', context=context)


def show_user(request, parameter):
    user_ratings = SubjectRating.objects.filter(user__username=parameter)
    user_subjects = UserSubject.objects.filter(user__username=parameter)
    user = User.objects.filter(username=parameter)
    context = {
        'user_ratings': user_ratings,
        'user_name': user,
        'user_subjects': user_subjects
    }
    return render(request, 'user.html', context=context)


def save_ratings(request):
    all_subjects = Subject.objects.all()
    for subject in all_subjects:
        subject_value = request.POST.get(subject.name, '3')
        try:
            subject_element = SubjectRating.objects.get(subject_id=subject, user=request.user)
        except:
            subject_element = None
        if subject_element:
            subject_element.subject_rating = subject_value
            subject_element.save()
        else:
            SubjectRating.objects.create(user=request.user, subject_id=subject, subject_rating=subject_value)
    all_subjects = Subject.objects.all()
    user_ratings = SubjectRating.objects.filter(user=request.user)
    context = {
        'all_subjects': all_subjects,
        'user_ratings': user_ratings,
    }
    return render(request, 'index.html', context=context)


def solver_site(request):
    calculate_filled_hours()
    all_users = User.objects.all()
    # for user in all_users:
    #     if user.username != "admin":
    #         user.delete()
    # Subject.objects.all().delete()
    # SubjectRating.objects.all().delete()
    # UserSubject.objects.all().delete()
    context = {
        'users': all_users,
    }
    return render(request, 'solver.html', context=context)


def random_objects(request):
    user_count = int(request.POST.get('user_count'))
    subject_count = int(request.POST.get('subjects_count'))
    random_manager.RandomizeAll(user_count, subject_count).randomize()
    simulated_annealing()
    all_users = User.objects.all()
    context = {
        'users': all_users,
    }
    return render(request, 'solver.html', context=context)


def simulated_annealing():
    file = open("knapsacks_data.inst.dat", "w")
    all_users = User.objects.all()
    all_subjects = Subject.objects.all()
    subjects_count = all_subjects.count()
    for user in all_users:
        if user.username != "admin":
            user_ratings = SubjectRating.objects.filter(user__username=user.username)
            line = str(user.id) + " "
            line += str(subjects_count) + " "
            line += str(user.profile.hours) + " "
            for subject in all_subjects:
                line += str(subject.hours)
                line += " "
                for rating in user_ratings:
                    if rating.subject_id.name == subject.name:
                        line += str(rating.subject_rating)
                        line += " "
            line += "\n"
            file.write(line)
    file.close()
    solver_class.SimulatedAnnealing("knapsacks_data.inst.dat", "knapsacks_data.sol.dat").solver()
    analyze_values()


def solve_problem(request):
    simulated_annealing()
    calculate_filled_hours()
    all_users = User.objects.all()
    context = {
        'users': all_users,
    }
    return render(request, 'solver.html', context=context)


def analyze_values():
    UserSubject.objects.all().delete()
    all_users = User.objects.all()
    all_subjects = Subject.objects.all()
    all_subjects_names = [subject.name for subject in all_subjects]
    for user in all_users:
        if user.username != "admin":
            file = open("knapsacks_data.sol.dat", "r")
            for line in file:
                line_user_id = line.split()[0]
                if user.id == int(line_user_id):
                    user_results = line.split()[3:]
                    for i in range(len(user_results)):
                        if user_results[i] == "1":
                            UserSubject.objects.create(user=user, subject=Subject.objects.get(name=all_subjects_names[i]))
            file.close()
    calculate_filled_hours()


def calculate_filled_hours():
    all_user_subject = UserSubject.objects.all()
    all_users = User.objects.all()
    for user in all_users:
        filled_hours = 0
        for pair in all_user_subject:
            if pair.user == user:
                filled_hours += pair.subject.hours
        user.profile.filled_hours = filled_hours
        user.save()


def calculate_average_ratings():
    all_subjects = Subject.objects.all()
    for subject in all_subjects:
        try:
            subject_elements = SubjectRating.objects.filter(subject_id=subject)
        except:
            subject_elements = None
        if subject_elements:
            sum = 0
            for element in subject_elements:
                sum += element.subject_rating
            average_rating = sum / subject_elements.count()
            subject.average_rating = average_rating
            subject.save()


def check_if_all_rated():
    all_users = User.objects.all()
    all_subjects = Subject.objects.all()
    for user in all_users:
        try:
            rated_subjects = SubjectRating.objects.filter(user=user)
        except:
            rated_subjects = None
        if rated_subjects:
            if rated_subjects.count() == all_subjects.count():
                user.profile.rated = True
                user.save()
            else:
                user.profile.rated = False
                user.save()


