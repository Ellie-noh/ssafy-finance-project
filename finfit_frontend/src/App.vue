<template>
  <div class="app">
    <NavBar />
    <main class="container">
      <router-view />
    </main>
    <Chatbot />
  </div>
</template>

<script setup>
import NavBar from "@/components/NavBar.vue";
import Chatbot from "@/components/Chatbot.vue";
</script>

<style scoped>
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 16px;
}

.app {
  min-height: 100vh;
  background: #ffffff;
}
</style>

<style>
@import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap");

:root {
  --bg: #ffffff;
  --text: #111827;
  --muted: #6b7280;
  --border: #e5e7eb;
  --surface: #ffffff;
  --surface-alt: #f9fafb;
  --accent: #111827;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Space Grotesk", "Noto Sans KR", "Apple SD Gothic Neo", sans-serif;
  color: var(--text);
  background: var(--bg);
}

a {
  color: inherit;
}
</style>
