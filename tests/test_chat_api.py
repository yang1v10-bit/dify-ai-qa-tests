import pytest
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# 读取本地API密钥
project_dir = Path(__file__).resolve().parents[1]
load_dotenv(project_dir / ".env", override=True)

API_KEY = os.getenv("DIFY_API_KEY")
API_URL = "https://api.dify.ai/v1/chat-messages"


def test_annual_leave():
    """验证AI能否正确回答年假申请规定"""

    assert API_KEY, "未找到Dify API密钥"

    payload = {
        "inputs": {},
        "query": "年假需要提前多久申请？",
        "response_mode": "blocking",
        "user": "qa-auto-test"
    }

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=payload,
        timeout=90
    )

    if response.status_code == 400 and "Model quota has been exceeded" in response.text:
        pytest.skip("Dify模型额度耗尽，在线测试暂时阻塞")

    assert response.status_code == 200, (
        f"HTTP {response.status_code}: {response.text[:200]}"
    )

    answer = response.json().get("answer", "")
    print("\nAI实际回答：", answer)

    assert "3个工作日" in answer
    assert "直属主管" in answer
