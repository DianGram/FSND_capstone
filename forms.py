from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Regexp, Length


class TaskForm(Form):
    title = StringField(
        'Title', validators=[DataRequired()]
    )

    details = TextAreaField(
        'Details'
    )

    date_needed = DateField(
        'Date Needed', validators=[DataRequired()]
    )

    status = SelectField(
        'Status',
        choices=[
            ('Open', 'Open'),
            ('Filled', 'Filled'),
            ('Complete', 'Complete'),
        ]
    )

    volunteer = SelectField(
        'Assign Volunteer',
        coerce=int
    )


class VolunteerForm(Form):
    name = StringField(
        'Name', validators=[DataRequired()]
    )

    address = StringField(
        'Address', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )

    state = SelectField(
        'State', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AR', 'AR'),
            ('AZ', 'AZ'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DC', 'DC'),
            ('DE', 'DE'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('IA', 'IA'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('MA', 'MA'),
            ('MD', 'MD'),
            ('ME', 'ME'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('MT', 'MT'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('NE', 'NE'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NV', 'NV'),
            ('NY', 'NY'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VA', 'VA'),
            ('VT', 'VT'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )

    zip_code = StringField(
        'Zip Code', validators=[DataRequired(),
                                Length(min=5, max=10,  message='Enter a valid'
                                                               ' Zip Code')]
    )

    phone_number = StringField(
        'Phone Number', validators=[DataRequired(),
                                    Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{4}$',
                                           message='Phone number should be in'
                                                   ' the format xxx-xxx-xxxx')
                                    ]
    )
