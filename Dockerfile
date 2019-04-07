FROM python:3.7
EXPOSE 8000

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
RUN mkdir /app/tmp
ENV DATABASE_URL postgres://ad@db/ad
ENV SECRET_KEY ''
ENV DJANGO_ENV 'dev'
ENV MAILGUN_KEY ''
ENV MAILGUN_DOMAIN ''
ENV DEFAULT_FROM_EMAIL ''
ENV ALLOWED_HOSTS "sos-laveries.bde-insa-lyon.fr"
ENV RECAPTCHA_PUBLIC_KEY ''
ENV RECAPTCHA_PRIVATE_KEY ''
ENV EMAIL_RESP_SERVICES 'services@bde-insa-lyon.fr'
ENV EMAIL_RESP_LAVERIE ''
ENV GOOGLE_ANALYTICS_PROPERTY_ID ''
RUN chmod +x bash/run-prod.sh
CMD bash/run-prod.sh