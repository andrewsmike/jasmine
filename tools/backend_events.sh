# Note: You may need to set your mysql client's default timezone.

INTERVAL="30 MINUTE"
DB="test"


echo "SELECT * FROM jasmine_${DB}.backend_events WHERE created_time > DATE_SUB(NOW(), INTERVAL $INTERVAL)\G" | \
    mysql \
    --user=root \
    --password=root \
    --host=127.0.0.1 \
    --port=3305 \
    jasmine_web
