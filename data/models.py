from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from pytils.translit import slugify
from django_ckeditor_5.fields import CKEditor5Field
from colorfield.fields import ColorField

# ==============================
# Факультет
# ==============================
class Faculty(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    slug = models.CharField('ЧПУ', max_length=255, blank=True, null=True)
    short_description = models.TextField(
        verbose_name="Короткое описание",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):

        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# ==============================
# Формат обучения
# ==============================
class EducationFormat(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )

    class Meta:
        verbose_name = "Формат обучения"
        verbose_name_plural = "Форматы обучения"

    def __str__(self):
        return self.name


# ==============================
# Программа обучения
# ==============================
class EducationProgramTag(models.Model):
    label = models.CharField(max_length=50, blank=False, null=True)

    class Meta:
        verbose_name = "Теги Программа обучения"
        verbose_name_plural = "Теги Программа обучения"

    def __str__(self):
        return self.label

class EducationProgram(models.Model):
    tags = models.ManyToManyField(EducationProgramTag, blank=True,verbose_name="Теги")
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="programs",
        verbose_name="Факультет"
    )
    show_on_main = models.BooleanField(
        default=False,
        verbose_name="Показать на главной"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок вывода"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    slug = models.CharField('ЧПУ', max_length=255, blank=True, null=True)


    background_image = models.ImageField(
        upload_to="programs/backgrounds/",
        verbose_name="Фотография на задний фон",
        blank=True,
        null=True
    )
    cover_image = models.ImageField(
        upload_to="programs/covers/",
        verbose_name="Фотография обложка",
        blank=True,
        null=True
    )
    short_description = models.TextField(
        verbose_name="Короткое описание",
        blank=True,
        null=True
    )
    duration = models.CharField(
        max_length=255,
        verbose_name="Срок обучения (текстовое)",
        blank=True,
        null=True
    )
    price = models.CharField(
        max_length=255,
        verbose_name="Стоимость (текстовое)",
        blank=True,
        null=True
    )
    format = models.ForeignKey(
        EducationFormat,
        on_delete=models.SET_NULL,
        null=True,
        related_name="programs",
        verbose_name="Формат обучения"
    )
    start_date = models.CharField(
        max_length=255,
        verbose_name="Дата начала (текстовое)",
        blank=True,
        null=True
    )
    teachers = models.ManyToManyField(
        "user.User",
        limit_choices_to={"is_teacher": True},
        blank=True,
        related_name="teaching_programs",
        verbose_name="Прикрепленные преподаватели"
    )
    video = models.FileField(
        upload_to="programs/videos/",
        verbose_name="Видео файл",
        blank=True,
        null=True
    )
    video_text = models.TextField(
        verbose_name="Текст на видео блок",
        blank=True,
        null=True
    )
    is_online = models.BooleanField(
        default=True,
        null=False,
    )
    study_plan = models.FileField(upload_to="programs/study_plans/",
                                  verbose_name="План обучения",
                                  blank=True,
                                  null=True)


    class Meta:
        verbose_name = "Программа обучения"
        verbose_name_plural = "Программы обучения"
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProgramAboutItem(models.Model):
    BLOCK_TYPES = (
        ('default', "Белый"),
        ('primary', "Красный"),
        ('dark', "Темный"),
    )

    program = models.ForeignKey(
        EducationProgram,
        on_delete=models.CASCADE,
        related_name="about_items",
        verbose_name="Программа"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    svg = models.TextField( verbose_name="КОД SVG", blank=True,
        null=True
    )
    text = CKEditor5Field(verbose_name="Текст")

    block_type = models.CharField(
        max_length=10,
        choices=BLOCK_TYPES,
        verbose_name="Вид плашки"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")

    class Meta:
        verbose_name = "Пункт 'О программе'"
        verbose_name_plural = "Пункты 'О программе'"
        ordering = ["order"]

    def __str__(self):
        return f"{self.program.name} - {self.name}"


class ProgramModule(models.Model):
    program = models.ForeignKey(
        EducationProgram,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name="Программа"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")
    description = CKEditor5Field(verbose_name="Описание", blank=True, null=True)
    files = models.FileField(
        upload_to="programs/modules/files/",
        verbose_name="Файлы",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Модуль обучения"
        verbose_name_plural = "Модули обучения"
        ordering = ["order"]

    def __str__(self):
        return f"{self.program.name} - {self.name}"



# ==============================
# Формат лекций
# ==============================
class LectureFormat(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    color = ColorField(default='#000000')
    icon = models.ImageField(
        upload_to="lectures/icons/",
        verbose_name="Иконка",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Формат лекций"
        verbose_name_plural = "Форматы лекций"

    def __str__(self):
        return self.name


class Lecture(models.Model):

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок вывода"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )
    slug = models.CharField('ЧПУ', max_length=255, blank=True, null=True)


    background_image = models.ImageField(
        upload_to="programs/backgrounds/",
        verbose_name="Фотография на задний фон",
        blank=True,
        null=True
    )
    cover_image = models.ImageField(
        upload_to="programs/covers/",
        verbose_name="Фотография обложка",
        blank=True,
        null=True
    )
    short_description = models.TextField(
        verbose_name="Короткое описание",
        blank=True,
        null=True
    )
    duration = models.CharField(
        max_length=255,
        verbose_name="Срок обучения (текстовое)",
        blank=True,
        null=True
    )
    price = models.CharField(
        max_length=255,
        verbose_name="Стоимость (текстовое)",
        blank=True,
        null=True
    )
    format = models.ForeignKey(
        LectureFormat,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Формат "
    )
    start_date = models.CharField(
        max_length=255,
        verbose_name="Дата начала (текстовое)",
        blank=True,
        null=True
    )
    end_date = models.CharField(
        max_length=255,
        verbose_name="Дата окончания (текстовое)",
        blank=True,
        null=True
    )
    date = models.CharField(
        max_length=255,
        verbose_name="Дата проведения",
        blank=True,
        null=True
    )
    learn_time = models.CharField(
        max_length=255,
        verbose_name="Нагрузка",
        blank=True,
        null=True
    )
    access = models.CharField(
        max_length=255,
        verbose_name="Доступ",
        blank=True,
        null=True
    )
    format_txt = models.CharField(
        max_length=255,
        verbose_name="Формат(текст)",
        blank=True,
        null=True
    )
    teachers = models.ManyToManyField(
        "user.User",
        limit_choices_to={"is_teacher": True},
        blank=True,
        related_name="teachers",
        verbose_name="Прикрепленные преподаватели"
    )
    video = models.FileField(
        upload_to="programs/videos/",
        verbose_name="Видео файл",
        blank=True,
        null=True
    )
    video_text = models.TextField(
        verbose_name="Текст на видео блок",
        blank=True,
        null=True
    )

    study_plan = models.FileField(upload_to="programs/study_plans/",
                                  verbose_name="План обучения",
                                  blank=True,
                                  null=True)


    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class LectureAboutItem(models.Model):
    BLOCK_TYPES = (
        ('default', "Белый"),
        ('primary', "Красный"),
        ('dark', "Темный"),
    )

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="about_items",
        verbose_name="Лекция"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    svg = models.TextField( verbose_name="КОД SVG", blank=True,
        null=True
    )
    text = CKEditor5Field(verbose_name="Текст")

    block_type = models.CharField(
        max_length=10,
        choices=BLOCK_TYPES,
        verbose_name="Вид плашки"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")

    class Meta:
        verbose_name = "Пункт 'Результат обучения'"
        verbose_name_plural = "Пункты 'Результат обучения'"
        ordering = ["order"]

    def __str__(self):
        return f"{self.lecture.name} - {self.name}"

class LectureForItem(models.Model):

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="for_items",
        verbose_name="Программа"
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    svg = models.TextField( verbose_name="КОД SVG", blank=True,
        null=True
    )
    text = models.TextField(verbose_name="Текст")

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")

    class Meta:
        verbose_name = "Пункт 'Для кого'"
        verbose_name_plural = "Пункты 'Для кого'"
        ordering = ["order"]

    def __str__(self):
        return f"{self.lecture.name} - {self.name}"

class LectureModule(models.Model):
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="lecture_modules",
        verbose_name="Программа",
        null=True,
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")
    description = CKEditor5Field(verbose_name="Описание", blank=True, null=True)
    files = models.FileField(
        upload_to="programs/modules/files/",
        verbose_name="Файлы",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Модуль обучения"
        verbose_name_plural = "Модули обучения"
        ordering = ["order"]

    def __str__(self):
        return f"{self.lecture.name} - {self.name}"

class NewsTag(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    name = models.CharField('Название', max_length=255, blank=False, null=False)
    slug = models.CharField('ЧПУ', max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True, null=True, editable=False)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Тег новости'
        verbose_name_plural = 'Теги новостей'


class NewsItem(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    tags = models.ManyToManyField(NewsTag,blank=True,related_name='Теги')
    creator = models.ForeignKey(
        "user.User",
        limit_choices_to={"is_teacher": True},
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор"
    )
    top_image = models.ImageField(
        upload_to="news/backgrounds/",
        verbose_name="Фотография вверху",
        blank=True,
        null=True
    )
    cover_image = models.ImageField(
        upload_to="news/covers/",
        verbose_name="Фотография обложка",
        blank=True,
        null=True
    )

    name = models.CharField('Название', max_length=255, blank=False, null=True)
    slug = models.CharField('ЧПУ',
                            max_length=255,
                            help_text='Если не заполнено, создается на основе поля Назавание',
                            blank=True,
                            null=True,
                            editable=False)


    description = models.TextField('Короткое описание', blank=True, null=True)
    content = CKEditor5Field('Контент', blank=True, null=False, config_name='extends')


    created_at = models.CharField('Дата публикации', max_length=50, blank=False, null=True)
    show_on_main = models.BooleanField('Показывать на главной',default=False,null=False)
    is_active = models.BooleanField('Активно',default=True,null=False)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Partner(models.Model):
    order_num = models.IntegerField(default=1, null=True)
    top_image = models.ImageField(
        upload_to="parnert/images/",
        verbose_name="Фотография",
        blank=True,
        null=True
    )
    text = models.TextField('Текст', blank=True, null=True)
    author = models.CharField('Автор', max_length=255, blank=True, null=True)
    text1 = models.CharField('Подпись', max_length=255, blank=True, null=True)
    show_on_main = models.BooleanField('Показывать на главной', default=True, null=False)

    class Meta:
        ordering = ('order_num',)
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'