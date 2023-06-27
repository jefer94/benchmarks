# cd server/encryptions/int-hmac-sha512

# source .venv/bin/activate;

export WORKERS=$(python3 ./count_cpus.py);

rm results.md

close-ports() {
    fuser -k 3000/tcp
    fuser -k 4000/tcp
    fuser -k 5000/tcp
}

killer() {
    sleep 15
    close-ports
    deactivate
}

setup-python() {
    cd $1
    python3 -m venv .venv;
    source .venv/bin/activate;
    touch requirements.txt;
    pip3 install -r requirements.txt;
}

serve-sanic() {
    close-ports
    setup-python $1

    sanic service-1:app --host=0.0.0.0 --port=3000 --workers=$WORKERS & \
        sanic service-2:app --host=0.0.0.0 --port=4000 --workers=$WORKERS & \
        sanic client:app --host=0.0.0.0 --port=5000 --workers=$WORKERS & \
        killer

    cd ../../..
}

setup-go() {
    cd $1
    go mod tidy
}

serve-go() {
    close-ports
    setup-go $1

    PORT=3000 go run service1/main.go & \
        PORT=4000 go run service2/main.go & \
        PORT=5000 go run client/main.go & \
        killer

    cd ../../..
}

serve-go server/encryptions/nothing
serve-go server/encryptions/int-hmac-sha256
serve-go server/encryptions/int-hmac-sha512
serve-go server/encryptions/int-ed25519
serve-go server/encryptions/int-jwt-ed25519
export POSTGRES_HOST=""
serve-go server/encryptions/int-postgres-token

test with external db
export POSTGRES_HOST="xyz.preview.app.github.dev"
serve-go server/encryptions/int-postgres-token

serve-go server/encryptions/int-redis-token

# test with external db (actually not working)
# export REDIS_HOST="xyz.preview.app.github.dev"
# serve-go server/encryptions/int-redis-token

serve-go server/encryptions/int-mongo-token

