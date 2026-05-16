from celery import shared_task


@shared_task
def add_test(x, y):
    return x + y
