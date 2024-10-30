curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"stress_time":"20", "bytes_n":"6000000000"}' \
    localhost:8000/memory-stress