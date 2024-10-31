from flask import Flask, request, jsonify, send_file, render_template, url_for
import os
import ffmpeg

app = Flask(__name__)

# 必要なディレクトリを作成
if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("processed"):
    os.makedirs("processed")

# ルートエンドポイントでindex.htmlを表示
@app.route('/')
def index():
    return render_template("index.html")

# アップロードとファイル処理用エンドポイント
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    operation = int(request.form.get('operation'))
    resolution = request.form.get('resolution')
    aspect_ratio = request.form.get('aspect_ratio')
    start_time = request.form.get('start_time')
    duration = request.form.get('duration')

    # ファイルを保存
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # 操作ごとの処理
    processed_file_path = None
    media_type = os.path.splitext(file.filename)[1]
    
    if operation == 1:
        processed_file_path = compress(media_type, file_path)
    elif operation == 2 and resolution:
        processed_file_path = change_resolution(media_type, file_path, resolution)
    elif operation == 3 and aspect_ratio:
        processed_file_path = change_aspect_ratio(media_type, file_path, aspect_ratio)
    elif operation == 4:
        output_mp3_file_path = os.path.join("processed", os.path.splitext(file.filename)[0] + ".mp3")
        processed_file_path = convert_to_audio(file_path, output_mp3_file_path)
    elif operation == 5 and start_time and duration:
        output_gif_file_path = os.path.join("processed", os.path.splitext(file.filename)[0] + ".gif")
        processed_file_path = create_gif(file_path, output_gif_file_path, start_time, duration)
    else:
        return jsonify({"message": "操作が無効です"})

    # ダウンロード用のURLを生成
    download_url = url_for('download_file', filename=os.path.basename(processed_file_path))
    return jsonify({"message": "ファイル処理が完了しました", "download_url": download_url})

# ダウンロードエンドポイント
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join("processed", filename), as_attachment=True)

# 動画ファイルの圧縮
def compress(media_type, output_file_path):
    temp_output = 'temp_compressed' + media_type
    if os.path.exists(temp_output):
        os.remove(temp_output)
    ffmpeg.input(output_file_path).output(temp_output, video_bitrate='1M').run()
    os.replace(temp_output, output_file_path)
    print(f"圧縮された動画は {output_file_path} に保存されました")
    return output_file_path

# 動画の解像度変更
def change_resolution(media_type, output_file_path, resolution):
    if resolution == "1":
        width, height = 640, 480
    elif resolution == "2":
        width, height = 1280, 720
    elif resolution == "3":
        width, height = 1920, 1080
    else:
        print("resolutionが1~3の数値以外です")
        return output_file_path
    
    temp_output = 'temp_resolution' + media_type
    if os.path.exists(temp_output):
        os.remove(temp_output)
    ffmpeg.input(output_file_path).output(temp_output, vf=f'scale={width}:{height}').run()
    os.replace(temp_output, output_file_path)
    print(f"解像度は {width}x{height} に変換され、 {output_file_path} へ保存されました")
    return output_file_path

# 動画のアスペクト比変更
def change_aspect_ratio(media_type, output_file_path, aspect_ratio_num):
    temp_output = 'temp_aspect_ratio' + media_type
    if os.path.exists(temp_output):
        os.remove(temp_output)
    aspect_ratio_map = {"1": "16/9", "2": "4/3", "3": "1/1", "4": "9/16"}
    aspect_ratio = aspect_ratio_map.get(aspect_ratio_num, None)
    if not aspect_ratio:
        print("aspect_ratio_numが1~4以外です")
        return output_file_path
    
    ffmpeg.input(output_file_path).output(temp_output, vf=f'setdar={aspect_ratio}').run()
    os.replace(temp_output, output_file_path)
    print(f"アスペクト比は {aspect_ratio} へ変換され、 {output_file_path} に保存されました")
    return output_file_path

# 動画をオーディオに変換
def convert_to_audio(output_file_path, output_mp3_file_path):
    temp_output = 'temp_audio.mp3'
    if os.path.exists(temp_output):
        os.remove(temp_output)
    ffmpeg.input(output_file_path).output(output_mp3_file_path, acodec='mp3').run()
    os.remove(output_file_path)
    print(f"オーディオが抽出され、 {output_mp3_file_path} へ保存されました")
    return output_mp3_file_path

# 時間範囲でのGIFの作成
def create_gif(output_file_path, output_gif_file_path, start_time, duration):
    temp_output = 'temp.gif'
    if os.path.exists(temp_output):
        os.remove(temp_output)
    ffmpeg.input(output_file_path, ss=start_time, t=duration).output(output_gif_file_path, vf='fps=10', loop=0).run()
    print(f"{start_time} から {duration} 秒間のGIFが作成され、 {output_gif_file_path} に保存されました")
    return output_gif_file_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)