# Use uma imagem base com Python
FROM python:3.8-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie apenas os arquivos necessários
COPY . .

# Instale as dependências da aplicação
RUN pip install -r requiriments.txt

# Comando de execução da sua aplicação
CMD ["python3", "data_processing.py"]

