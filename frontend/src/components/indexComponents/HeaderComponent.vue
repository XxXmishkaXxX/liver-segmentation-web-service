<template>
     <header>
    <router-link to="/">
        <img src="../../assets/img/navbar_footer/image.png" 
            alt="Логотип" 
            width="100" 
            height="60" 
            style="margin-left: 2vh;" 
            />
    </router-link>
    <nav style="font-family: 'Geologica'; margin-top:2vh ;">
      <a href="#aboutSection">о нас</a>
      <a href="#modelSection">модель</a>
      <a href="#supportSection" style="margin-right: 4vh;">поддержка</a>

      <button type="button" id="logo_but" class="btn">
        <img src="../../assets/img/navbar_footer/logo.svg" alt="Логотип" width="60" height="60" style="margin-right: 2vh;" />
      </button>
    </nav>
  </header>

</template>

<script>
    export default{
    }
</script>