#FROM python:3.9-slim
#
#WORKDIR /app
#
#COPY requirements.txt /app/
#RUN pip install --no-cache-dir --upgrade pip
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY . /app/
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.9-slim AS builder

WORKDIR /app

# 의존성 설치 최적화
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 소스 복사 (나중에 진행해서 캐시 최적화)
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
