FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY requirements.txt ./
RUN apt-get install gcc libffi-dev && pip install --no-cache-dir -r requirements.txt
COPY . ./
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]