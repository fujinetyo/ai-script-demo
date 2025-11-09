# ai-script-demo
Github Copilotを用いたスクリプト作成デモ用リポジトリ

## PDF ページテキスト抽出スクリプト

PDFファイルの指定ページからテキストを抽出するPythonスクリプトです。

### 必要な環境

- Python 3.8以上

### インストール方法

依存ライブラリをインストールします：

```bash
pip install -r requirements.txt
```

### 使用方法

#### 基本的な使い方

```bash
# 単一ページを抽出（標準出力）
python pdf_page_extractor.py document.pdf 1

# ページ範囲を抽出
python pdf_page_extractor.py document.pdf 1-3

# 複数ページを抽出
python pdf_page_extractor.py document.pdf 1,3,5

# 範囲と個別ページを組み合わせ
python pdf_page_extractor.py document.pdf 1-3,5,7-9

# 結果をファイルに保存
python pdf_page_extractor.py document.pdf 1-3 output.txt
```

#### コマンドライン引数

```
python pdf_page_extractor.py <PDFファイルパス> <ページ番号> [出力ファイルパス]
```

- `PDFファイルパス`: 処理対象のPDFファイルのパス（必須）
- `ページ番号`: 抽出するページ番号の指定（必須）
  - 単一ページ: `1`
  - ページ範囲: `1-3`
  - 複数ページ: `1,3,5`
  - 組み合わせ: `1-3,5,7-9`
- `出力ファイルパス`: 抽出したテキストの保存先（省略時は標準出力）

### 機能

- PDF ファイルから指定したページのテキストを抽出
- 柔軟なページ指定（単一ページ、範囲、複数ページの組み合わせ）
- 標準出力またはファイルへの出力
- 日本語を含むテキストの抽出に対応
- エラーハンドリング（ファイル未検出、不正なページ番号など）

### 制限事項

- 画像化されたPDF（スキャンPDFなど）からはテキストを抽出できません
- PDFの構造によってはテキストの順序が期待通りにならない場合があります
- パスワード保護されたPDFには対応していません
- フォント埋め込みがされていないPDFでは文字化けが発生する可能性があります
