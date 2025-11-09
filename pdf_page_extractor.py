#!/usr/bin/env python3
"""
PDFファイルの指定ページからテキストを抽出するスクリプト

使用方法:
    python pdf_page_extractor.py <PDFファイルパス> <ページ番号> [出力ファイルパス]

例:
    python pdf_page_extractor.py document.pdf 1
    python pdf_page_extractor.py document.pdf 1-3
    python pdf_page_extractor.py document.pdf 1,3,5
    python pdf_page_extractor.py document.pdf 1-3 output.txt
"""

import sys
import argparse
from pathlib import Path
from pypdf import PdfReader


def parse_page_numbers(page_spec: str, total_pages: int) -> list[int]:
    """
    ページ指定文字列を解析してページ番号のリストを返す
    
    Args:
        page_spec: ページ指定文字列（例: "1", "1-3", "1,3,5", "1-3,5-7"）
        total_pages: PDFの総ページ数
    
    Returns:
        ページ番号のリスト（0始まりのインデックス）
    
    Raises:
        ValueError: ページ指定が不正な場合
    """
    pages = set()
    
    for part in page_spec.split(','):
        part = part.strip()
        if '-' in part:
            # 範囲指定（例: "1-3"）
            start, end = part.split('-', 1)
            start = int(start.strip())
            end = int(end.strip())
            
            if start < 1 or end < 1:
                raise ValueError(f"ページ番号は1以上である必要があります: {part}")
            if start > end:
                raise ValueError(f"開始ページが終了ページより大きいです: {part}")
            if end > total_pages:
                raise ValueError(f"ページ番号がPDFの総ページ数（{total_pages}）を超えています: {end}")
            
            pages.update(range(start - 1, end))
        else:
            # 単一ページ指定（例: "5"）
            page_num = int(part)
            if page_num < 1:
                raise ValueError(f"ページ番号は1以上である必要があります: {page_num}")
            if page_num > total_pages:
                raise ValueError(f"ページ番号がPDFの総ページ数（{total_pages}）を超えています: {page_num}")
            
            pages.add(page_num - 1)
    
    return sorted(list(pages))


def extract_text_from_pages(pdf_path: str, page_numbers: list[int]) -> str:
    """
    PDFファイルの指定ページからテキストを抽出する
    
    Args:
        pdf_path: PDFファイルのパス
        page_numbers: 抽出するページ番号のリスト（0始まりのインデックス）
    
    Returns:
        抽出されたテキスト
    
    Raises:
        FileNotFoundError: PDFファイルが見つからない場合
        Exception: PDF読み込みエラー
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        raise Exception(f"PDFファイルの読み込みに失敗しました: {e}")
    
    extracted_text = []
    for page_num in page_numbers:
        page = reader.pages[page_num]
        text = page.extract_text()
        extracted_text.append(f"=== ページ {page_num + 1} ===\n{text}\n")
    
    return "\n".join(extracted_text)


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="PDFファイルの指定ページからテキストを抽出します",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  単一ページを抽出:
    %(prog)s document.pdf 1
  
  ページ範囲を抽出:
    %(prog)s document.pdf 1-3
  
  複数ページを抽出:
    %(prog)s document.pdf 1,3,5
  
  範囲と個別ページを組み合わせ:
    %(prog)s document.pdf 1-3,5,7-9
  
  結果をファイルに保存:
    %(prog)s document.pdf 1-3 output.txt
        """
    )
    
    parser.add_argument(
        'pdf_path',
        help='PDFファイルのパス'
    )
    parser.add_argument(
        'pages',
        help='抽出するページ番号（例: 1, 1-3, 1,3,5, 1-3,5-7）'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        default=None,
        help='出力ファイルのパス（省略時は標準出力）'
    )
    
    args = parser.parse_args()
    
    try:
        # PDFファイルを開いて総ページ数を取得
        reader = PdfReader(args.pdf_path)
        total_pages = len(reader.pages)
        
        # ページ番号を解析
        page_numbers = parse_page_numbers(args.pages, total_pages)
        
        if not page_numbers:
            print("エラー: 抽出するページが指定されていません", file=sys.stderr)
            sys.exit(1)
        
        # テキストを抽出
        extracted_text = extract_text_from_pages(args.pdf_path, page_numbers)
        
        # 結果を出力
        if args.output_file:
            output_path = Path(args.output_file)
            output_path.write_text(extracted_text, encoding='utf-8')
            print(f"テキストを {args.output_file} に保存しました")
            print(f"抽出したページ: {', '.join(str(p + 1) for p in page_numbers)}")
        else:
            print(extracted_text)
    
    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
