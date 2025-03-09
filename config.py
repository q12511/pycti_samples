#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenCTI API設定ファイル
このファイルでAPIのURLとAPIキーを一元管理します。
"""

# OpenCTI APIの設定
API_URL = "https://demo.opencti.io"  # OpenCTIのURLを設定
API_KEY = "e1ba28b4-4118-4581-9acf-6f1c42456c72"  # OpenCTIのAPIキーを設定

# デフォルト設定
DEFAULT_CONFIDENCE = 75  # 信頼度のデフォルト値
DEFAULT_TLP = "TLP:AMBER"  # TLPマーキングのデフォルト値
DEFAULT_VALID_DAYS = 30  # Indicatorの有効期間（日数） 