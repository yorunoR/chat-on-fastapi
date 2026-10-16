import asyncio
from collections.abc import Coroutine
from typing import Any

from loguru import logger

# 実行中のタスクの参照を持っておかないと、完了前にガベージコレクションされることがある
background_tasks: set[asyncio.Task[Any]] = set()


def run_in_background(coro: Coroutine[Any, Any, Any], *, name: str) -> None:
    """接続やリクエストの寿命から切り離して実行する。例外はログに出す"""
    task = asyncio.create_task(coro, name=name)
    background_tasks.add(task)
    task.add_done_callback(on_background_task_done)


def on_background_task_done(task: asyncio.Task[Any]) -> None:
    background_tasks.discard(task)
    if task.cancelled():
        logger.warning(f"background task cancelled: {task.get_name()}")
        return
    exception = task.exception()
    if exception is not None:
        logger.opt(exception=exception).error(f"background task failed: {task.get_name()}")


async def wait_background_tasks(timeout: float) -> None:
    """終了時に実行中のタスクを待つ。timeout を過ぎたものはキャンセルする"""
    if not background_tasks:
        return
    _done, pending = await asyncio.wait(set(background_tasks), timeout=timeout)
    for task in pending:
        task.cancel()
    # キャンセルが終わるまで待つ
    await asyncio.gather(*pending, return_exceptions=True)
