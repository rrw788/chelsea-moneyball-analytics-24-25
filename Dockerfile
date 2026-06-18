# Menggunakan base image Python resmi yang ringan
FROM python:3.10-slim

# Mengatur working directory di dalam container
WORKDIR /app

# Menginstal tool pendukung sistem jika diperlukan
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Menyalin file requirements ke dalam container
COPY requirements.txt .

# Menginstal library Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode proyek ke dalam container
COPY . .

# Mengekspos port default yang digunakan oleh Streamlit
EXPOSE 8501

# Konfigurasi agar Streamlit berjalan lancar di dalam Docker
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Perintah utama untuk menjalankan aplikasi Streamlit saat container dimulai
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]