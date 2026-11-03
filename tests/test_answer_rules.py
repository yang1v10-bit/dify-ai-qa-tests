import pytest


@pytest.mark.parametrize("answer,expected", [
    ("需提前3个工作日在系统提交申请", True),
    ("需提前5个工作日提交申请", False),
    ("知识库中没有相关规定", False),
])
def test_annual_leave_answer(answer, expected):
    """离线验证年假答案的判断规则"""
    actual = "3个工作日" in answer
    assert actual == expected
