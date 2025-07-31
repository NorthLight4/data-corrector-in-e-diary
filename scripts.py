from random import choice
from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Commendation


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(full_name, subject):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    except Schoolkid.MultipleObjectsReturned:
        return 'Было найдено сразу несколько учеников с таким именем'
    except Schoolkid.DoesNotExist:
        return 'Ученик с данным именем не был найден'

    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                       subject__title__contains=subject).order_by('?').first()
    if not lesson:
        return 'Указанный предмет не был найден, проверьте правильность написания'

    commendation_templates = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
                              'Ты меня приятно удивил!',
                              'Великолепно!', 'Прекрасно!', 'Мегахароооооооооош!']

    Commendation.objects.create(text=choice(commendation_templates), created=lesson.date, schoolkid=schoolkid,
                                subject=lesson.subject, teacher=lesson.teacher)
