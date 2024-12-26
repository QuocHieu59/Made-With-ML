FROM python:3.10.9

WORKDIR /usr/src

COPY . .

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# (Optional) Install pre-commit hooks
RUN pre-commit install && \
    pre-commit autoupdate

# Set the PythonPath environment variable (optional, only if needed)
ENV PYTHONPATH=$PYTHONPATH:/app

CMD ["python", "madewithml/serve.py"]
