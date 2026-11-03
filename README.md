# AI知识库问答助手质量评测与自动化测试

## 项目简介

基于Dify Chatflow搭建企业AI知识库问答助手，
使用Python、Requests、pytest进行接口自动化测试，
验证知识库问答的准确性、知识边界和异常场景。

## 技术栈

- Dify / RAG / GPT-5
- Python 3.13
- Requests
- pytest
- pytest-html
- python-dotenv

## 测试架构

用户问题
    ↓
Dify Chatflow API
    ↓
知识库检索
    ↓
LLM生成回答
    ↓
Python获取JSON结果
    ↓
pytest执行断言
    ↓
HTML测试报告

## 已完成的真实测试

### 1. 手工测试
- 知识库召回验证
- 正常业务问答
- 无依据问题拒答
- 知识边界测试
- 基础提示词注入测试

### 2. 在线接口自动化
- 已实现Dify API调用和Bearer认证
- 年假、报销两条用例通过
- 后续两条因模型额度耗尽返回HTTP 400
- 不将额度限制误报为AI回答错误

### 3. 离线规则测试
- 正确回答识别
- 错误申请天数识别
- 无依据回答识别

执行结果：3 passed，0 failed。

## 运行方法

安装依赖：

    pip install requests pytest python-dotenv pytest-html

在项目根目录创建本地.env文件：

    DIFY_API_KEY=你的应用密钥

执行离线测试：

    python -m pytest tests/test_answer_rules.py -v

生成HTML报告：

    python -m pytest tests/test_answer_rules.py --html=reports/offline-report.html --self-contained-html

## 测试结果说明

本项目区分真实在线API测试与离线规则测试。
Dify模型额度耗尽会阻止后续在线用例执行，
不代表AI答案本身验证失败。

项目使用虚构企业制度数据，不涉及真实企业内部资料。

## 项目状态

已完成基础手工测试、API调用、部分在线自动化、
离线规则测试及HTML报告。

后续完善异常处理、测试断言和持续集成。

## 测试报告

查看[项目测试执行总结](docs/TEST_REPORT.md)。

HTML离线测试报告可在本地使用pytest-html生成。
在线测试与Mock测试结果分开记录。
