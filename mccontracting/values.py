
USERS_GROUP_ADMINISTRATORS = 1
USERS_GROUP_EMPLOYEES = 2
USERS_GROUP_CUSTOMERS = 3

USERS_GROUPS = (
    (USERS_GROUP_ADMINISTRATORS, 'Administrators'),
    (USERS_GROUP_EMPLOYEES, 'Employees'),
    (USERS_GROUP_CUSTOMERS, 'Customers'),
)


STATUS_NEW_ID = 1
STATUS_PROGRESS_ID = 2
STATUS_COMPLETED_ID = 3

STATUSES = (
    (STATUS_NEW_ID, 'New'),
    (STATUS_PROGRESS_ID, 'Progress'),
    (STATUS_COMPLETED_ID, 'Completed'),
)


GENDER_FEMALE_ID = 1
GENDER_MALE_ID = 2

GENDERS = (
    (GENDER_FEMALE_ID, 'Female'),
    (GENDER_MALE_ID, 'Male'),
)


EVALUATION_TYPE_NO_EVALUATION = 0
EVALUATION_TYPE_BAD = 1
EVALUATION_TYPE_REGULAR = 2
EVALUATION_TYPE_GOOD = 3
EVALUATION_TYPE_VERY_GOOD = 4
EVALUATION_TYPE_EXCELLENT = 5

EVALUATION_TYPES = (
    (EVALUATION_TYPE_NO_EVALUATION, 'No Evaluation'),
    (EVALUATION_TYPE_BAD, 'Bad'),
    (EVALUATION_TYPE_REGULAR, 'Regular'),
    (EVALUATION_TYPE_GOOD, 'Good'),
    (EVALUATION_TYPE_VERY_GOOD, 'Very Good'),
    (EVALUATION_TYPE_EXCELLENT, 'Excellent')
)


MONTHS = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)


YEARS = (
    (2018, 2018),
    (2019, 2019),
    (2020, 2020),
    (2021, 2021),
    (2022, 2022),
    (2023, 2023),
    (2024, 2024),
    (2025, 2025),
)