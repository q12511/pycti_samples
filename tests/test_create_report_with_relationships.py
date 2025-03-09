#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create_report_with_relationships.pyのテスト
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# テスト対象のモジュールをインポートできるようにパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_config import (
    TEST_REPORT_ID,
    TEST_OBSERVABLE_ID,
    TEST_INDICATOR_ID,
    TEST_RELATIONSHIP_ID
)
from create_report_with_relationships import create_report_with_relationships


class TestCreateReportWithRelationships(unittest.TestCase):
    """create_report_with_relationships関数のテストクラス"""

    @patch('create_report_with_relationships.client')
    def test_create_report_with_relationships_success(self, mock_client):
        """レポート作成と関係性の設定が成功するケースのテスト"""
        # モックの設定
        mock_report = {"id": TEST_REPORT_ID}
        mock_ip_observable = {"id": TEST_OBSERVABLE_ID}
        mock_url_observable = {"id": TEST_OBSERVABLE_ID}
        mock_ip_indicator = {"id": TEST_INDICATOR_ID}
        mock_url_indicator = {"id": TEST_INDICATOR_ID}
        mock_ip_relationship = {"id": TEST_RELATIONSHIP_ID}
        mock_url_relationship = {"id": TEST_RELATIONSHIP_ID}
        mock_add_object = {"id": TEST_REPORT_ID}

        mock_client.report.create.return_value = mock_report
        mock_client.stix_cyber_observable.create.side_effect = [
            mock_ip_observable, mock_url_observable
        ]
        mock_client.indicator.create.side_effect = [
            mock_ip_indicator, mock_url_indicator
        ]
        mock_client.stix_core_relationship.create.side_effect = [
            mock_ip_relationship, mock_url_relationship
        ]
        mock_client.report.add_stix_object_or_stix_relationship.return_value = (
            mock_add_object
        )

        # テスト対象の関数を実行
        result = create_report_with_relationships(
            "テストレポート", "8.8.8.8", "https://example.com"
        )

        # 検証
        self.assertEqual(result, TEST_REPORT_ID)
        mock_client.report.create.assert_called_once()
        self.assertEqual(mock_client.stix_cyber_observable.create.call_count, 2)
        self.assertEqual(mock_client.indicator.create.call_count, 2)
        self.assertEqual(mock_client.stix_core_relationship.create.call_count, 2)
        self.assertGreaterEqual(
            mock_client.report.add_stix_object_or_stix_relationship.call_count, 1
        )

    @patch('create_report_with_relationships.client')
    def test_create_report_failure(self, mock_client):
        """レポート作成が失敗するケースのテスト"""
        # モックの設定
        mock_client.report.create.side_effect = Exception("API Error")

        # テスト対象の関数を実行
        result = create_report_with_relationships(
            "テストレポート", "8.8.8.8", "https://example.com"
        )

        # 検証
        self.assertIsNone(result)
        mock_client.report.create.assert_called_once()
        mock_client.stix_cyber_observable.create.assert_not_called()

    @patch('create_report_with_relationships.client')
    def test_create_observable_failure(self, mock_client):
        """Observable作成が失敗するケースのテスト"""
        # モックの設定
        mock_report = {"id": TEST_REPORT_ID}
        mock_client.report.create.return_value = mock_report
        mock_client.stix_cyber_observable.create.return_value = None

        # テスト対象の関数を実行
        result = create_report_with_relationships(
            "テストレポート", "8.8.8.8", "https://example.com"
        )

        # 検証
        self.assertEqual(result, TEST_REPORT_ID)
        mock_client.report.create.assert_called_once()
        mock_client.stix_cyber_observable.create.assert_called_once()
        mock_client.indicator.create.assert_not_called()


if __name__ == '__main__':
    unittest.main() 