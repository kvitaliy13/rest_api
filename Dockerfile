FROM python:slim

COPY requirements-docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /src
WORKDIR /src
VOLUME env

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]