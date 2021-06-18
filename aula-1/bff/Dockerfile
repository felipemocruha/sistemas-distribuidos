FROM python:3.8-slim-buster

RUN apt update \
	&& apt install --no-install-recommends -y git build-essential \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip && mkdir /app

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "-b", "0.0.0.0:5001", "--access-logfile", "'-'", "main:app"]
