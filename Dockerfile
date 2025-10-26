FROM python:3.11-slim

WORKDIR /app

# копіюємо всі файли проєкту
COPY . /app

# встановлюємо залежності та пакет
RUN pip install --upgrade pip && \
    pip install .

# команда за замовчуванням
ENTRYPOINT ["my-sort"]