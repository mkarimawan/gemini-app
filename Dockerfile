FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY app.py ./

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]