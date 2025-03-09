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


def create_report_with_relationships(report_name, ip_value, url_value):
    """
    レポートを作成し、Observableとそれに対応するIndicatorを作成し、
    それらの関係性も含めるメイン関数

    Args:
        report_name (str): レポートの名前
        ip_value (str): IPアドレスの値
        url_value (str): URLの値

    Returns:
        str: 作成されたレポートのID、エラー時はNone
    """
    try:
        print("[+] OpenCTIレポート作成プロセスを開始します...")
        
        # 現在の日時を取得
        current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # レポートに追加するオブジェクトの参照を保持するリスト
        object_refs = []
        observable_refs = []
        
        # レポートの作成
        report = client.report.create(
            name=report_name,
            description="このレポートはマルウェアの分析結果を含みます。",
            published=current_date,
            report_types=["threat-report"],
            confidence=DEFAULT_CONFIDENCE
        )
        
        print(f"[+] レポートが作成されました: {report['id']}")
        
        # Observable (IP) の作成
        ip_observable_data = {
            "type": "ipv4-addr",
            "value": ip_value,
            "x_opencti_description": "悪意のあるIPアドレス"
        }
        
        ip_observable = client.stix_cyber_observable.create(
            observableData=ip_observable_data
        )
        
        if not ip_observable:
            print("[!] IP Observableの作成に失敗しました")
            return report["id"]
            
        print(f"[+] IP Observable が作成されました: {ip_observable['id']}")
        observable_refs.append(ip_observable["id"])
        
        # Observable (URL) の作成
        url_observable_data = {
            "type": "url",
            "value": url_value,
            "x_opencti_description": "悪意のあるURL"
        }
        
        url_observable = client.stix_cyber_observable.create(
            observableData=url_observable_data
        )
        
        if not url_observable:
            print("[!] URL Observableの作成に失敗しました")
            return report["id"]
            
        print(f"[+] URL Observable が作成されました: {url_observable['id']}")
        observable_refs.append(url_observable["id"])
        
        # IP Observable に対応する Indicator の作成
        valid_until = (
            datetime.datetime.now() + datetime.timedelta(days=DEFAULT_VALID_DAYS)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        ip_indicator_data = {
            "name": f"悪意のあるIPアドレス指標: {ip_value}",
            "description": f"悪意のあるIPアドレス {ip_value} を示す指標",
            "pattern": f"[ipv4-addr:value = '{ip_value}']",
            "pattern_type": "stix",
            "valid_from": current_date,
            "valid_until": valid_until,
            "x_opencti_main_observable_type": "IPv4-Addr",
            "indicator_types": ["malicious-activity"],
            "confidence": DEFAULT_CONFIDENCE
        }
        
        ip_indicator = client.indicator.create(**ip_indicator_data)
        
        if not ip_indicator:
            print("[!] IP Indicatorの作成に失敗しました")
            return report["id"]
            
        print(f"[+] IP Indicator が作成されました: {ip_indicator['id']}")
        object_refs.append(ip_indicator["id"])
        
        # URL Observable に対応する Indicator の作成
        url_indicator_data = {
            "name": f"悪意のあるURL指標: {url_value}",
            "description": f"悪意のあるURL {url_value} を示す指標",
            "pattern": f"[url:value = '{url_value}']",
            "pattern_type": "stix",
            "valid_from": current_date,
            "valid_until": valid_until,
            "x_opencti_main_observable_type": "Url",
            "indicator_types": ["malicious-activity"],
            "confidence": DEFAULT_CONFIDENCE
        }
        
        url_indicator = client.indicator.create(**url_indicator_data)
        
        if not url_indicator:
            print("[!] URL Indicatorの作成に失敗しました")
            return report["id"]
            
        print(f"[+] URL Indicator が作成されました: {url_indicator['id']}")
        object_refs.append(url_indicator["id"])
        
        # IP Observable と IP Indicator の関係性を作成
        try:
            ip_relationship = client.stix_core_relationship.create(
                relationship_type="based-on",
                fromId=ip_indicator["id"],
                toId=ip_observable["id"],
                description="この指標は観測されたIPアドレスに基づいています"
            )
            print("[+] IP Observable と Indicator の関係性が作成されました")
            object_refs.append(ip_relationship["id"])
        except Exception as e:
            print(f"[!] IP Observable と Indicator の関係性作成に失敗しました: {str(e)}")
        
        # URL Observable と URL Indicator の関係性を作成
        try:
            url_relationship = client.stix_core_relationship.create(
                relationship_type="based-on",
                fromId=url_indicator["id"],
                toId=url_observable["id"],
                description="この指標は観測されたURLに基づいています"
            )
            print("[+] URL Observable と Indicator の関係性が作成されました")
            object_refs.append(url_relationship["id"])
        except Exception as e:
            print(f"[!] URL Observable と Indicator の関係性作成に失敗しました: {str(e)}")
        
        # レポートにオブジェクトを追加
        for object_ref in object_refs:
            try:
                client.report.add_stix_object_or_stix_relationship(
                    id=report["id"],
                    stixObjectOrStixRelationshipId=object_ref
                )
                print(f"[+] オブジェクト {object_ref} をレポートに追加しました")
            except Exception as e:
                print(f"[!] オブジェクト {object_ref} のレポートへの追加に失敗しました: {str(e)}")
        
        # レポートにObservableを追加
        for observable_ref in observable_refs:
            try:
                client.report.add_stix_object_or_stix_relationship(
                    id=report["id"],
                    stixObjectOrStixRelationshipId=observable_ref
                )
                print(f"[+] Observable {observable_ref} をレポートに追加しました")
            except Exception as e:
                msg = f"[!] Observable {observable_ref} のレポートへの追加に失敗: "
                print(f"{msg}{str(e)}")
        
        print("[+] プロセスが正常に完了しました")
        
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
        description='OpenCTIにレポート、Observable、Indicatorを作成します'
    )
    parser.add_argument(
        '--report-name',
        type=str,
        default='マルウェア分析レポート',
        help='作成するレポートの名前'
    )
    parser.add_argument(
        '--ip',
        type=str,
        default='8.8.8.8',
        help='作成するIP Observableの値'
    )
    parser.add_argument(
        '--url',
        type=str,
        default='https://malicious-example.com',
        help='作成するURL Observableの値'
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    report_id = create_report_with_relationships(
        args.report_name, args.ip, args.url
    )
    if report_id:
        print(f"[+] 作成されたレポートID: {report_id}")
        print(f"[+] レポートURL: {API_URL}/dashboard/analysis/reports/{report_id}")
    else:
        print("[!] レポートの作成に失敗しました") 