FROM python:3.9

WORKDIR /app

COPY . .

RUN npm install
RUN pip install --no-cache-dir -r requirements.txt

# docker build -t myHHUApp .
# docker run -it myHHUApp bash