LEAVE_STATUS = [
    ('PENDING' , 'PENDING'),
    ('CONFIRMED' , 'CONFIRMED'),
    ('REJECTED','REJECTED')
]

ATTENDANCE_STATUS = [
    ('PRESENT' , 'Present'),
    ('ABSENT' , 'Absent')
]

TASK_STATUS = [
    ('PENDING' , 'PENDING'),
    ('IN PROGRESS' , 'IN PROGRESS'),
    ('COMPLETED','COMPLETED')
]

EMPLOYEE_TYPE = [
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('contractor', 'Contractor'),
    ('intern', 'Intern'),
]

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    )
USER_TYPE = (
    ('0', 'SUPERADMIN'),
    ('1', 'HRMANAGER'),
    ('2', 'EMPLOYEE'),
)
LEAVE_TYPES = (
    ('Sick Leave', 'Sick Leave'),
    ('Vacation Leave', 'Vacation Leave'),
    ('Maternity/Paternity Leave', 'Maternity/Paternity Leave'),
    ('Unpaid Leave', 'Unpaid Leave'),
    )