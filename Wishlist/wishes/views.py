"""Представления (контроллеры) вишлиста. Бизнес-логика вынесена в validators/weeks/models."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Wish
from .validators import clean_date, clean_text
from .weeks import DAY_NAMES, WeekCalendar


def _date_or(value, default):
    """Вернуть проверенную дату или default, если значение некорректно."""
    try:
        return clean_date(value)
    except ValueError:
        return default


def _back(day):
    """Редирект на страницу недели, в которой лежит day."""
    return redirect(f"{reverse('week')}?d={WeekCalendar(day).monday.isoformat()}")


@login_required
def week(request):
    """Страница недели: 7 карточек-дней с желаниями текущего пользователя."""
    today = timezone.localdate()
    cal = WeekCalendar(_date_or(request.GET.get("d"), today))

    by_day = {}
    for wish in Wish.objects.filter(user=request.user, date__range=(cal.monday, cal.sunday)):
        by_day.setdefault(wish.date, []).append(wish)

    days = [
        {"date": d, "name": DAY_NAMES[i], "wishes": by_day.get(d, []), "today": d == today}
        for i, d in enumerate(cal.dates())
    ]
    all_wishes = [w for lst in by_day.values() for w in lst]
    return render(request, "wishes/week.html", {
        "days": days,
        "monday": cal.monday,
        "sunday": cal.sunday,
        "week_number": cal.number,
        "prev_week": cal.shifted(-1).monday.isoformat(),
        "next_week": cal.shifted(1).monday.isoformat(),
        "is_current": cal.contains(today),
        "total": len(all_wishes),
        "done": sum(w.done for w in all_wishes),
    })


@login_required
@require_POST
def add(request):
    """Добавить желание. Некорректные дата или текст молча игнорируются."""
    today = timezone.localdate()
    try:
        day = clean_date(request.POST.get("date"))
        text = clean_text(request.POST.get("text", ""))
    except ValueError:
        return _back(_date_or(request.POST.get("date"), today))
    Wish.objects.create(user=request.user, date=day, text=text)
    return _back(day)


@login_required
@require_POST
def toggle(request, pk):
    """Переключить «выполнено». Чужое желание -> 404."""
    wish = get_object_or_404(Wish, pk=pk, user=request.user)
    wish.toggle()
    return _back(wish.date)


@login_required
@require_POST
def delete(request, pk):
    """Удалить желание. Чужое желание -> 404."""
    wish = get_object_or_404(Wish, pk=pk, user=request.user)
    day = wish.date
    wish.delete()
    return _back(day)
