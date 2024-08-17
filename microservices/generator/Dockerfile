FROM python:3.12

WORKDIR /code

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH /code

COPY . /code
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN ["chmod", "+x", "/code/run.sh"]
CMD ["run.sh"]