from wtforms import Form, StringField, validators
from wtforms.ext.dateutil.fields import DateTimeField


class EventForm(Form):
    """Form for handling registration form validation
    """
    title = StringField(
        'title',
        [validators.required(),
         validators.Length(min=4, max=256)]
    )
    description = StringField(
        'password',
        [validators.required(),
         validators.Length(min=0, max=2000)]
    )
    subtitle = StringField(
        'subtitle',
        [validators.Length(min=0, max=500)]
    )
    start = DateTimeField('start', [validators.required()])
    end = DateTimeField('end', [validators.required()])
