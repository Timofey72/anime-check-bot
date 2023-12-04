FROM python:3.11.3-slim

RUN mkdir /src
WORKDIR /src
COPY . /src

# Копирование wait-for-it.sh
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN pip install -r requirements.txt

# Запуск entrypoint.sh
ENTRYPOINT ["/src/entrypoint.sh"]