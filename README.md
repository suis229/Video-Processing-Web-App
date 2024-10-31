# Video Processor Web App

このアプリケーションは、以前作成した Video Processor リポジトリの内容をWebアプリケーションとしたものです。
Flaskを使用して動画ファイルをアップロードし、さまざまな処理（圧縮、解像度変更、アスペクト比変更、オーディオ抽出、GIF作成）を行うことができます。

## 必要条件

- Python 3.x
- Flask
- Flask-CORS
- ffmpeg

## インストール

1. リポジトリをクローンします。

    ```bash
    git clone https://github.com/suis229/Video-Processing-Web-App.git
    cd flask-video-processing-app
    ```

2. 必要なパッケージをインストールします。
- ffmpegのインストール（MacやLinuxの場合）
  
  Ubuntu
  ```bash
  sudo apt-get install ffmpeg
  ```
  macOS
  ```bash
  brew install ffmpeg
  ```
  
- Pythonライブラリのインストール
  ```bash
  pip install Flask ffmpeg-python
  ```

## 使用方法

1. アプリケーションを起動します。

    ```bash
    python server.py
    ```

2. ブラウザで `http://localhost:9000` にアクセスします。(コンソールにリンクが表示されます）

3. ファイルをアップロードし、必要な処理を選択します。

4. リンクから変換されたファイルをダウンロードしてください。

## ファイル処理

- 動画ファイルの圧縮
- 動画の解像度変更
- 動画のアスペクト比変更
- 動画をオーディオに変換
- 時間範囲でのGIFの作成

## 注意事項

- アップロードされたファイルは `uploads` フォルダに保存され、処理されたファイルは `processed` フォルダに保存されます。

