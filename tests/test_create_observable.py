#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create_observable.pyのテスト
"""

import unittest
from unittest.mock import patch
import sys
import os

# テスト対象のモジュールをインポートできるようにパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_config import TEST_OBSERVABLE_ID
from create_observable import create_observable


class TestCreateObservable(unittest.TestCase):
    """create_observable関数のテストクラス"""

    @patch('create_observable.client')
    def test_create_ipv4_observable_success(self, mock_client):
        """IPv4 Observable作成が成功するケースのテスト"""
        # モックの設定
        mock_observable = {
            "id": TEST_OBSERVABLE_ID,
            "type": "ipv4-addr",
            "value": "8.8.8.8",
            "description": "テスト用IPアドレス"
        }
        mock_client.stix_cyber_observable.create.return_value = mock_observable

        # テスト対象の関数を実行
        result = create_observable("ipv4-addr", "8.8.8.8", "テスト用IPアドレス")

        # 検証
        self.assertEqual(result, TEST_OBSERVABLE_ID)
        mock_client.stix_cyber_observable.create.assert_called_once()
        args, kwargs = mock_client.stix_cyber_observable.create.call_args
        self.assertEqual(kwargs["observableData"]["type"], "ipv4-addr")
        self.assertEqual(kwargs["observableData"]["value"], "8.8.8.8")

    @patch('create_observable.client')
    def test_create_url_observable_success(self, mock_client):
        """URL Observable作成が成功するケースのテスト"""
        # モックの設定
        mock_observable = {
            "id": TEST_OBSERVABLE_ID,
            "type": "url",
            "value": "https://example.com",
            "description": "テスト用URL"
        }
        mock_client.stix_cyber_observable.create.return_value = mock_observable

        # テスト対象の関数を実行
        result = create_observable("url", "https://example.com", "テスト用URL")

        # 検証
        self.assertEqual(result, TEST_OBSERVABLE_ID)
        mock_client.stix_cyber_observable.create.assert_called_once()
        args, kwargs = mock_client.stix_cyber_observable.create.call_args
        self.assertEqual(kwargs["observableData"]["type"], "url")
        self.assertEqual(kwargs["observableData"]["value"], "https://example.com")

    @patch('create_observable.client')
    def test_create_file_observable_success(self, mock_client):
        """File Observable作成が成功するケースのテスト"""
        # モックの設定
        mock_observable = {
            "id": TEST_OBSERVABLE_ID,
            "type": "file",
            "hashes": {"md5": "d41d8cd98f00b204e9800998ecf8427e"},
            "description": "テスト用ファイル"
        }
        mock_client.stix_cyber_observable.create.return_value = mock_observable

        # テスト対象の関数を実行
        result = create_observable(
            "file", "d41d8cd98f00b204e9800998ecf8427e", "テスト用ファイル"
        )

        # 検証
        self.assertEqual(result, TEST_OBSERVABLE_ID)
        mock_client.stix_cyber_observable.create.assert_called_once()
        args, kwargs = mock_client.stix_cyber_observable.create.call_args
        self.assertEqual(kwargs["observableData"]["type"], "file")
        self.assertEqual(
            kwargs["observableData"]["hashes"]["md5"],
            "d41d8cd98f00b204e9800998ecf8427e"
        )

    @patch('create_observable.client')
    def test_create_observable_failure(self, mock_client):
        """Observable作成が失敗するケースのテスト"""
        # モックの設定
        mock_client.stix_cyber_observable.create.side_effect = Exception("API Error")

        # テスト対象の関数を実行
        result = create_observable("ipv4-addr", "8.8.8.8", "テスト用IPアドレス")

        # 検証
        self.assertIsNone(result)
        mock_client.stix_cyber_observable.create.assert_called_once()


if __name__ == '__main__':
    unittest.main() 