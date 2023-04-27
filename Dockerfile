FROM python:3.10

WORKDIR /godgptAPI

COPY ./requirements.txt /godgptAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /godgptAPI/requirements.txt

COPY ./godgptapi.py /godgptAPI/

CMD ["uvicorn", "godgptapi:app", "--host", "0.0.0.0", "--port", "80"]