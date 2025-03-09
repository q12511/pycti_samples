#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
テスト用のOpenCTI API設定ファイル
テスト実行時に使用される設定です。
"""

# テスト用のOpenCTI API設定
API_URL = "https://test.opencti.io"  # テスト用URL
API_KEY = "test-api-key"  # テスト用APIキー

# デフォルト設定
DEFAULT_CONFIDENCE = 75  # 信頼度のデフォルト値
DEFAULT_TLP = "TLP:AMBER"  # TLPマーキングのデフォルト値
DEFAULT_VALID_DAYS = 30  # Indicatorの有効期間（日数）

# テスト用のモックデータ
TEST_REPORT_ID = "report--test-id"
TEST_OBSERVABLE_ID = "observable--test-id"
TEST_INDICATOR_ID = "indicator--test-id"
TEST_RELATIONSHIP_ID = "relationship--test-id" 