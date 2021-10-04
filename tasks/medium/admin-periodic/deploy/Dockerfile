FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y openssh-server cron python3-pip

RUN useradd --no-create-home --home-dir / --shell /bin/bash --uid 1000 --user-group challenge \
    && echo 'challenge:challenge' | chpasswd

RUN useradd --no-create-home --home-dir / --shell /bin/false --uid 1001 --user-group challenge-flag

# remove motd
RUN rm -rf /etc/update-motd.d/* /etc/legal

# some hacks to make crond work in read-only filesystem
RUN sed -i 's/crond.pid/crond\/pid/g' /usr/sbin/cron \
    && touch /run/crond.reboot \
    && chmod 444 /run/crond.reboot

COPY service/periodic-script /etc/cron.d/periodic-script

RUN chmod 444 /etc/cron.d/periodic-script

COPY --chown=1001:1001 service/requirements.txt service/script.py service/secret.txt /var/local/

RUN chmod 544 /var/local/script.py \
    && chmod 400 /var/local/secret.txt \
    && chmod 444 /var/local/requirements.txt

RUN pip install -r /var/local/requirements.txt

COPY start.sh /var/run/start.sh

RUN chmod 500 /var/run/start.sh

# will mount it later with tmpfs
RUN rm -rf /tmp/

ENTRYPOINT ["/var/run/start.sh"]
