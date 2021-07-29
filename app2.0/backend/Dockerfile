FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash todo
USER todo

EXPOSE 4000

ENTRYPOINT ["python","index.py"]