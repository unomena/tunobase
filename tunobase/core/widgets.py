'''
CORE APP

Useful widgets.

'''
import datetime

from django.forms import widgets
from django.utils.translation import ugettext as _

class DateSelectorWidget(widgets.MultiWidget):
    MONTHS = {
        1: _('Jan'),
        2: _('Feb'),
        3: _('Mar'),
        4: _('Apr'),
        5: _('May'),
        6: _('Jun'),
        7: _('Jul'),
        8: _('Aug'),
        9: _('Sep'),
        10: _('Oct'),
        11: _('Nov'),
        12: _('Dec')
    }

    def __init__(self, attrs=None, min_num_years_back=10,
            max_num_years_back=-1, reverse_years=False):
        # create choices for days, months, years
        # example below, the rest snipped for brevity.
        if max_num_years_back >= 0:
            max_num_years_back -= 1

        days = [(year, year) for year in range(1, 32)]
        months = [(year, self.MONTHS[year]) for year in range(1, 13)]

        if reverse_years:
            years = [(year, year) for year in reversed(range(
                (datetime.datetime.now() -
                    datetime.timedelta(days=min_num_years_back*365)).year,
                (datetime.datetime.now() -
                    datetime.timedelta(days=max_num_years_back*365)).year))
            ]
        else:
            years = [(year, year) for year in range(
                (datetime.datetime.now() -
                    datetime.timedelta(days=min_num_years_back*365)).year,
                (datetime.datetime.now() -
                    datetime.timedelta(days=max_num_years_back*365)).year)
            ]

        _widgets = (
            widgets.Select(attrs=attrs, choices=days),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=years),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]

        try:
            D = datetime.date(day=int(datelist[0]), month=int(datelist[1]),
                    year=int(datelist[2]))
        except ValueError:
            return ''
        else:
            return D
