document.getElementById("uploadForm").addEventListener("submit", async function(event) {
  event.preventDefault();
  
  const formData = new FormData();
  const fileInput = document.getElementById("file");
  const operation = document.getElementById("operation").value;
  
  formData.append("file", fileInput.files[0]);
  formData.append("operation", operation);

  // 他の設定データを追加
  if (operation === "2") {
    formData.append("resolution", prompt("解像度を選択（1: SD, 2: HD, 3: Full HD）"));
  } else if (operation === "3") {
    formData.append("aspect_ratio", prompt("アスペクト比を選択（1: 16/9, 2: 4/3, 3: 1/1, 4: 9/16）"));
  } else if (operation === "5") {
    formData.append("start_time", prompt("開始時間を秒で入力"));
    formData.append("duration", prompt("GIFの長さを秒で入力"));
  }

  // サーバーにデータ送信
  const response = await fetch("/upload", {
    method: "POST",
    body: formData,
  });

  const result = await response.json();
  const resultDiv = document.getElementById("result");

  // メッセージ表示とダウンロードリンク生成
  if (result.download_url) {
    resultDiv.innerHTML = `${result.message} <a href="${result.download_url}" download>処理済みファイルをダウンロード</a>`;
  } else {
    resultDiv.innerText = result.message;
  }
});
