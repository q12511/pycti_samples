#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pycti import OpenCTIApiClient
import datetime
import argparse
import traceback
import sys
from config import API_URL, API_KEY, DEFAULT_CONFIDENCE

# クライアントの初期化
client = OpenCTIApiClient(API_URL, API_KEY)

def create_report(report_name, description):
    """
    OpenCTIにレポートを作成する関数
    
    Args:
        report_name (str): レポートの名前
        description (str): レポートの説明
        
    Returns:
        str: 作成されたレポートのID、エラー時はNone
    """
    try:
        print("[+] OpenCTIレポート作成プロセスを開始します...")
        
        # 現在の日時を取得
        current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # レポートの作成
        report = client.report.create(
            name=report_name,
            description=description,
            published=current_date,
            report_types=["threat-report"],
            confidence=DEFAULT_CONFIDENCE
        )
        
        print(f"[+] レポートが作成されました: {report['id']}")
        return report["id"]
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"[!] エラーが発生しました (行 {line_number}): {str(e)}")
        print("[!] 詳細なエラー情報:")
        traceback.print_exc()
        return None

def parse_args():
    """コマンドライン引数をパースする関数"""
    parser = argparse.ArgumentParser(
        description='OpenCTIにレポートを作成します'
    )
    parser.add_argument(
        '--name',
        type=str,
        default='テスト分析レポート',
        help='作成するレポートの名前'
    )
    parser.add_argument(
        '--description',
        type=str,
        default='このレポートはテスト用です。',
        help='レポートの説明'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    report_id = create_report(args.name, args.description)
    if report_id:
        print(f"[+] 作成されたレポートID: {report_id}")
        print(f"[+] レポートURL: {API_URL}/dashboard/analysis/reports/{report_id}")
    else:
        print("[!] レポートの作成に失敗しました") 