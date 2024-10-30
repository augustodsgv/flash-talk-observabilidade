curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"stress_time":"5", "cores_n":"3"}' \
    localhost:8000/cpu-stress