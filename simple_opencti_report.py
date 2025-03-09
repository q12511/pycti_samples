#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pycti import OpenCTIApiClient
import datetime

# OpenCTI APIの設定
API_URL = "https://demo.opencti.io"
API_KEY = "e1ba28b4-4118-4581-9acf-6f1c42456c72"

# クライアントの初期化
client = OpenCTIApiClient(API_URL, API_KEY)

# 現在の日時を取得
current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    try:
        print("[+] OpenCTIレポート作成プロセスを開始します...")
        
        # レポートの作成
        report = client.report.create(
            name="テスト分析レポート",
            description="このレポートはテスト用です。",
            published=current_date,
            report_types=["threat-report"],
            confidence=75
        )
        
        print(f"[+] レポートが作成されました: {report['id']}")
        
        # Observable (IP) の作成
        ip_observable = client.stix_cyber_observable.create(
            observable_type="IPv4-Addr",
            observable_value="8.8.8.8",
            description="テスト用IPアドレス"
        )
        
        print(f"[+] IP Observable が作成されました: {ip_observable['id']}")
        
        # Observable (URL) の作成
        url_observable = client.stix_cyber_observable.create(
            observable_type="Url",
            observable_value="https://test-malicious.example.com",
            description="テスト用URL"
        )
        
        print(f"[+] URL Observable が作成されました: {url_observable['id']}")
        
        # IP Observable に対応する Indicator の作成
        ip_indicator = client.indicator.create(
            name="テスト用IPアドレス指標",
            description="テスト用IPアドレスを示す指標",
            pattern="[ipv4-addr:value = '8.8.8.8']",
            pattern_type="stix",
            indicator_types=["malicious-activity"],
            valid_from=current_date,
            valid_until=(datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            confidence=75
        )
        
        print(f"[+] IP Indicator が作成されました: {ip_indicator['id']}")
        
        # URL Observable に対応する Indicator の作成
        url_indicator = client.indicator.create(
            name="テスト用URL指標",
            description="テスト用URLを示す指標",
            pattern="[url:value = 'https://test-malicious.example.com']",
            pattern_type="stix",
            indicator_types=["malicious-activity"],
            valid_from=current_date,
            valid_until=(datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            confidence=75
        )
        
        print(f"[+] URL Indicator が作成されました: {url_indicator['id']}")
        
        # IP Observable と IP Indicator の関係性を作成
        ip_relationship = client.stix_core_relationship.create(
            relationship_type="based-on",
            source_id=ip_indicator["id"],
            target_id=ip_observable["id"],
            description="この指標は観測されたIPアドレスに基づいています"
        )
        
        print(f"[+] IP Observable と Indicator の関係性が作成されました: {ip_relationship['id']}")
        
        # URL Observable と URL Indicator の関係性を作成
        url_relationship = client.stix_core_relationship.create(
            relationship_type="based-on",
            source_id=url_indicator["id"],
            target_id=url_observable["id"],
            description="この指標は観測されたURLに基づいています"
        )
        
        print(f"[+] URL Observable と Indicator の関係性が作成されました: {url_relationship['id']}")
        
        # レポートにObservableを追加
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=ip_observable["id"],
            description="このレポートはIPアドレスを含みます"
        )
        
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=url_observable["id"],
            description="このレポートはURLを含みます"
        )
        
        # レポートにIndicatorを追加
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=ip_indicator["id"],
            description="このレポートはIPアドレス指標を含みます"
        )
        
        client.stix_core_relationship.create(
            relationship_type="object-refs",
            source_id=report["id"],
            target_id=url_indicator["id"],
            description="このレポートはURL指標を含みます"
        )
        
        print("[+] レポートにObservableとIndicatorが追加されました")
        print("[+] プロセスが正常に完了しました")
        
        return report["id"]
        
    except Exception as e:
        print(f"[!] エラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    report_id = main()
    if report_id:
        print(f"[+] 作成されたレポートID: {report_id}")
    else:
        print("[!] レポートの作成に失敗しました") 