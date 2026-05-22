<template>
  <div id="app">
    <nav>
      <h1>🎯 求职助手</h1>
      <div class="nav-links">
        <router-link to="/career">职业探索</router-link>
        <router-link to="/interview">面试模拟</router-link>
        <router-link to="/resume">简历优化</router-link>
        <router-link to="/jobmatch">投递分析</router-link>
      </div>
    </nav>
    <main>
      <router-view />
    </main>
    <footer>
      <p>多模态模拟面试评测智能体 · 第八组</p>
    </footer>
  </div>
</template>

<style scoped>
nav {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
nav h1 { font-size: 1.2rem; }
.nav-links { display: flex; gap: 1.5rem; }
.nav-links a {
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  font-size: 0.9rem;
  padding: 0.3rem 0.8rem;
  border-radius: 6px;
  transition: all 0.2s;
}
.nav-links a:hover, .nav-links a.router-link-active {
  color: white;
  background: rgba(255,255,255,0.2);
}
main {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}
footer {
  text-align: center;
  padding: 1rem;
  color: #999;
  font-size: 0.8rem;
  margin-top: 3rem;
}
</style>