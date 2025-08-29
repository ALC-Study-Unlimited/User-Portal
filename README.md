# ALC Study Unlimited - User Portal

## 概要
ALC Study Unlimited学習プラットフォームのユーザーポータルサイトです。

## ディレクトリ構成

```
/
├── *.html                    # HTMLページファイル（4ファイル）
├── css/
│   └── minified/            # 圧縮済みCSSファイル
├── css_backup/
│   └── original/            # オリジナルCSSのバックアップ
├── js/                      # JavaScriptファイル
├── images/                  # 画像ファイル
├── videos/                  # 動画・PDF資料
├── robots.txt              # 検索エンジン制御
└── toeic_learning_models.pdf # TOEIC学習モデル資料
```

## デプロイ時の注意事項

### 必要なファイル
以下のファイル・ディレクトリをそのままデプロイしてください：
- 全HTMLファイル（index.html, study-guide.html, orientation-video.html, user-guide.html）
- css/minified/ ディレクトリ
- js/ ディレクトリ
- images/ ディレクトリ
- videos/ ディレクトリ
- robots.txt
- toeic_learning_models.pdf

### CSS参照について
- 全てのHTMLファイルは圧縮版CSS（css/minified/内）を参照しています
- パフォーマンス最適化済みです

### バックアップ
- css_backup/original/ にオリジナルCSSファイルが保存されています
- 問題発生時はこちらから復元可能です

## 更新履歴
- 2025-08-29: ファイル構成を整理、圧縮版CSSへの統一化を実施