# syntax=docker/dockerfile:1

FROM python:3.12-slim-bullseye

WORKDIR /bakingapp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping netcat

#Copy rest of the files into workdir
COPY . .

EXPOSE 3000

#RUN pip3 install gunicorn
#CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=3000" ]
