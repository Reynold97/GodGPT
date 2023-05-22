FROM python:3.10

WORKDIR /GodGPT

COPY ./requirements.txt /GodGPT/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /GodGPT/requirements.txt

COPY ./helper /GodGPT/helper/

COPY ./god_agent /GodGPT/god_agent/

COPY ./godgpt.py /GodGPT/godgpt.py

CMD ["uvicorn", "godgpt:app", "--host", "0.0.0.0", "--port", "80"]