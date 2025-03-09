#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenCTI APIのモック
テスト時に実際のAPIの代わりに使用されます。
"""

from tests.test_config import (
    TEST_REPORT_ID,
    TEST_OBSERVABLE_ID,
    TEST_INDICATOR_ID,
    TEST_RELATIONSHIP_ID
)


class MockOpenCTIApiClient:
    """OpenCTI APIクライアントのモッククラス"""

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.report = MockReportAPI()
        self.stix_cyber_observable = MockObservableAPI()
        self.indicator = MockIndicatorAPI()
        self.stix_core_relationship = MockRelationshipAPI()


class MockReportAPI:
    """レポートAPIのモック"""

    def create(self, **kwargs):
        """レポート作成のモック"""
        return {
            "id": TEST_REPORT_ID,
            "name": kwargs.get("name", "テストレポート"),
            "description": kwargs.get("description", "テスト用の説明"),
            "published": kwargs.get("published", "2023-01-01T00:00:00Z"),
            "confidence": kwargs.get("confidence", 75)
        }

    def add_stix_object_or_stix_relationship(self, **kwargs):
        """レポートにオブジェクトを追加するモック"""
        return {
            "id": kwargs.get("id", TEST_REPORT_ID),
            "stixObjectOrStixRelationshipId": kwargs.get(
                "stixObjectOrStixRelationshipId", TEST_OBSERVABLE_ID
            )
        }


class MockObservableAPI:
    """Observable APIのモック"""

    def create(self, **kwargs):
        """Observable作成のモック"""
        observable_data = kwargs.get("observableData", {})
        return {
            "id": TEST_OBSERVABLE_ID,
            "type": observable_data.get("type", "ipv4-addr"),
            "value": observable_data.get("value", "8.8.8.8"),
            "description": observable_data.get(
                "x_opencti_description", "テスト用Observable"
            )
        }


class MockIndicatorAPI:
    """Indicator APIのモック"""

    def create(self, **kwargs):
        """Indicator作成のモック"""
        return {
            "id": TEST_INDICATOR_ID,
            "name": kwargs.get("name", "テスト用Indicator"),
            "description": kwargs.get("description", "テスト用の説明"),
            "pattern": kwargs.get("pattern", "[ipv4-addr:value = '8.8.8.8']"),
            "pattern_type": kwargs.get("pattern_type", "stix"),
            "valid_from": kwargs.get("valid_from", "2023-01-01T00:00:00Z"),
            "valid_until": kwargs.get("valid_until", "2023-02-01T00:00:00Z"),
            "confidence": kwargs.get("confidence", 75)
        }


class MockRelationshipAPI:
    """Relationship APIのモック"""

    def create(self, **kwargs):
        """関係性作成のモック"""
        return {
            "id": TEST_RELATIONSHIP_ID,
            "relationship_type": kwargs.get("relationship_type", "based-on"),
            "fromId": kwargs.get("fromId", TEST_INDICATOR_ID),
            "toId": kwargs.get("toId", TEST_OBSERVABLE_ID),
            "description": kwargs.get("description", "テスト用の関係性")
        } 