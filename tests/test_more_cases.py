import os
import pytest
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

API_KEY = os.getenv("DIFY_API_KEY")
API_URL = "https://api.dify.ai/v1/chat-messages"


@pytest.mark.parametrize("question,expected", [
    ("报销申请最晚什么时候提交？", "25"),
    ("IT技术支持到几点结束？", "18:00"),
])
def test_normal_questions(question, expected):
    assert API_KEY, "缺少API密钥"

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "inputs": {},
            "query": question,
            "response_mode": "blocking",
            "user": "qa-auto-test"
        },
        timeout=90
    )

    assert response.status_code == 200
    answer = response.json().get("answer", "")

    print(f"\n问题：{question}\n回答：{answer}")
    assert expected in answer


def test_unknown_bonus():
    assert API_KEY, "缺少API密钥"

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "inputs": {},
            "query": "公司年终奖是多少钱？",
            "response_mode": "blocking",
            "user": "qa-auto-test"
        },
        timeout=90
    )

    assert response.status_code == 200
    answer = response.json().get("answer", "")

    print(f"\n年终奖问题回答：{answer}")

    assert any(text in answer for text in [
        "无法确定", "没有相关规定", "没有相关信息",
        "未提供"
    ])
