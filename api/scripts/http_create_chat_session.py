import json
import sys
import urllib.request

from loguru import logger


def main(user_uid: str, session_uid: str, initial_message: str | None) -> None:
    """user_uid のユーザーとして、session_uid の chat_session を作る(認証は Authorization: Bearer <user_uid>)"""
    url = "http://localhost:5000/api/chat_session"
    body = {"uid": session_uid, "label": "cli", "initial_message": initial_message}
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {user_uid}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        logger.info(response.status)


if __name__ == "__main__":
    # make で initial_message を省略すると空文字で渡ってくるため、None にする
    main(sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "") or None)
