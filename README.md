# Scrapy 项目(更新修改版)

基于 **Scrapy、DrissionPage 和 Scrapy-Redis** 的 Python 项目。

本项目的改进:
将 Scrapy 的请求调度机制与 DrissionPage 的浏览器自动化能力进行进一步深度整合。

本项目通过DrissionRequest、DrissionResponse 和 DrissionSpider，使 Scrapy 的 Request / Response / Spider 工作流程能够直接使用 DrissionPage 的浏览器能力。
在此基础上，进一步结合 Scrapy-Redis，将浏览器自动化爬取能力扩展到 Redis 分布式调度，使多个爬虫实例能够共享任务队列和请求去重机制。

本项目主要用于学习和实践：

* Scrapy 爬虫框架
* DrissionPage 浏览器自动化
* Scrapy 与 DrissionPage 集成
* Scrapy-Redis 分布式采集
* Redis 请求队列与去重
* 某东搜索数据采集
* 动态页面、懒加载页面的数据获取

---

## 📁 项目结构

```text
demo/
│
├── distributed_scrapy-drissionpage-redis/
│   └── JD_DP/
│       ├── spiders/
│       │   └── JDDP.py
│       ├── items.py
│       ├── pipelines.py
│       ├── settings.py
│       └── middlewares.py
│
├── scrapy-drissionpage/
│   └── JD_DP/
│       ├── spiders/
│       │   ├── JDDP.py
│       │   └── UrlRequests.txt
│       ├── items.py
│       ├── pipelines.py
│       ├── settings.py
│       └── middlewares.py
│
├── .gitignore
└── README.md

```

# 🕷️ 项目一：Scrapy + DrissionPage

目录：

```text
scrapy-drissionpage/
```

该项目将 Scrapy 的请求调度机制与 DrissionPage 浏览器自动化能力结合。

传统 Scrapy 主要通过 HTTP 请求获取网页：

```text
Scrapy
   ↓
HTTP Request
   ↓
HTML
   ↓
Selector
   ↓
数据解析
```

而使用 DrissionPage 后，可以通过真实浏览器加载页面：

```text
Scrapy
   ↓
DrissionPage Middleware
   ↓
Chromium
   ↓
网页加载 / JavaScript
   ↓
页面 DOM
   ↓
数据解析
```

因此可以处理一些依赖 JavaScript、动态渲染以及懒加载的页面。

---

## 🔧 主要功能

### 浏览器模式

使用 DrissionPage 的 `ChromiumPage` 加载网页：

```python
yield self.drission_request(
    url,
    page_type='chromium',
    callback=self.parse
)
```

在 `parse()` 中可以直接操作页面：

```python
response.page.ele(...)
response.page.eles(...)
response.page.scroll.to_bottom()
response.page.run_js(...)
```

---

## 🛒 某东数据采集

项目以某东搜索页面作为练习目标。

例如：

```text
https://example.com/Search?keyword=手机
```

可以采集：

* 商品名称
* 商品价格
* 商品销量
* 店铺名称

示例数据：

```text
商品名称 🔥 商品价格 🔥 销量 🔥 店铺名称
```

---

## 🔄 懒加载处理

某东页面存在动态加载内容，因此项目通过不断滚动页面的方式触发更多数据加载：

```python
while True:
    old_height = response.page.run_js(
        'return document.body.scrollHeight'
    )

    response.page.scroll.to_bottom()

    time.sleep(0.8)

    new_height = response.page.run_js(
        'return document.body.scrollHeight'
    )

    if new_height == old_height:
        break
```

基本原理：

```text
页面初始加载
      ↓
获取当前页面高度
      ↓
滚动到底部
      ↓
等待页面加载
      ↓
重新获取页面高度
      ↓
高度发生变化？
   ↙          ↘
 是            否
 ↓              ↓
继续滚动       停止滚动
```

---

# 🚀 项目二：Scrapy-Redis + DrissionPage

目录：

```text
distributed_scrapy-drissionpage-redis/
```

该项目在 Scrapy + DrissionPage 的基础上加入 Scrapy-Redis，实现多个爬虫实例之间共享任务队列。

基本结构：

```text
                Redis
             ↙    ↓    ↘
           爬虫1  爬虫2  爬虫3
             ↓     ↓     ↓
        DrissionPage
             ↓
           某东
             ↓
          数据采集
```

---

## Redis 的作用

