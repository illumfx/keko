FROM python:3.9
WORKDIR /keko
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "runner.py"]