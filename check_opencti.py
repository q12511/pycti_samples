#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pycti import OpenCTIApiClient
import json

# OpenCTI APIの設定
API_URL = "https://demo.opencti.io"
API_KEY = "e1ba28b4-4118-4581-9acf-6f1c42456c72"

# クライアントの初期化
client = OpenCTIApiClient(API_URL, API_KEY)

# 利用可能なマーキング定義を取得
print("=== マーキング定義の取得 ===")
try:
    marking_definitions = client.marking_definition.list()
    print(f"マーキング定義の数: {len(marking_definitions['entities'])}")
    for i, marking in enumerate(marking_definitions["entities"][:3]):
        print(f"\nマーキング定義 {i+1}:")
        print(f"ID: {marking['id']}")
        print(f"定義タイプ: {marking.get('definition_type', 'N/A')}")
        print(f"定義: {marking.get('definition', 'N/A')}")
        print(f"色: {marking.get('x_opencti_color', 'N/A')}")
except Exception as e:
    print(f"エラー: {str(e)}")

# 利用可能なアイデンティティを取得
print("\n=== アイデンティティの取得 ===")
try:
    identities = client.identity.list()
    print(f"アイデンティティの数: {len(identities['entities'])}")
    for i, identity in enumerate(identities["entities"][:3]):
        print(f"\nアイデンティティ {i+1}:")
        print(f"ID: {identity['id']}")
        print(f"名前: {identity.get('name', 'N/A')}")
        print(f"タイプ: {identity.get('entity_type', 'N/A')}")
except Exception as e:
    print(f"エラー: {str(e)}")

# レポートの作成テスト
print("\n=== レポート作成テスト ===")
try:
    # TLP:WHITEのマーキング定義を取得
    tlp_white = None
    for marking in marking_definitions["entities"]:
        if marking.get("definition") == "TLP:WHITE":
            tlp_white = marking
            break
    
    if tlp_white:
        print(f"TLP:WHITE マーキング定義: {tlp_white['id']}")
        
        # 最初のアイデンティティを使用
        identity = identities["entities"][0]
        print(f"使用するアイデンティティ: {identity['name']} ({identity['id']})")
        
        # レポートの作成を試みる
        report = client.report.create(
            name="APIテストレポート",
            description="APIテスト用のレポートです",
            published="2023-08-01T00:00:00Z",
            report_types=["threat-report"],
            confidence=75,
            object_marking_refs=[tlp_white["id"]],
            created_by_ref=identity["id"]
        )
        
        print(f"レポートが作成されました: {report['id']}")
    else:
        print("TLP:WHITEマーキング定義が見つかりませんでした")
except Exception as e:
    print(f"エラー: {str(e)}") 