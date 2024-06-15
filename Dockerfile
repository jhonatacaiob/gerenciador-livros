FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir hatch==1.12.0;\
    pip install --no-cache-dir --upgrade .

CMD ["fastapi", "run", "./src/gerenciador_livros/app.py"]
