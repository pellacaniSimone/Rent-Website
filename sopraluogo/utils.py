from dashboard.debug_utils import debug_info
from calendar import HTMLCalendar
from .models import Sopraluogo

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		debug_info(self)
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	def formatday(self, day, events):
		debug_info(self)
		events_per_day = events.filter(data_ora_sopraluogo__day=day)
		d = ''
		for event in events_per_day:
			d += f' Sopraluogo {event.immobile.__str__()[:20] } <br>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	def formatweek(self, theweek, events):
		debug_info(self)
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	def formatmonth(self, withyear=True):
		debug_info(self)
		events = Sopraluogo.objects.filter(data_ora_sopraluogo__year=self.year, data_ora_sopraluogo__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		print (cal)
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal + "</table> <br><br>"