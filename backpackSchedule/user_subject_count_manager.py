import random
from schedule.models import Subject, SubjectRating, User
from schedule import views


class RandomizeAll():

    def __init__(self, users_count, subjects_count):
        self.users_count = users_count
        self.subjects_count = subjects_count

    def randomize(self):
        self.randomize_subjects()
        self.randomize_users()

    def randomize_users(self):
        SubjectRating.objects.all().delete()
        all_users = User.objects.all()
        for user in all_users:
            if user.username != "admin":
                user.delete()
        usernames = ['grant333', 'penaxxy', 'jessica957', 'kerri333', 'natashaxxy', 'white34', 'vanessa957', 'meredith957', 'carolm_e', 'barreraxxy', 'julia957', 'holman34', 'marisa957', 'dejesus', 'gayle4a4', 'prince4a4', 'keri22', 'duran789', 'schmidt34', 'lara34', 'perry789', 'randall34', 'josefam_e', 'vega1_a', 'fitzgerald34', 'burns', 'byrdm_e', 'guerreroxxy', 'solisxxy', 'lottiexxy', 'bates4a4', 'benton', 'barbara333', 'meganm_e', 'guy', 'clinexxy', 'juliette', 'susanna', 'mildred789', 'valdez', 'wilkersonm_e', 'daisy', 'lucile4a4', 'savage', 'mannxxy', 'adrienne22', 'comptonm_e', 'britney22', 'gill957', 'russo1_a', 'bryan', 'parsonsm_e', 'burt957', 'sherri789', 'dawn1_a', 'pruitt957', 'reyes333', 'munozm_e', 'middleton333', 'cathy', 'wendi', 'crawford957', 'sophia1_a', 'petram_e', 'lucy957', 'sadiem_e', 'crosbym_e', 'jean4a4', 'blevinsxxy', 'moses', 'berg333', 'rivasm_e', 'flossie22', 'cook', 'blackm_e', 'swanson', 'lindsey34', 'soto', 'marcia957', 'mendoza', 'drake4a4', 'stafford22', 'janice1_a', 'douglas1_a', 'kerrym_e', 'ines22', 'martinxxy', 'combsxxy', 'roxie', 'michele22', 'tricia957', 'cohen', 'ernam_e', 'shawna', 'gail34', 'sherry22', 'jensen', 'branchxxy', 'terrellxxy', 'graciela333']
        emails = ['marshall@yahoo.com', 'valdez@yahoo.com', 'miles@mail.com', 'barber@gmail.com', 'gamble@outlook.com', 'castaneda@mail.com', 'ryan@mail.com', 'hendricks@yahoo.com', 'kelly@mail.com', 'ramsey@gmail.com', 'petersen@yahoo.com', 'valencia@outlook.com', 'cain@outlook.com', 'norris@gmail.com', 'gaines@yahoo.com', 'phelps@gmail.com', 'hudson@mail.com', 'clayton@mail.com', 'english@outlook.com', 'lynn@outlook.com', 'bradley@outlook.com', 'hurley@gmail.com', 'gardner@outlook.com', 'hayes@yahoo.com', 'stanton@mail.com', 'marks@mail.com', 'hewitt@outlook.com', 'woodard@outlook.com', 'mullen@outlook.com', 'stone@outlook.com', 'dunn@mail.com', 'willis@mail.com', 'bernard@yahoo.com', 'singleton@outlook.com', 'mccoy@mail.com', 'lindsay@gmail.com', 'medina@gmail.com', 'simmons@outlook.com', 'clark@mail.com', 'bruce@gmail.com', 'hardin@yahoo.com', 'mcintyre@mail.com', 'mccormick@outlook.com', 'mayer@yahoo.com', 'cox@outlook.com', 'miller@outlook.com', 'dejesus@yahoo.com', 'soto@yahoo.com', 'hansen@gmail.com', 'mccray@gmail.com', 'conway@mail.com', 'mcfadden@mail.com', 'hawkins@outlook.com', 'stokes@mail.com', 'bauer@mail.com', 'acevedo@gmail.com', 'riggs@yahoo.com', 'buckley@mail.com', 'sawyer@outlook.com', 'guzman@mail.com', 'michael@gmail.com', 'odom@mail.com', 'cochran@yahoo.com', 'brewer@outlook.com', 'bender@yahoo.com', 'frazier@yahoo.com', 'meadows@mail.com', 'wiley@outlook.com', 'fletcher@outlook.com', 'kirk@outlook.com', 'davidson@mail.com', 'bartlett@outlook.com', 'holland@gmail.com', 'rodgers@gmail.com', 'golden@gmail.com', 'clarke@yahoo.com', 'mcgowan@mail.com', 'edwards@outlook.com', 'greer@outlook.com', 'carver@gmail.com', 'morin@outlook.com', 'carrillo@outlook.com', 'wilder@yahoo.com', 'burks@outlook.com', 'herrera@mail.com', 'campbell@yahoo.com', 'peck@mail.com', 'juarez@gmail.com', 'dominguez@yahoo.com', 'henderson@outlook.com', 'yang@mail.com', 'oneil@yahoo.com', 'alexander@mail.com', 'norman@mail.com', 'harrington@gmail.com', 'hale@gmail.com', 'wade@outlook.com', 'hines@outlook.com', 'murray@yahoo.com', 'mitchell@mail.com']
        for i in range(self.users_count):
            random_username = random.choice(usernames)
            usernames.remove(random_username)
            random_email = random.choice(emails)
            emails.remove(random_email)
            new_user = User.objects.create_user(random_username, random_email, "qwerty")
            new_user.profile.hours = random.randint(80, 200)
            new_user.save()
            self.randomize_subjects_ratings(new_user)
        views.calculate_filled_hours()
        views.calculate_average_ratings()
        views.check_if_all_rated()

    def randomize_subjects(self):
        Subject.objects.all().delete()
        subjects = ['Language Arts', 'Mathematics', 'Science', 'Health', 'Handwriting', 'Physical Education (P.E.)', 'Art', 'Music', 'Instrumental Music – specific instrument', 'Movement or Eurythmy', 'Handwork or handcrafts', 'Life Lab or gardening', 'Dramatics', 'Dance', 'Spanish or other foreign language', 'Leadership', 'Special Education Day Class', 'Resource Program', 'Speech', 'Adaptive P.E.', 'Occupational Therapy', 'Reading', 'Language arts', 'Speech and Debate', 'English', 'Basic Math', 'Pre-algebra', 'Consumer Math', 'Algebra', 'Geometry', 'Honors Math in Algebra or Geometry', 'Life Science', 'Earth Science', 'Physical Science', 'Social Studies', 'Geography', 'Ancient Civilizations', 'Medieval and Renaissance', 'U.S. History and Government', 'Computer Science or Lab', 'Home Economics', 'Woodshop', 'Metal Shop', 'Business Technology', 'Instrumental Music', 'Band', 'Drama', 'Physical Education', 'Sports', 'Speech Therapy', 'Remedial English', 'ESL – English as second language', 'World Literature', 'Ancient Literature', 'Medieval Literature', 'Renaissance Literature', 'Modern Literature', 'British Literature', 'American Literature', 'Composition', 'Creative Writing', 'Poetry', 'Grammar', 'Vocabulary', 'Debate', 'Journalism', 'Publishing Skills', 'Photojournalism', 'Yearbook', 'Study Skills', 'Research Skills', 'Art Appreciation', 'Art History', 'Drawing', 'Painting', 'Sculpture', 'Ceramics', 'Pottery', 'Music Appreciation', 'Music History', 'Music Theory', 'Music Fundamentals', 'Orchestra', 'Choir', 'Voice']
        for i in range(self.subjects_count):
            random_subject_name = random.choice(subjects)
            subjects.remove(random_subject_name)
            new_subject = Subject.objects.create(name=random_subject_name, hours=random.randint(40, 90))
            new_subject.save()

    def randomize_subjects_ratings(self, user):
        all_subjects = Subject.objects.all()
        for subject in all_subjects:
            new_rating = SubjectRating.objects.create(user=user, subject_rating=random.randint(0, 9), subject_id=subject)
            new_rating.save()

