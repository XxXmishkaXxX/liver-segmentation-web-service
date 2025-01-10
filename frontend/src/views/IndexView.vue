<template>
  <div class="container mt-5">
    <div class="row align-items-center gap-200px">
  <div class="text col-md-6 mb-5" style="display: flex; flex-direction: column; justify-content: flex-start;">
    <div class="display-5 text-white" style="font-family: 'Geologica'; font-size: 3.2vh; position: relative;">
      <span style="position: absolute; left: 20%; transform: translateX(-340%); width: 10%; height: 5px; background-color: white; top: 17%;"></span>
      Инновационный сайт, специализирующийся на сегментации печени.
    </div>
    <div class="mt-2 h5" style="font-family: 'Geologica-SemiBold'; color: #858585;">
      мы обеспечиваем медицинских специалистов<br>
      инструментами для анализа и визуализации, чтобы<br>
      повысить качество диагностики и лечения.
    </div>
    <div class="mt-5">
      <router-link to="/auth/register/" >
      <button class="btn btn-outline-light hover-outline" style="width: 250px; height: 60px; border-radius: 30px; color: white; border-color: white; transition: all 0.1s ease;">
        Начать
      </button>
    </router-link>
    </div>
  </div>
  <div class="col-md-4">
    <img src="../assets/img/index/chel.png" alt="" class="img-fluid float-right">
  </div>
</div>
  </div>


  <div style="width: 100%; height: 1px; background-color: white;"></div>

  <div id="aboutSection" class="mt-5">
    <div class="container">
      <div class="row align-items-start">
        <div class="col-auto">
          <img src="../assets/img/index/chb.png" alt="Фото" width="421" height="356">
        </div>
        <div class="col-auto text-white text-end mt-5" style="font-family: 'Geologica'; font-size: 20px; margin-left: 20vh;">
          <p style="max-width: 629px;">
            Мы — молодая и амбициозная команда из УрФУ,
            объединившаяся для создания инновационных решений в
            области медицины. Наш проект — сайт для сегментации
            печени, который упрощает процесс анализа медицинских
            изображений и помогает специалистам быстрее и точнее
            ставить диагнозы. Мы верим, что наша разработка сможет
            сделать диагностику доступнее и повысить её качество.
          </p>
        </div>
      </div>
    </div>
  </div>

  <div class="container mt-5">
    <div class="row align-items-start">
      <div class="col-auto text-white text-start mt-5" style="font-family: 'Geologica'; font-size: 20px;">
        <p style="max-width: 629px;">
          Проект направлен на разработку системы машинного
          обучения для автоматической сегментации контуров
          печени на КТ-снимках. Основная цель — повысить точность
          и скорость диагностики заболеваний печени за счет
          минимизации ошибок в интерпретации снимков, улучшения качества
          сегментации и уменьшения нагрузки на врачей.
        </p>
      </div>
      <div class="col-auto">
        <img src="../assets/img/index/chb2.png" alt="Фото" width="421" height="356" style="margin-left: 20vh;">
      </div>
    </div>
  </div>

  <div style="width: 100%; height: 1px; background-color: white;"></div>

  <div id="modelSection" style="margin-top: 7rem;">
    <div style="width: 80%; height: 1px; background-color: white; margin-left: 20vh;"></div>
  </div>

  <div class="container mt-5">
    <div class="row align-items-start">
      <div class="col-auto text-white text-start mt-5" style="font-family: 'Geologica'; font-size: 18px;">
        <p><img src="../assets/img/index/ai.svg" alt="" class="mx-3">AI-модель</p>
        <p style="max-width: 528px;">
          Проект направлен на разработку системы машинного
          обучения для автоматической сегментации контуров
          печени на КТ-снимках. Основная цель — повысить точность
          и скорость диагностики заболеваний печени за счет
          минимизации ошибок в интерпретации снимков, улучшения качества
          сегментации и уменьшения нагрузки на врачей.
        </p>
      </div>
      <div class="mx-auto" style="width: 1px; height: 421px; background-color: white;"></div>
      <div class="col-auto text-white text-start mt-5" style="font-family: 'Geologica'; font-size: 18px;">
        <p><img src="../assets/img/index/tri.svg" alt="" class="mx-3">Как это работает</p>
        <p style="max-width: 528px;">
          Attention Unet анализирует каждое изображение послойно,
          применяя сложные алгоритмы для выявления даже
          мельчайших деталей и аномалий. В отличие от традиционных
          Unet-архитектур, наш подход с использованием внимания
          позволяет сосредотачиваться именно на тех областях, которые
          наиболее значимы для диагностики, что особенно важно при
          анализе медицинских изображений.
        </p>
      </div>
    </div>
  </div>

  <div style="width: 80%; height: 1px; background-color: white; margin-left: 20vh;"></div>

  <div id="supportSection" style="margin-top: 7rem;">
    <div style="width: 100%; height: 1px; background-color: white;"></div>
  </div>

  <div class="text-center mt-5 text-white">
    <span style="font-family: 'Geologica'; font-size: 36px;">Помогите нам стать лучше!</span>
  </div>

  <div class="container mt-5">
    <div class="row align-items-start">
      <div class="col-auto">
        <img src="../assets/img/index/head.png" alt="Фото" width="440" height="440">
      </div>
      <div class="col-auto text-white text-end mt-5" style="font-family: 'Geologica'; font-size: 20px; margin-left: 20vh;">
        <p style="max-width: 629px;">
          Нашли ошибку в сегментации? Исправьте и помогите нам стать лучше!
          Если вы заметили ошибку в результатах сегментации печени, вы можете исправить её вручную. Отправьте ваш исправленный вариант нам на почту, и это поможет нам улучшить нашу модель. Мы ценим ваш вклад в развитие технологии!
          <br><br>
          Вы можете внести свой вклад в развитие технологии, предоставив свои снимки или исправления сегментации. Каждый предоставленный вами пример поможет нашей модели обучаться и становиться точнее. Отправьте ваши снимки или исправленные результаты сегментации нам на почту — и вместе мы сделаем процесс диагностики ещё эффективнее. Спасибо за вашу помощь и поддержку!
        </p>
      </div>
    </div>
  </div>
</template>

<script>

export default{
}

</script>

<style scoped>
h1 {
  color: #2c3e50;
}

.gap-200px{
  gap: 200px;
}
</style>