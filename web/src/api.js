// ブラウザから見た API サーバーの URL(compose ではホストに公開した 5000 番)
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:5000";

export async function createChatSession(userUid, sessionUid) {
  const res = await fetch(`${API_URL}/api/chat_session`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${userUid}` },
    body: JSON.stringify({ uid: sessionUid, label: "web" }),
  });
  if (res.status === 401) throw new Error("ユーザーの uid が正しくありません");
  if (!res.ok) throw new Error(`chat_session の作成に失敗しました (${res.status})`);
}

/**
 * 1 回の送信と、その回答の受信。接続は 1 送信につき 1 つ。
 * message は回答の一部(stop: true で 1 つの回答の終わり)、done で処理がすべて終わるので接続を閉じる。
 */
export function sendText(sessionUid, text, { onMessage, onDone, onError }) {
  const ws = new WebSocket(`${API_URL.replace(/^http/, "ws")}/ws/normal_chat/${sessionUid}`);
  let done = false;
  ws.onopen = () => ws.send(text);
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.message) onMessage(data.message);
    if (data.done) {
      done = true;
      ws.close();
      onDone();
    }
  };
  // done が来ないまま切れたら異常として扱う
  ws.onclose = () => {
    if (!done) onError(new Error("接続が切れました"));
  };
  return ws;
}
