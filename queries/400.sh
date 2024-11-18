curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"stress_time":"1", "bytes_n":"600"}' \
    localhost:8000/disk-test