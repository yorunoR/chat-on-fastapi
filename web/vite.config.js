import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vue()],
  server: {
    // compose のボリューム上では inotify が効かないため、ポーリングで変更を検知する
    watch: { usePolling: true },
  },
});
