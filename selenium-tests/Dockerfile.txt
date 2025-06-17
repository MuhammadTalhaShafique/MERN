FROM selenium/standalone-chrome:latest

USER root
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["pytest", "test_todo_app.py"]