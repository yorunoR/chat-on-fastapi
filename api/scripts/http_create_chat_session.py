import json
import sys
import urllib.request

from loguru import logger


def main(token: str, uid: str, initial_message: str | None) -> None:
    url = "http://localhost:5000/api/chat_session"
    body = {"uid": uid, "label": "cli", "initial_message": initial_message}
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        logger.info(response.status)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
