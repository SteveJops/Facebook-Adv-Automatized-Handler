FROM python:3.10-slim


WORKDIR /api

COPY req.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ./src ./api

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get install && \
    apt-get update &&\
    apt-get -y upgrade && \
    pip3 install --upgrade pip


EXPOSE 8000

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port",  "8000"]