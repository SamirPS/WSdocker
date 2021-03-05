FROM python

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD . /var/www/
RUN pip install -r lib.txt

EXPOSE 9999

CMD [ "python", "api.py"]