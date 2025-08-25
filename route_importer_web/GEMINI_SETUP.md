# 🚀 Gemini API 集成设置

## 📋 前置要求

1. **Python 3.9+**
2. **Gemini API 密钥**

## 🔑 获取 Gemini API 密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录你的Google账户
3. 点击"Create API Key"
4. 复制生成的API密钥

## ⚙️ 环境配置

### 方法1：环境变量（推荐）
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 方法2：.env文件
```bash
# 复制示例文件
cp .env.example .env

# 编辑.env文件，填入你的API密钥
GEMINI_API_KEY=your_actual_api_key_here
```

## 🧪 测试API

运行测试脚本验证API是否正常工作：

```bash
python3 test_gemini.py
```

输入你的API密钥，脚本会：
1. 测试API连接
2. 解析示例小红书文本
3. 提取POI信息
4. 显示结果

## 🔧 集成到主应用

1. **设置环境变量**
2. **重启Flask应用**
3. **在Web界面中测试**

## 📊 预期效果

使用Gemini API后，POI识别应该：
- ✅ 准确识别5个地点
- ✅ 过滤掉描述性文本
- ✅ 提供结构化的地点信息
- ✅ 大幅提升识别准确率

## 🚨 注意事项

- API密钥请保密，不要提交到代码仓库
- 每次API调用都有成本，建议在开发阶段使用
- 如果API失败，系统会自动回退到规则解析器

## 🆘 故障排除

### API调用失败
- 检查API密钥是否正确
- 确认网络连接正常
- 查看控制台错误日志

### 解析结果不准确
- 调整提示词内容
- 检查输入文本格式
- 验证API响应格式
