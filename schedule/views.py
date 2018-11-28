from django.shortcuts import render
from schedule.models import Subject, SubjectRating, User
from django.views.generic import RedirectView


# Create your views here.
def index(request):
    """View function for home page of site."""

    if request.user.is_authenticated:
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
    user = User.objects.filter(username=parameter)
    context = {
        'user_ratings': user_ratings,
        'user_name': user
    }
    return render(request, 'user.html', context=context)


def save_ratings(request):
    print("saving")
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
