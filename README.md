# FastAPI 电影 CRUD（无数据库 Session 版）

这是一个独立的学习副本，用 Python 内存中的 `movies` 列表保存电影，不连接 MySQL，也不创建或注入 `AsyncSession`。

## 运行

在本目录打开终端后运行：

```powershell
python -m uvicorn src:app --reload
```

如果要使用原项目已有的虚拟环境：

```powershell
..\demofastapi\demoenv\Scripts\python.exe -m uvicorn src:app --reload
```

接口文档：<http://127.0.0.1:8000/docs>

接口前缀是 `/api/v1/movies`。可以在 Swagger 文档中练习查询全部、按 ID 查询、创建、修改和删除。

## 请求数据示例

创建电影时，发送 JSON：

```json
{
  "title": "新电影",
  "director": "导演姓名",
  "production_company": "制作公司",
  "release_date": "2026-10-20",
  "duration_minutes": 110,
  "language": "Mandarin"
}
```

`id` 由这个学习版的 Service 根据当前列表生成，创建请求不用传。

## 重要边界

电影列表只是 Python 进程内存中的对象。创建、修改或删除只改变当前进程里的列表；重启服务后，会重新加载 `movie_data.py` 中的初始 10 条电影。因此这份副本用于理解路由、Service 和 CRUD 调用关系，不具备数据库持久化能力。

这是根据现有 `movie_data.py` 和学习对话中确认的旧版 CRUD 行为重建的学习副本，不声称是从 PyCharm Local History 原样恢复的逐字历史快照。原项目保持不变。

额外保留了原项目的基础 FastAPI 示例。需要运行它时，在本目录执行：

```powershell
..\demofastapi\demoenv\Scripts\python.exe -m uvicorn src.demo.main_demo:app --reload --port 8001
```
