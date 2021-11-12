FROM registry.redhat.io/ubi8/python-36

RUN pip3 install flask flask-restful
COPY . /opt/app-root/src
ENV FLASK_APP app
ENV FLASK_ENV development

EXPOSE 5000

USER 1000

CMD flask run --host=0.0.0.0
