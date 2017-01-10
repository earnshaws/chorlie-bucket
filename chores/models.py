from djmoney.models.fields import MoneyField
from django.db import models
from django.contrib.auth.models import User


class Chore(models.Model):
    HOURLY = 'h'
    DAILY = 'd'
    WEEKLY = 'w'
    FREQUENCIES = (
        (HOURLY, 'Hourly'),
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
    )
    name = models.CharField(max_length=32, unique=True)
    value = MoneyField(max_digits=5, decimal_places=2, default_currency='USD')
    frequency = models.CharField(max_length=1, choices=FREQUENCIES,
                                 default=DAILY)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AssignedChores(models.Model):
    user = models.ForeignKey(User)
    chores = models.ManyToManyField(Chore)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'assigned chores'

    def _possible_earnings_per_week(self):
        earnings = 0.
        hourly_earnings = 0.
        for chore in self.chores.filter(active=True):
            if chore.frequency == chore.DAILY:
                earnings += 7 * chore.value
            elif chore.frequency == chore.WEEKLY:
                earnings += chore.value
            elif chore.frequency == chore.HOURLY:
                hourly_earnings += chore.value
        msg = str(earnings) + ' + ' + str(hourly_earnings) + ' per hour'
        return msg
    possible_earnings_per_week = property(_possible_earnings_per_week)

    def _active_chores(self):
        return ', '.join(sorted(map(lambda x: x.name, self.chores.filter(active=True))))
    active_chores = property(_active_chores)


class Task(models.Model):
    user = models.ForeignKey(User)
    chore = models.ForeignKey(Chore)
    value = MoneyField(max_digits=5, decimal_places=2, default_currency='USD')
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_on = models.DateField()
    completed_at = models.DateTimeField()

    def _completed(self):
        return self.completed_at is not None
    completed = property(_completed)
