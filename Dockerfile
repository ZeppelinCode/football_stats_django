FROM python:3.7.2-alpine3.9

ADD requirements.txt /requirements.txt
ADD docker_build_scripts/install_dependencies.sh /install_dependencies.sh

RUN apk add --no-cache --virtual .build-deps \
  ca-certificates gcc postgresql-dev linux-headers libffi-dev \
  musl-dev zlib-dev

ADD football_stats /football_stats
ADD docker_build_scripts/run_django.sh /run_django.sh
ADD very_secure_prod_settings.py /football_stats/football_stats/local_settings.py

CMD ["sh", "/run_django.sh"]