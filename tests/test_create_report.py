#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create_report_only.pyのテスト
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# テスト対象のモジュールをインポートできるようにパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.mock_opencti import MockOpenCTIApiClient
from tests.test_config import TEST_REPORT_ID
from create_report_only import create_report


class TestCreateReport(unittest.TestCase):
    """create_report関数のテストクラス"""

    @patch('create_report_only.client')
    def test_create_report_success(self, mock_client):
        """レポート作成が成功するケースのテスト"""
        # モックの設定
        mock_report = {
            "id": TEST_REPORT_ID,
            "name": "テストレポート",
            "description": "テスト用の説明",
            "published": "2023-01-01T00:00:00Z",
            "confidence": 75
        }
        mock_client.report.create.return_value = mock_report

        # テスト対象の関数を実行
        result = create_report("テストレポート", "テスト用の説明")

        # 検証
        self.assertEqual(result, TEST_REPORT_ID)
        mock_client.report.create.assert_called_once()
        args, kwargs = mock_client.report.create.call_args
        self.assertEqual(kwargs["name"], "テストレポート")
        self.assertEqual(kwargs["description"], "テスト用の説明")

    @patch('create_report_only.client')
    def test_create_report_failure(self, mock_client):
        """レポート作成が失敗するケースのテスト"""
        # モックの設定
        mock_client.report.create.side_effect = Exception("API Error")

        # テスト対象の関数を実行
        result = create_report("テストレポート", "テスト用の説明")

        # 検証
        self.assertIsNone(result)
        mock_client.report.create.assert_called_once()


if __name__ == '__main__':
    unittest.main() 