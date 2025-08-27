# Image Python 3.10 (compatible scikit-learn 1.0.2)
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY . .

# Mettre à jour pip et installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port FastAPI
EXPOSE 8000

# Lancer FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
