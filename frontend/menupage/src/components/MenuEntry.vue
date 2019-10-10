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

<style>
#menu {
    text-align: left;
}
</style>
