#!/bin/bash
function wait_for_celery {
    until timeout 10 celery -A jasmine.etl.app inspect ping; do
        echo "Waiting for celery workers..."
    done
}

function launch_flower {
    wait_for_celery

    echo 'Starting flower.'
    celery -A jasmine.etl.app flower
}
function launch_celery_beat {
    wait_for_celery

    echo "Starting celery beat."
    celery -A jasmine.etl.app beat
}

# Launch celery, repeating task scheduler (celery beat), and celery monitoring app (flower).
celery -A jasmine.etl.app worker -l INFO & \
    launch_flower & \
    launch_celery_beat

