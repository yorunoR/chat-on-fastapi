<script setup>
import { nextTick, ref } from "vue";
import { createChatSession, sendText } from "./api";

const userUid = ref(localStorage.getItem("userUid") ?? "");
const sessionUid = ref(localStorage.getItem("sessionUid") ?? "");
const loggedIn = ref(false);
const messages = ref([]); // { role: "user" | "assistant", content }
const input = ref("");
const sending = ref(false);
const error = ref("");
const logEl = ref(null);

async function startSession() {
  sessionUid.value = crypto.randomUUID();
  await createChatSession(userUid.value, sessionUid.value);
  localStorage.setItem("sessionUid", sessionUid.value);
  messages.value = [];
}

async function login() {
  error.value = "";
  try {
    // 既存の chat_session があれば続きから、なければ新しく作る
    if (!sessionUid.value) await startSession();
    else await createChatSession(userUid.value, sessionUid.value).catch(() => {});
    localStorage.setItem("userUid", userUid.value);
    loggedIn.value = true;
  } catch (e) {
    error.value = e.message;
  }
}

async function newChat() {
  error.value = "";
  try {
    await startSession();
  } catch (e) {
    error.value = e.message;
  }
}

function scrollToBottom() {
  nextTick(() => logEl.value?.scrollTo(0, logEl.value.scrollHeight));
}

function send() {
  const text = input.value.trim();
  if (!text || sending.value) return;
  input.value = "";
  error.value = "";
  sending.value = true;
  messages.value.push({ role: "user", content: text });
  messages.value.push({ role: "assistant", content: "" });
  const answer = messages.value[messages.value.length - 1];
  scrollToBottom();
  sendText(sessionUid.value, text, {
    onMessage: (m) => {
      answer.content += m.content;
      scrollToBottom();
    },
    onDone: () => (sending.value = false),
    onError: (e) => {
      error.value = e.message;
      sending.value = false;
    },
  });
}
</script>

<template>
  <main>
    <form v-if="!loggedIn" class="login" @submit.prevent="login">
      <h1>Chat</h1>
      <input v-model="userUid" placeholder="User の uid" required />
      <button>開始</button>
    </form>

    <template v-else>
      <header>
        <h1>Chat</h1>
        <button :disabled="sending" @click="newChat">新しい会話</button>
      </header>
      <div ref="logEl" class="log">
        <div v-for="(m, i) in messages" :key="i" :class="['msg', m.role]">{{ m.content }}</div>
      </div>
      <form class="input" @submit.prevent="send">
        <input v-model="input" placeholder="メッセージを入力" :disabled="sending" />
        <button :disabled="sending || !input.trim()">送信</button>
      </form>
    </template>
    <p v-if="error" class="error">{{ error }}</p>
  </main>
</template>

<style>
body { margin: 0; font-family: sans-serif; background: #f4f4f5; }
main { max-width: 720px; height: 100vh; margin: 0 auto; padding: 16px; box-sizing: border-box; display: flex; flex-direction: column; gap: 12px; }
h1 { margin: 0; font-size: 20px; }
header { display: flex; justify-content: space-between; align-items: center; }
.login { margin: auto; display: flex; flex-direction: column; gap: 12px; width: 320px; }
.log { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
.msg { max-width: 80%; padding: 8px 12px; border-radius: 8px; white-space: pre-wrap; background: #fff; align-self: flex-start; }
.msg.user { background: #2563eb; color: #fff; align-self: flex-end; }
.input { display: flex; gap: 8px; }
.input input { flex: 1; }
input, button { padding: 8px 12px; font-size: 14px; }
.error { color: #dc2626; margin: 0; }
</style>
