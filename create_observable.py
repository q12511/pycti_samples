#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pycti import OpenCTIApiClient
import argparse
import traceback
import sys
from config import API_URL, API_KEY

# クライアントの初期化
client = OpenCTIApiClient(API_URL, API_KEY)


def create_observable(observable_type, observable_value, description):
    """
    OpenCTIにObservableを作成する関数
    
    Args:
        observable_type (str): Observableのタイプ（IPv4-Addr, Url, など）
        observable_value (str): Observableの値
        description (str): Observableの説明
        
    Returns:
        str: 作成されたObservableのID、エラー時はNone
    """
    try:
        print(f"[+] Observable ({observable_type}) 作成プロセスを開始します...")
        
        # Observableの作成（新しい方法）
        observable_data = {}
        
        if observable_type.lower() == "ipv4-addr":
            observable_data = {
                "type": "ipv4-addr",
                "value": observable_value,
                "x_opencti_description": description
            }
        elif observable_type.lower() == "url":
            observable_data = {
                "type": "url",
                "value": observable_value,
                "x_opencti_description": description
            }
        elif observable_type.lower() == "file":
            # ファイルの場合はハッシュ値を指定
            observable_data = {
                "type": "file",
                "hashes": {
                    "md5": observable_value
                },
                "x_opencti_description": description
            }
        else:
            observable_data = {
                "type": observable_type.lower(),
                "value": observable_value,
                "x_opencti_description": description
            }
        
        # 新しいAPIを使用してObservableを作成
        observable = client.stix_cyber_observable.create(
            observableData=observable_data
        )
        
        if observable:
            print(f"[+] Observable が作成されました: {observable['id']}")
            return observable["id"]
        else:
            print("[!] Observableの作成に失敗しました（APIからの応答がありません）")
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
        description='OpenCTIにObservableを作成します'
    )
    parser.add_argument(
        '--type',
        type=str,
        default='ipv4-addr',
        help='作成するObservableのタイプ（ipv4-addr, url, file, など）'
    )
    parser.add_argument(
        '--value',
        type=str,
        required=True,
        help='Observableの値'
    )
    parser.add_argument(
        '--description',
        type=str,
        default='テスト用Observable',
        help='Observableの説明'
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    observable_id = create_observable(args.type, args.value, args.description)
    if observable_id:
        print(f"[+] 作成されたObservableID: {observable_id}")
        obs_url = f"{API_URL}/dashboard/observations/observables/{observable_id}"
        print(f"[+] ObservableURL: {obs_url}")
    else:
        print("[!] Observableの作成に失敗しました") 