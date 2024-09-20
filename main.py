from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseModel

from redis_app.db_connect import RedisHelper
from proxy_app.proxy_api_task import ProxyApiTask
from tool.schedule_app import run_all_proxy

db_helper = RedisHelper()
app = FastAPI()
scheduler = AsyncIOScheduler()


class DeleteProxyRequest(BaseModel):
    proxy: str


@app.get("/get_proxy")
async def get_proxy():
    proxy_app = ProxyApiTask()
    data = proxy_app.random_get_proxy()
    if data:
        return {
            "status": "success",
            "data": data
        }
    else:
        return {
            "status": "failed"
        }


@app.get("/batch_get_proxy")
async def batch_get_proxy():
    proxy_app = ProxyApiTask()
    data = proxy_app.get_all_proxy()
    if data:
        return {
            "status": "success",
            "data": data
        }
    else:
        return {
            "status": "failed"
        }


@app.delete("/delete_proxy")
async def delete_proxy(request_body: DeleteProxyRequest):
    proxy_app = ProxyApiTask()
    proxy = request_body.proxy
    result = proxy_app.delete_a_proxy(proxy)
    if result:
        return {
            "status": "success"
        }
    else:
        return {
            "status": "failed"
        }


@app.delete("/clear_proxy_table")
async def clear_proxy_table():
    proxy_app = ProxyApiTask()
    result = proxy_app.clear_proxy_table()
    if result:
        return {
            "status": "success"
        }
    else:
        return {
            "status": "failed"
        }


@app.put("/refresh_proxy_table")
async def refresh_proxy_table(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_all_proxy)
    return {"status": "success"}


@scheduler.scheduled_job('interval', hours=3)
async def schedule_func():
    """
    每3小时更新一次
    :return:
    """
    await run_all_proxy()


@app.on_event('startup')
async def startup():
    scheduler.start()


@app.on_event('shutdown')
async def shutdown():
    scheduler.shutdown()
