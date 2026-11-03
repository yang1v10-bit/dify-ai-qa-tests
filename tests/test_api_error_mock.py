import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests


@pytest.mark.parametrize("filename,function,args", [
    ("test_chat_api.py", "test_annual_leave", ()),
    ("test_more_cases.py", "test_normal_questions",
     ("IT技术支持到几点结束？", "18:00")),
    ("test_more_cases.py", "test_unknown_bonus", ()),
])
@pytest.mark.parametrize("scenario", ["quota", "other_error"])
def test_error_handling(monkeypatch, filename, function, args, scenario):
    """使用模拟响应验证在线测试的错误处理，不调用真实API"""

    namespace = runpy.run_path(
        str(Path(__file__).parent / filename)
    )
    test_function = namespace[function]

    # 只使用虚构密钥，不需要真实API密钥
    test_function.__globals__["API_KEY"] = "app-offline-test"

    if scenario == "quota":
        message = "Model quota has been exceeded"
    else:
        message = "Invalid parameter"

    fake_response = SimpleNamespace(
        status_code=400,
        text=message
    )

    # 用模拟响应代替真正的网络请求
    monkeypatch.setattr(
        requests, "post",
        lambda *args, **kwargs: fake_response
    )

    if scenario == "quota":
        with pytest.raises(pytest.skip.Exception):
            test_function(*args)
    else:
        with pytest.raises(AssertionError, match="HTTP 400"):
            test_function(*args)
