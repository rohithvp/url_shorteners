From python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt
CMD ["python3","/app/main.py"]