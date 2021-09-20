from jasmine.etl.app import celery_app


@celery_app.task
def foo(a, b):
    print(a, b)
    return a + b
