redis-server &
export CELERY_BROKER_URL=redis://localhost:6379/0
service postgresql start
