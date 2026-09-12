from django.db.models import QuerySet
from django.db import transaction

from db.models import Order
from db.models import Ticket
from db.models import User


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: str | None = None
) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            order=order)
    if date:
        order.created_at = date
        order.save()
    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username is not None:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user.id)
    return Order.objects.all()