Scrapy-Redis 主要利用 Redis 保存：

### 请求队列

```text
Redis
  ↓
待处理 URL
  ↓
Scrapy Spider
```

多个爬虫实例可以从同一个 Redis 队列中获取任务。

---

### 请求去重

Scrapy-Redis 可以通过 Redis 保存请求指纹。

当多个爬虫实例遇到相同 URL 时，可以避免重复处理。

---

### 数据共享

Scrapy-Redis 还可以将 Item 写入 Redis：

```text
Spider
  ↓
Item
  ↓
RedisPipeline
  ↓
Redis
```

方便后续其他程序继续处理数据。

---

# ⚙️ 环境

推荐环境：

```text
Python 3.10
Scrapy
DrissionPage
Scrapy-Redis
Redis
Chrome / Chromium
```

安装依赖：

```bash
pip install scrapy
pip install DrissionPage
pip install scrapy-redis
pip install scrapy-drissionpage
```

如果项目后续增加其他依赖，可以使用：

```bash
pip install -r requirements.txt
```

---

# 🔴 Redis 配置

Scrapy-Redis 项目需要 Redis 服务。

在：

```text
distributed_scrapy-drissionpage-redis/JD_DP/settings.py
```

中配置 Redis：

```python
REDIS_URL = "redis://127.0.0.1:6379"
```

如果 Redis 位于其他机器，则修改为对应地址：

```python
REDIS_URL = "redis://IP地址:6379"
```

例如：

```python
REDIS_URL = "redis://192.168.193.128:6379"
```

---

# 🕷️ 启动普通爬虫

进入对应 Scrapy 项目目录：

```bash
cd scrapy-drissionpage
```

查看爬虫：

```bash
scrapy list
```

运行：

```bash
scrapy crawl JDDP
```

如果不希望显示大量日志：

```bash
scrapy crawl JDDP --nolog
```

---

# 🌐 启动分布式爬虫

进入：

```text
distributed_scrapy-drissionpage-redis/
```

运行：

```bash
scrapy crawl JDDP_REDIS
```

或

```text
distributed_scrapy-drissionpage-redis/JD_DP/spiders
```

运行：

```bash
scrapy runspider JDDP.py
```

多个机器或多个进程可以连接到同一个 Redis 服务，从 Redis 队列中获取任务。

例如：

```text
Redis
  │
  ├── Spider A
  │
  ├── Spider B
  │
  └── Spider C
```

每个 Spider 都可以从 Redis 获取待处理 URL。

---

# 📌 Redis 请求格式

项目支持通过 Redis 向爬虫发送任务。

例如可以向对应的 Redis key 写入 URL：

```text
https://example/Search?keyword=手机
```

爬虫从 Redis 获取 URL 后，再通过：

```python
self.drission_request(
    url,
    page_type='chromium',
    callback=self.parse
)
```

创建 DrissionPage 请求。

---

# 🧩 核心技术

| 技术           | 作用            |
| ------------ | ------------- |
| Python       | 项目开发语言        |
| Scrapy       | 爬虫框架、请求调度     |
| DrissionPage | 浏览器自动化、动态页面处理 |
| Chromium     | 浏览器页面渲染       |
| Scrapy-Redis | Redis 分布式调度   |
| Redis        | 请求队列、去重、数据存储  |
| XPath        | 页面元素定位        |
| JavaScript   | 页面高度检测、动态页面操作 |

---

# ⚠️ 注意事项

1. 本项目主要用于学习 Scrapy、DrissionPage 和 Scrapy-Redis。
2. 使用爬虫时应遵守目标网站的相关规则和法律法规。
3. 不要对目标网站进行过高频率的请求。
4. 分布式爬虫启动多个实例后，请注意 Redis、浏览器实例以及目标网站的负载。
5. `.gitignore` 已排除 Python 缓存、虚拟环境、日志以及临时文件。

---

# 📚 方向

后续可以继续扩展：

* [ ] Scrapy Middleware
* [ ] Scrapy Pipeline
* [ ] DrissionPage 浏览器池
* [ ] Redis URL 队列
* [ ] Redis 请求去重
* [ ] 多机器分布式爬虫
* [ ] 浏览器实例池
* [ ] 代理池
* [ ] Cookie 池
* [ ] 数据库存储
* [ ] Elasticsearch
* [ ] Kafka
* [ ] Docker 部署

---

## License

MIT License
