echo "export CELERY_BROKER_URL=redis://localhost:6379/0" >> ~/.bashrc
source ~/.bashrc

apt-get install -y python3 python3-pip python3-dev redis-server pgadmin3 postgresql postgresql-contrib gcc g++ git wget curl vim libpq-dev yarn sudo

service postgresql start
sudo -u postgres createuser ubuntu
sudo -u postgres createdb clotudy_backend --owner=ubuntu

# sudo -i -u postgres
# psql
# ALTER USER postgres WITH PASSWORD 'new_password';
# \q

