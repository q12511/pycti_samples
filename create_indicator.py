#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pycti import OpenCTIApiClient
import datetime
import argparse
import traceback
import sys
from config import API_URL, API_KEY, DEFAULT_CONFIDENCE, DEFAULT_VALID_DAYS

# クライアントの初期化
client = OpenCTIApiClient(API_URL, API_KEY)


def create_indicator(name, description, pattern, pattern_type):
    """
    OpenCTIにIndicatorを作成する関数
    
    Args:
        name (str): Indicatorの名前
        description (str): Indicatorの説明
        pattern (str): STIXパターン
        pattern_type (str): パターンタイプ（通常は "stix"）
        
    Returns:
        str: 作成されたIndicatorのID、エラー時はNone
    """
    try:
        print("[+] Indicator 作成プロセスを開始します...")
        
        # 現在の日時を取得
        current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # 30日後の日時を取得（有効期限用）
        valid_until = (
            datetime.datetime.now() + datetime.timedelta(days=DEFAULT_VALID_DAYS)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Indicatorの作成
        indicator_data = {
            "name": name,
            "description": description,
            "pattern": pattern,
            "pattern_type": pattern_type,
            "valid_from": current_date,
            "valid_until": valid_until,
            "x_opencti_main_observable_type": "IPv4-Addr",  # 必須パラメータ
            "indicator_types": ["malicious-activity"],
            "confidence": DEFAULT_CONFIDENCE
        }
        
        # 新しいAPIを使用してIndicatorを作成
        indicator = client.indicator.create(**indicator_data)
        
        if indicator:
            print(f"[+] Indicator が作成されました: {indicator['id']}")
            return indicator["id"]
        else:
            print("[!] Indicatorの作成に失敗しました（APIからの応答がありません）")
            return None
        
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
        description='OpenCTIにIndicatorを作成します'
    )
    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='Indicatorの名前'
    )
    parser.add_argument(
        '--description',
        type=str,
        default='テスト用Indicator',
        help='Indicatorの説明'
    )
    parser.add_argument(
        '--pattern',
        type=str,
        required=True,
        help='STIXパターン（例: [ipv4-addr:value = \'8.8.8.8\']）'
    )
    parser.add_argument(
        '--pattern-type',
        type=str,
        default='stix',
        help='パターンタイプ（通常は "stix"）'
    )
    parser.add_argument(
        '--observable-type',
        type=str,
        default='IPv4-Addr',
        help='主要なObservableタイプ（IPv4-Addr, URL, File, など）'
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    indicator_id = create_indicator(
        args.name, args.description, args.pattern, args.pattern_type
    )
    if indicator_id:
        print(f"[+] 作成されたIndicatorID: {indicator_id}")
        ind_url = f"{API_URL}/dashboard/observations/indicators/{indicator_id}"
        print(f"[+] IndicatorURL: {ind_url}")
    else:
        print("[!] Indicatorの作成に失敗しました") 