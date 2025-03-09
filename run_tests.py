#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
すべてのテストを実行するスクリプト
"""

import unittest
import sys
import os

# テストディレクトリをインポートパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# テストを検出して実行
if __name__ == '__main__':
    # テストディレクトリからすべてのテストを検出
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')

    # テストを実行
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # 終了コードを設定（テストが失敗した場合は1、成功した場合は0）
    sys.exit(not result.wasSuccessful()) 