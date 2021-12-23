FROM python:3.8
RUN mkdir /CLI_project
COPY . /CLI_project/
WORKDIR /CLI_project/
RUN rm -rf venv
RUN python3 -m venv /CLI_project/testvenv
RUN /bin/bash -c "source /CLI_project/testvenv/bin/activate"
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python", "/CLI_project/CLI_project/main.py" ]