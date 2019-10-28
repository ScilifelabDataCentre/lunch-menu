<template>
<div class="menu">
  {{ dish }}
</div>
</template>

<script>
export default {
  name: 'MenuEntry',
  props: ["dish"],
}
</script>

<style scoped>
.menu {
    color: #2c3e50;
}
</style>
