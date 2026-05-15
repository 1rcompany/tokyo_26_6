# Tokyo Trip Streamlit

這是一個用 Streamlit 做的日本旅行規劃小網站，可以輸入住宿、航班、日期、想去的地方，以及逐日行程。

## 在自己電腦執行

```bash
pip install -r requirements.txt
streamlit run app.py
```

開啟後通常會看到這個網址：

```text
http://localhost:8501
```

如果 8501 已經被占用，可以改用：

```bash
streamlit run app.py --server.port 8502
```

## 變成大家都能開的網址

最簡單的方式是用 Streamlit Community Cloud：

1. 建一個 GitHub repository。
2. 把這個資料夾裡的檔案上傳到 repository。
3. 到 https://share.streamlit.io/ 登入 GitHub。
4. 選剛剛的 repository。
5. Main file path 填：

```text
app.py
```

6. 按 Deploy。

部署完成後會得到一個像這樣的公開網址：

```text
https://your-app-name.streamlit.app
```

之後只要把這個網址傳給別人，大家就能打開網站。

## 專案檔案

- `app.py`: 網站主程式
- `requirements.txt`: 部署時需要安裝的套件
- `README.md`: 說明文件
