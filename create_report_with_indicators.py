#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import argparse
from pycti import OpenCTIApiClient

# OpenCTI APIの設定
API_URL = "https://demo.opencti.io"  # OpenCTIのURLを設定
API_KEY = "e1ba28b4-4118-4581-9acf-6f1c42456c72"  # OpenCTIのAPIキーを設定

# クライアントの初期化
client = OpenCTIApiClient(API_URL, API_KEY)

# 現在の日時を取得
current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def create_report_with_indicators(report_name, ip_value, url_value):
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
        
        # TLP:AMBERのマーキング定義を取得
        marking_definitions = client.marking_definition.list(
            filters={
                "mode": "and",
                "filters": [
                    {"key": "definition_type", "values": ["TLP"]},
                    {"key": "definition", "values": ["TLP:AMBER"]}
                ],
                "filterGroups": []
            }
        )
        
        if not marking_definitions or len(marking_definitions["entities"]) == 0:
            print("[!] TLP:AMBERのマーキング定義が見つかりませんでした")
            # TLP:WHITEを試す
            marking_definitions = client.marking_definition.list(
                filters={
                    "mode": "and",
                    "filters": [
                        {"key": "definition_type", "values": ["TLP"]},
                        {"key": "definition", "values": ["TLP:WHITE"]}
                    ],
                    "filterGroups": []
                }
            )
            
            if not marking_definitions or len(marking_definitions["entities"]) == 0:
                print("[!] TLP:WHITEのマーキング定義も見つかりませんでした")
                # 任意のマーキング定義を取得
                marking_definitions = client.marking_definition.list(first=1)
                
                if not marking_definitions or len(marking_definitions["entities"]) == 0:
                    print("[!] マーキング定義が見つかりませんでした")
                    return None
        
        marking_definition = marking_definitions["entities"][0]
        mark_def_id = marking_definition["id"]
        mark_def_name = marking_definition["definition"]
        print(f"[*] 使用するマーキング定義: {mark_def_name} ({mark_def_id})")
            
        # 内部アイデンティティを取得
        identities = client.identity.list(
            filters={
                "mode": "and",
                "filters": [
                    {"key": "name", "values": ["ANSSI"]}
                ],
                "filterGroups": []
            }
        )
        
        if not identities or len(identities["entities"]) == 0:
            print("[!] アイデンティティが見つかりませんでした")
            # デフォルトのアイデンティティを使用
            print("[*] デフォルトのアイデンティティを使用します")
            identities = client.identity.list(first=1)
            if not identities or len(identities["entities"]) == 0:
                print("[!] デフォルトのアイデンティティも見つかりませんでした")
                return None
            
        identity = identities["entities"][0]
        identity_id = identity["id"]
        print(f"[*] 使用するアイデンティティ: {identity['name']} ({identity_id})")
        
        # レポートの作成
        report = client.report.create(
            name=report_name,
            description="このレポートはマルウェアの分析結果を含みます。",
            published=current_date,
            report_types=["threat-report"],
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        print(f"[+] レポートが作成されました: {report['id']}")
        
        # Observable (IP) の作成
        ip_observable = client.stix_cyber_observable.create(
            observable_type="IPv4-Addr",
            observable_value=ip_value,
            description="悪意のあるIPアドレス",
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        print(f"[+] IP Observable が作成されました: {ip_observable['id']}")
        
        # Observable (URL) の作成
        url_observable = client.stix_cyber_observable.create(
            observable_type="Url",
            observable_value=url_value,
            description="悪意のあるURL",
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        print(f"[+] URL Observable が作成されました: {url_observable['id']}")
        
        # IP Observable に対応する Indicator の作成
        valid_until = (
            datetime.datetime.now() + datetime.timedelta(days=30)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        ip_indicator = client.indicator.create(
            name=f"悪意のあるIPアドレス指標: {ip_value}",
            description=f"悪意のあるIPアドレス {ip_value} を示す指標",
            pattern=f"[ipv4-addr:value = '{ip_value}']",
            pattern_type="stix",
            indicator_types=["malicious-activity"],
            valid_from=current_date,
            valid_until=valid_until,
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        print(f"[+] IP Indicator が作成されました: {ip_indicator['id']}")
        
        # URL Observable に対応する Indicator の作成
        url_indicator = client.indicator.create(
            name=f"悪意のあるURL指標: {url_value}",
            description=f"悪意のあるURL {url_value} を示す指標",
            pattern=f"[url:value = '{url_value}']",
            pattern_type="stix",
            indicator_types=["malicious-activity"],
            valid_from=current_date,
            valid_until=valid_until,
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        print(f"[+] URL Indicator が作成されました: {url_indicator['id']}")
        
        # IP Observable と IP Indicator の関係性を作成
        ip_relationship = client.stix_core_relationship.create(
            relationship_type="based-on",
            source_id=ip_indicator["id"],
            target_id=ip_observable["id"],
            description="この指標は観測されたIPアドレスに基づいています",
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        msg = "[+] IP Observable と Indicator の関係性が作成されました: "
        print(msg + ip_relationship['id'])
        
        # URL Observable と URL Indicator の関係性を作成
        url_relationship = client.stix_core_relationship.create(
            relationship_type="based-on",
            source_id=url_indicator["id"],
            target_id=url_observable["id"],
            description="この指標は観測されたURLに基づいています",
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        msg = "[+] URL Observable と Indicator の関係性が作成されました: "
        print(msg + url_relationship['id'])
        
        # レポートにObservableを追加
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=ip_observable["id"],
            description="このレポートはIPアドレスを含みます",
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=url_observable["id"],
            description="このレポートはURLを含みます",
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        # レポートにIndicatorを追加
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=ip_indicator["id"],
            description="このレポートはIPアドレス指標を含みます",
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=url_indicator["id"],
            description="このレポートはURL指標を含みます",
            confidence=75,
            object_marking_refs=[marking_definition["id"]],
            created_by_ref=identity_id,
        )
        
        print("[+] レポートにObservableとIndicatorが追加されました")
        print("[+] プロセスが正常に完了しました")
        
        return report["id"]
        
    except Exception as e:
        print(f"[!] エラーが発生しました: {str(e)}")
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
        default='192.168.1.1',
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
    report_id = create_report_with_indicators(
        args.report_name, args.ip, args.url
    )
    if report_id:
        print(f"[+] 作成されたレポートID: {report_id}")
    else:
        print("[!] レポートの作成に失敗しました") 