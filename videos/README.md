# 動画ファイル保存ディレクトリ

このディレクトリには、オリエンテーション動画および関連資料を保存します。

## ファイル構成

### 必要なファイル

1. **orientation.mp4** (または .webm)
   - オリエンテーション動画本体
   - 推奨フォーマット: MP4 (H.264コーデック)
   - 推奨解像度: 1920x1080 (Full HD) または 1280x720 (HD)
   - 推奨ビットレート: 5-10 Mbps
   - 動画の長さ: 約20-25分

2. **orientation-guide.pdf**
   - オリエンテーション動画の内容をまとめた資料
   - ユーザーがダウンロードして印刷できる形式
   - 動画の要点、手順、スクリーンショットなどを含む

## アップロード方法

### 動画ファイルのアップロード

```bash
# 動画ファイルをこのディレクトリにコピー
cp /path/to/your/orientation.mp4 /home/user/webapp/videos/

# WebM形式も用意する場合（ブラウザ互換性向上のため）
cp /path/to/your/orientation.webm /home/user/webapp/videos/
```

### PDF資料のアップロード

```bash
cp /path/to/your/orientation-guide.pdf /home/user/webapp/videos/
```

## 動画ファイルの準備

### 推奨される動画の内容構成

1. **0:00-2:00** - イントロダクション
2. **2:00-5:00** - ログイン方法とアカウント設定
3. **5:00-8:00** - 学習ツールの概要
4. **8:00-12:00** - boocoの使い方
5. **12:00-15:00** - TALKING MARATHONの使い方
6. **15:00-18:00** - オンラインセミナー機能
7. **18:00-20:00** - 学習進捗の管理
8. **20:00-22:00** - FAQ・トラブルシューティング

### 動画編集のポイント

- 字幕を付けることを推奨
- チャプターマーカーを設定
- 音声は明瞭に
- 画面録画は高解像度で

## ファイルサイズの考慮事項

- GitHubのファイルサイズ制限: 100MB
- 大きな動画ファイルの場合は、Git LFSの使用を検討
- または外部ホスティングサービス（YouTube、Vimeo等）の利用も可能

## Git LFSの設定（大きなファイルの場合）

```bash
# Git LFSをインストール
git lfs install

# 動画ファイルをLFSで管理
git lfs track "*.mp4"
git lfs track "*.webm"
git lfs track "*.pdf"

# .gitattributesファイルをコミット
git add .gitattributes
git commit -m "Add Git LFS tracking for video files"
```

## 注意事項

- 動画ファイルは著作権に配慮して作成・使用してください
- 個人情報が含まれないよう注意してください
- 定期的にバックアップを取ることを推奨します