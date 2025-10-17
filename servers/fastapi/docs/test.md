# 初始化会话
```json
{
  "userId": "100",
  "userInput": "双曲线",
  "config": {
    "pages": 10,
    "classType": "新授课",
    "kbIds": [
      "111","112","113"
    ],
    "webSearch": true
  },
  "files": [
    {
      "name": "双曲线定义",
      "content": "双曲线",
      "url": "http://127.0.0.1:1234"
    },
{
      "name": "双曲线性质",
      "content": "双曲线",
      "url": "http://127.0.0.1:1234"
    },
{
      "name": "双曲线习题",
      "content": "双曲线",
      "url": "http://127.0.0.1:1234"
    }
  ]
}

{
  "userId": "100",
  "userInput": "二次函数",
  "config": {
    "pages": 10,
    "classType": "新授课",
    "kbIds": [
      "111","112","113"
    ],
    "webSearch": true
  },
  "files": [
    {
      "name": "二次函数定义",
      "content": "123456",
      "url": "http://127.0.0.1:1234"
    },
{
      "name": "二次函数性质",
      "content": "123456双曲线",
      "url": "http://127.0.0.1:1234"
    },
{
      "name": "二次函数习题",
      "content": "123456",
      "url": "http://127.0.0.1:1234"
    }
  ]
}
```
# 搜图
```shell
curl -H "Authorization: token" \
  "https://api.pexels.com/v1/search?query=nature&per_page=1"

```

# 教学大纲测试
```json
"tree": {
    "title": "AI大模型应用",
    "children": [
      {
        "title": "课程导学与职业发展",
        "children": [
          {
            "title": "你将收获哪些能力",
            "children": []
          },
          {
            "title": "AI时代需要什么样的人才",
            "children": []
          },
          {
            "title": "职业发展路径规划",
            "children": []
          }
        ]
      },
      {
        "title": "初识AI大模型与提示词工程",
        "children": [
          {
            "title": "提示词工程最佳实践",
            "children": []
          }
        ]
      },
      {
        "title": "AI核心技术与模型",
        "children": [
          {
            "title": "主流大模型(GPT/Claude)解析",
            "children": []
          }
        ]
      }
    ]
  }
```