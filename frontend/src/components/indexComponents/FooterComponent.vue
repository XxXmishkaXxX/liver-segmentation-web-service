<template>
    <footer class="text-center text-lg-start text-black" style="background-color: #D9D9D9;">
    <div class="container p-4 pb-0">
      <section class="">
        <div class="row">
          <div class="col-md-3 col-lg-3 col-xl-3 mx-auto mt-3">
            <h6 class="text-uppercase mb-4 fw-bold">
              <img src="../../assets/img/navbar_footer/image.png" alt="Логотип" width="60" height="35" />
            </h6>
            <p style="font-family: 'Geologica';">
              Наш сайт — всё о точной и быстрой сегментации печени. Оставайтесь с нами — у нас лучшие решения и технологии!
            </p>
          </div>

          <hr class="w-100 clearfix d-md-none" />
<!--   -->
          <div class="col-md-2 col-lg-2 col-xl-2 mx-auto mt-3">
            <h6 class="text-uppercase mb-4 fw-bold">Ссылки</h6>
            <p>
              <router-link to="/#modelSection" class="text-black-src" style="font-family: 'Geologica';">Модель</router-link>
            </p>
            <p>
              <router-link to="/workspace/" class="text-black-src" style="font-family: 'Geologica';">Рабочая среда</router-link>
            </p>
            <p>
              <router-link to="/auth/register/" class="text-black-src" style="font-family: 'Geologica';">Регистрация</router-link>
            </p>
            
          </div>

          <hr class="w-100 clearfix d-md-none" />

          <div class="col-md-4 col-lg-3 col-xl-3 mx-auto mt-3" style="font-family: 'Geologica';">
            <h6 class="text-uppercase mb-4 fw-bold"> Контакты</h6>
            <p><i class="fas fa-home mr-3"></i> Улица Мира 32</p>
            <p><i class="fas fa-envelope mr-3"></i> info@gmail.com</p>
            <p><i class="fas fa-phone mr-3"></i> + 01 234 567 88</p>
            
          </div>

          <div class="col-md-3 col-lg-2 col-xl-2 mx-auto mt-3">
            <h6 class="text-uppercase mb-4 fw-bold">Наши соц. сети</h6>

            <!-- гит -->
            <a class="btn btn-dark btn-floating m-3" href="#!" role="button"><i class="fab fa-github"></i></a>
            <!-- вкид -->
            <a class="btn btn-primary m-1" href="#!" role="button"><i class="fab fa-vk"></i></a>


          </div>
        </div>
      </section>
    </div>
  </footer>
</template>

<script>
    export default{

    }
</script>