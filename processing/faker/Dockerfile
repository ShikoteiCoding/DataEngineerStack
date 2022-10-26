FROM python:3.10

WORKDIR /code

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH /code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY wait-for-collector.sh wait-for-collector.sh
RUN ["chmod", "+x", "/code/wait-for-collector.sh"]
CMD ["./wait-for-collector.sh", "collector", "python3", "app/app-generator.py"]