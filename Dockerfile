FROM phusion/baseimage:0.11

# add code and directories
RUN mkdir /webstore
WORKDIR /webstore
RUN apt-get -y update
RUN apt-get install -y \
    nginx \
    postgresql-client \
    python3 \
    python3-pip \
    python3-venv 
COPY requirements* /webstore/
COPY django/ /webstore/django
COPY bash_scripts/ /webstore/scripts
RUN mkdir /var/log/webstore
RUN touch /var/log/webstore/webstore.log
RUN touch /var/log/webstore/webstore_bad_request_args.log
RUN chown www-data /var/log/webstore/webstore.log
RUN chown www-data /var/log/webstore/webstore_bad_request_args.log
RUN python3 -m venv /webstore/venv
RUN bash /webstore/scripts/pip_install.sh /webstore

# collect the static files
RUN bash /webstore/scripts/collect_static.sh /webstore

# configure Nginx
COPY nginx/webstore.conf /etc/nginx/sites-available/webstore.conf
RUN rm /etc/nginx/sites-enabled/*
RUN ln -s /etc/nginx/sites-available/webstore.conf /etc/nginx/sites-enabled/webstore.conf
COPY runit/nginx /etc/service/nginx
RUN chmod +x /etc/service/nginx/run

# configure uWSGI
COPY uwsgi/webstore.ini /etc/uwsgi/apps-enabled/webstore.ini
RUN mkdir -p /var/log/uwsgi
RUN touch /var/log/uwsgi/webstore.log
RUN chown www-data /var/log/uwsgi/webstore.log
COPY runit/uwsgi /etc/service/uwsgi
RUN chmod +x /etc/service/uwsgi/run

# Finishing
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EXPOSE 80
EXPOSE 443
