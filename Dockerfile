FROM python:3.9-buster
WORKDIR /scheduler
COPY . .
RUN pip install -r requirements.txt
RUN python __main__.py