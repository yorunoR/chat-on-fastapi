import asyncio
import json
from collections.abc import AsyncIterator, Callable
from typing import Any

# 回答をまとめて送るチャンク数。1 チャンクずつ送ると送信回数が多くなりすぎる
CHUNKS_PER_MESSAGE = 3


async def send_json(ws, data: dict[str, Any]) -> None:
    """ws が None のときは送らない(テスト・評価・バッチ用)"""
    if ws is not None:
        # 日本語を \uXXXX にせずそのまま送る(読みやすく、UTF-8 のほうがデータも小さい)
        await ws.send_text(json.dumps(data, ensure_ascii=False))
        await asyncio.sleep(0)


async def send_message(ws, message: dict[str, Any]) -> None:
    await send_json(ws, {"message": message})


class ContentStreamSender:
    """1 つの回答をストリーミングで送り、最後に stop を送る。1 回答につき 1 インスタンス

    送信中に例外(切断・タイムアウト・LLM のエラー)で止まっても、content にそこまでの回答が残る
    """

    def __init__(self, ws, agent: str, *, check_cancel: Callable[[str], bool] | None = None) -> None:
        """check_cancel は、それまでの回答の全文を受け取り、中断するなら True を返す"""
        self.ws = ws
        self.agent = agent
        self.check_cancel = check_cancel
        self.content = ""
        self.cancel = False

    async def send(self, astream: AsyncIterator[str]) -> None:
        pending_content = ""
        pending_count = 0
        async for content in astream:
            self.content += content
            pending_content += content
            pending_count += 1
            if pending_count >= CHUNKS_PER_MESSAGE:
                await self.__send_content(pending_content)
                pending_content = ""
                pending_count = 0

        if pending_content:
            await self.__send_content(pending_content)

        await send_message(self.ws, {"agent": self.agent, "content": "", "content_key": None, "stop": True, "cancel": self.cancel})

    async def __send_content(self, content: str) -> None:
        self.cancel = self.cancel or (self.check_cancel is not None and self.check_cancel(self.content))
        message = {"agent": self.agent, "content": content, "content_key": "message", "stop": None, "cancel": self.cancel}
        await send_message(self.ws, message)


async def send_content_with_options(ws, agent: str, content: str, options: Any) -> None:
    """選択肢つきの回答を 1 回で送る。stop も兼ねる"""
    await send_message(ws, {"agent": agent, "content": content, "options": options, "content_key": None, "stop": True, "cancel": False})


async def send_done(ws) -> None:
    """この接続での処理がすべて終わった合図。クライアントは受け取ったら接続を閉じる"""
    await send_json(ws, {"done": True})
