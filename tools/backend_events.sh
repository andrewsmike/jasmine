# Note: You may need to set your mysql client's default timezone.

INTERVAL="5 MINUTE"

for DB in web test
do
    echo "SELECT * FROM jasmine_${DB}.backend_events WHERE created_time > DATE_SUB(NOW(), INTERVAL $INTERVAL) ORDER BY created_time ASC\G" | \
        mysql \
            --user=jasmine_web_su \
            --password=password \
            --host=127.0.0.1 \
            --port=3305 \
            jasmine_web
done
