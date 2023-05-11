FROM python:3.10

WORKDIR /GodGPT

COPY ./requirements.txt /GodGPT/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /GodGPT/requirements.txt

COPY ./godgpt.py /GodGPT/godgpt.py

COPY ./helper /GodGPT/helper/

CMD ["uvicorn", "godgpt:app", "--host", "0.0.0.0", "--port", "8000"]