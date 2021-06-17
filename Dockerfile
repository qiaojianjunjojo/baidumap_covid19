# Use the Python3.6 image
# 使用python 3.7作為基礎鏡像
FROM apibase:V1.1

LABEL maintainer="jojo"


# Set the working directory to /app
# 設置工作目錄，作用是啟動容器後直接進入的目錄名稱
WORKDIR /app

# Copy the current directory contents into the container at /app
# . 表示和Dockerfile同級的目錄
# 該句將目前的目錄下的檔複製到docker鏡像的/app目錄中
ADD . /app

# Install the dependencies
# 安裝相關依賴
# RUN pip install -r requirements.txt

EXPOSE 5000

#print()時在控制台正常顯示中文
ENV PYTHONIOENCODING=utf-8

# run the command to start uWSGI
# 容器啟動後要執行的命令 -> 啟動uWSGI伺服器
# CMD ["uwsgi", "uwsgi.ini"]
