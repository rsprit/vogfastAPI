FROM python:3.8

WORKDIR /app
ADD requirements.txt loader.sh get_data.sh generate_db.py /app/
RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "/bin/bash" ]
CMD [ "loader.sh" ]
