#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create_indicator.pyのテスト
"""

import unittest
from unittest.mock import patch
import sys
import os

# テスト対象のモジュールをインポートできるようにパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_config import TEST_INDICATOR_ID
from create_indicator import create_indicator


class TestCreateIndicator(unittest.TestCase):
    """create_indicator関数のテストクラス"""

    @patch('create_indicator.client')
    def test_create_indicator_success(self, mock_client):
        """Indicator作成が成功するケースのテスト"""
        # モックの設定
        mock_indicator = {
            "id": TEST_INDICATOR_ID,
            "name": "テスト用Indicator",
            "description": "テスト用の説明",
            "pattern": "[ipv4-addr:value = '8.8.8.8']",
            "pattern_type": "stix",
            "valid_from": "2023-01-01T00:00:00Z",
            "valid_until": "2023-02-01T00:00:00Z",
            "confidence": 75
        }
        mock_client.indicator.create.return_value = mock_indicator

        # テスト対象の関数を実行
        result = create_indicator(
            "テスト用Indicator",
            "テスト用の説明",
            "[ipv4-addr:value = '8.8.8.8']",
            "stix"
        )

        # 検証
        self.assertEqual(result, TEST_INDICATOR_ID)
        mock_client.indicator.create.assert_called_once()
        args, kwargs = mock_client.indicator.create.call_args
        self.assertEqual(kwargs["name"], "テスト用Indicator")
        self.assertEqual(kwargs["description"], "テスト用の説明")
        self.assertEqual(kwargs["pattern"], "[ipv4-addr:value = '8.8.8.8']")
        self.assertEqual(kwargs["pattern_type"], "stix")

    @patch('create_indicator.client')
    def test_create_indicator_failure(self, mock_client):
        """Indicator作成が失敗するケースのテスト"""
        # モックの設定
        mock_client.indicator.create.side_effect = Exception("API Error")

        # テスト対象の関数を実行
        result = create_indicator(
            "テスト用Indicator",
            "テスト用の説明",
            "[ipv4-addr:value = '8.8.8.8']",
            "stix"
        )

        # 検証
        self.assertIsNone(result)
        mock_client.indicator.create.assert_called_once()


if __name__ == '__main__':
    unittest.main() 