from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from algorithm.base import calculate_age, generateUserID
import re, random
from django.core.validators import MinValueValidator


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, phone, first_name, last_name, day_of_birth, gender, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError('Email is invalid!')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValueError('Email already exists!')

        if not username:
            raise ValueError("You have not provided a valid username")

        password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[~`!@#$%^&*()-_+=\[\]{}\\|;:<>,./?*]).{8,}$'
        if not re.match(password_pattern, password):
            raise ValueError("Passwords must have at least 8 characters, including uppercase letters,"
                             "lowercase letters,numbers and special characters to ensure security!")

        email = self.normalize_email(email)
        user_id = generateUserID(email, 'VN')

        user = self.model(user_id=user_id,
                          email=email,
                          username=username,
                          phone=phone,
                          first_name=first_name,
                          last_name=last_name,
                          day_of_birth=day_of_birth,
                          gender=gender,
                          **extra_fields)
        user.set_password(password)
        random_index = random.randint(1, 10)
        if gender == '0':
            user.avatar = f"avatars/nam{random_index}.jpg"
        else:
            user.avatar = f"avatars/nu{random_index}.jpg"
        user.save(using=self._db)
        bag = Bag(user=user)
        bag.save()
        return user

    def create_user(self, username, email, password, phone, first_name, last_name, day_of_birth, gender, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_manager', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(username,
                                 email,
                                 password,
                                 phone,
                                 first_name,
                                 last_name,
                                 day_of_birth,
                                 gender,
                                 **extra_fields)

    def create_superuser(self, username, email, password, phone, first_name, last_name, day_of_birth, gender, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username,
                                 email,
                                 password,
                                 phone,
                                 first_name,
                                 last_name,
                                 day_of_birth,
                                 gender,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(primary_key=True, unique=True, max_length=36, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(unique=True, max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    mode_choose = ((0, "Public"),
                   (1, "Follower"),
                   (2, "Fan"),
                   (3, "Fiend"),
                   (4, "Private"))
    view_timeline_permission = models.IntegerField(choices=mode_choose, default=0)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    background = models.ImageField(null=True, blank=True)
    day_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    gender_choice = ((0, "Male"), (1, "Female"), (2, "Other"))
    gender = models.IntegerField(choices=gender_choice, default=0)
    story = models.CharField(max_length=50, null=True, blank=True)
    relationship_choice = ((0, "Single"), (1, "Dating"), (2, "Married"))
    relationship = models.IntegerField(choices=relationship_choice, default=0)
    hometown = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    hobby = models.CharField(max_length=100, null=True, blank=True)

    friends = models.TextField(default='', blank=True, null=True)
    friend_quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    # Who do you follow?
    follows = models.TextField(default='', blank=True, null=True)
    follow_quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    # Who follows you?
    followers = models.TextField(default='', blank=True, null=True)
    follower_quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    # Who are you a fan of?
    idols = models.TextField(default='', blank=True, null=True)
    idol_quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    # Who fans you?
    fans = models.TextField(default='', blank=True, null=True)
    fan_quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    businessmen_choose = ((0, "None"),
                          (1, "Startup"),
                          (2, "Small trader"),
                          (3, "Silver"),
                          (4, "Gold"),
                          (5, "Platinum"),
                          (6, "Tycoon"))
    businessmen_rank = models.IntegerField(choices=businessmen_choose, default=0)

    popularity_choose = ((0, "None"),
                         (1, "Favorite person"),
                         (2, "Idol"),
                         (3, "Public figure"),
                         (4, "Celebrity"),
                         (5, "D-list star"),
                         (6, "C-list star"),
                         (7, "B-list star"),
                         (8, "A-list star"),
                         (9, "S-list star"))
    popularity_rank = models.IntegerField(choices=popularity_choose, default=0)

    artist_choose = ((0, "None"),
                     (1, "Artist"),
                     (2, "Outstanding artist"),
                     (3, "People's Artist"))
    artist_rank = models.IntegerField(choices=artist_choose, default=0)

    aristocrat_choose = ((0, "Layman"),
                         (1, "Baron"),
                         (2, "Viscount"),
                         (3, "Earl"),
                         (4, "Marquess"),
                         (5, "Duke"),
                         (6, "King"))
    aristocrat_rank = models.IntegerField(choices=aristocrat_choose, default=0)
    is_abaddoner = models.BooleanField(default=False)
    is_universeExplorer = models.BooleanField(default=False)
    is_globeTrotter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Users'

    def save(self, *args, **kwargs):
        self.age = calculate_age(self.day_of_birth)
        self.friend_quantity = len(str(self.friends).split('@')[:-1])
        self.follow_quantity = len(str(self.follows).split('@')[:-1])
        self.follower_quantity = len(str(self.followers).split('@')[:-1])
        self.idol_quantity = len(str(self.idols).split('@')[:-1])
        self.fan_quantity = len(str(self.fans).split('@')[:-1])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Bag(models.Model):
    bag_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sapphires = models.PositiveBigIntegerField(default=0)  # Main currency

    class Meta:
        db_table = 'Bags'

    objects = models.Manager()


class Item(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=20, null=False, blank=False)
    item_image = models.ImageField(max_length=255, null=False, blank=False)
    price = models.BigIntegerField(validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    bag = models.ManyToManyField('Bag', blank=True, through='BagItem')

    class Meta:
        db_table = 'Items'

    objects = models.Manager()


class BagItem(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    class Meta:
        db_table = 'BagItems'
    objects = models.Manager()
