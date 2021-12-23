FROM python: 3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app_folder/

RUN pip install pipenv
COPY Pipfile Pipfile.lock /app_folder/
RUN pipenv install --system

COPY . /app_folder/
ENTRYPOINT ['python']
CMD ['run.py']
