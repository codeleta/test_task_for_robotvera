from django.core.exceptions import ValidationError
from django.db import models


class Child(models.Model):
    """Child."""

    class GENDERS:
        BOY = 'boy'
        GIRL = 'girl'

        CHOICES = (
            (BOY, 'Мальчик'),
            (GIRL, 'Девочка'),
        )

    photo = models.ImageField('Фотография', upload_to='children/%Y/%m/%d/', null=True, blank=True)
    name = models.CharField('Имя', max_length=255)
    gender = models.CharField('Пол', choices=GENDERS.CHOICES, max_length=4)
    birthdate = models.DateField('Дата рождения')
    classroom = models.SmallIntegerField('Класс', null=True, blank=True)
    is_pupil = models.BooleanField('Учится', default=False, db_index=True)

    class Meta:
        verbose_name = 'Ребенок'
        verbose_name_plural = 'Дети'

    def __str__(self):
        """Str repr."""
        return f'{self._meta.verbose_name} {self.name}'


class JournalEntry(models.Model):
    """Journal Entry for Child."""

    class PEOPLES:
        DAD = 'dad'
        MOM = 'mom'

        CHOICES = (
            (DAD, 'Папа'),
            (MOM, 'Мама'),
        )

    child = models.ForeignKey(Child, verbose_name=Child._meta.verbose_name, on_delete=models.CASCADE)
    timestamp_come = models.TimeField('Время прихода', db_index=True)
    timestamp_away = models.TimeField('Время ухода', null=True, blank=True, db_index=True)
    people_come = models.CharField('Кто привел ребенка', max_length=3, choices=PEOPLES.CHOICES)
    people_away = models.CharField('Кто забрал ребенка', max_length=3, choices=PEOPLES.CHOICES, blank=True)
    datestamp = models.DateField('Дата записи', db_index=True)

    class Meta:
        verbose_name = 'Запись в журнале'
        verbose_name_plural = 'Записи в журнале'
        unique_together = ('child', 'datestamp')

    def __str__(self):
        """Str repr."""
        return f'{self._meta.verbose_name} от {self.datestamp}'

    def clean_fields(self, exclude=None):
        """
        Clean fields.

        Check when timestamp_away and people_away both equals None or both equals anything.

        :param exclude:
        :return:
        """
        super().clean_fields(exclude=exclude)
        one_of_fields_filled = self.timestamp_away or self.people_away
        both_fields_filled = self.timestamp_away and self.people_away
        if one_of_fields_filled and not both_fields_filled:
            timestamp_away_verbose_name = self._meta.get_field('timestamp_away').verbose_name
            people_away_verbose_name = self._meta.get_field('people_away').verbose_name
            raise ValidationError(
                f'В отметке об уходе надо заполнить поля {timestamp_away_verbose_name} и {people_away_verbose_name}',
            )
