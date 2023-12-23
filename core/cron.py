# myapp/cron.py
from userauths.models import Transaction
from django.utils import timezone

def update_total_invested_job():
    # Get the current date and time
    current_time = timezone.now()

    # Your logic to calculate and update total_invested
    transactions = Transaction.objects.filter(confirmed=True)

    for transaction in transactions:
        # Calculate the time difference between the current time and the transaction timestamp
        time_difference = current_time - transaction.timestamp

        # Check if the interval condition is met
        if (
            (transaction.interval == 'daily' and time_difference.days >= 1) or
            (transaction.interval == 'weekly' and time_difference.days >= 7) or
            (transaction.interval == 'monthly' and time_difference.days >= 30)
        ):
            # Calculate the amount to be added based on your formula
            amount_to_add = transaction.percentage_return * transaction.amount / 100

            # Update the user's total_invested field
            transaction.user.total_invested += amount_to_add
            transaction.user.save()
