from django.shortcuts import render
from schedule.models import Subject, SubjectRating, Profile
from django.views.generic import RedirectView


# Create your views here.
def index(request):
    """View function for home page of site."""

    if request.user.is_authenticated:
        subject_count = Subject.objects.all().count()
        all_subjects = Subject.objects.all()

        user_ratings = SubjectRating.objects.filter(user=request.user)
        # user_ratings = []

        context = {
            'subject_count': subject_count,
            'all_subjects': all_subjects,
            'user_ratings': user_ratings
        }
        return render(request, 'index.html', context=context)
    else:
        return RedirectView.as_view(url='/schedule/login', permanent=True)(request)


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

