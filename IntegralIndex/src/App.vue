<template>
  <div class="app">
    <!-- Заголовок сайта ------------------------------------------------------------------------>
    <div class="header">
      <div class="app">
        <input class="header-cb-transparent" type="checkbox" @click="left_panel_show()" id="id_menu"
          v-model="menu_check" true-value="0" false-value="20" />
        <label for="id_menu" class="header-strips">
          <label for="id_menu" class="strip"></label>
          <label for="id_menu" class="strip"></label>
          <label for="id_menu" class="strip"></label>
        </label>
      </div>
      <div class="header-text">
        <div class="header-title">Интегральный индекс</div>
        <div class="header-exit">
          <div class="save-cur-calc-block">
            <button class="btn-save-cur">
              <div class=btn-calc-text @click="save_current_calc()"> Сохранить текущий расчет</div>
            </button>
          </div>
          <div class="settings-button-block">
            <label for="id_settings" class="header-strips">
              <img class="img-settings" for="id_settings" src="@/settings.png" />
            </label>
            <input class="header-cb-transparent" type="checkbox" id="id_settings" v-model="settings_check"
              true-value="0" false-value="20" />
          </div>
          <div class="exit-label" @click="logout()">Выход</div>
        </div>
      </div>
    </div>
    <!--/Заголовок сайта------------------------------------------------------------------------>

    <!-- Тело ------------------------------------------------------------------------>

    <div class="body">
      <!-- Выпадающее меню слева---------------------------------------------------------------->
      <div v-show="menu_check === '20'">
        <div class="left-panel">
          <h5 class="sub-section-title">
            <label class="checkbox style-c">
              <input type="checkbox" @change="set_all_checkbox()" />
              <div class="checkbox__checkmark"></div>
              <div class="checkbox__body">Выбрать все</div>
            </label>
          </h5>
          <h4 class="glob-section-title">
            {{ reliability_section.title }}
          </h4>
          <h5 class="sub-section-title">
            <label class="checkbox style-c">
              <input type="checkbox" v-model="reliability_section.check" />
              <div class="checkbox__checkmark"></div>
              <div class="checkbox__body">Надежность</div>
            </label>
          </h5>
          <div v-for="bgsec_name in big_sections_name" :key=bgsec_name>
            <div>
              <h4 class="glob-section-title">
                {{ bgsec_name.name }}
              </h4>
              <div v-for="sec in sections" :key=sec>
                <div v-if="sec.section === bgsec_name.name">
                  <h5 class="sub-section-title">
                    <label :for=sec.name class="checkbox style-c">
                      <input type="checkbox" :id=sec.name v-model="sec.check" />
                      <div class="checkbox__checkmark"></div>
                      <div class="checkbox__body">{{ sec.title }}</div>
                    </label>
                  </h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- /Выпадающее меню слева--------------------------------------------------------------->


      <!-- Меню настроек---------------------------------------------------------------->
      <div v-show="settings_check === '20'">
        <div class="right-panel">
          <h1 class="settings-title">Настройка параметров здания</h1>

          <!-------Основные настройки------------------------->
          <h1 class="settings-param-name">Этажность здания</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.floors">

          <h1 class="settings-param-name">Длина здания, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.length_build">

          <h1 class="settings-param-name">Ширина здания, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.width_build">

          <h1 class="settings-param-name">Длина стен на одном этаже, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.length_wall">

          <h1 class="settings-param-name">Высота стен на одном этаже, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.height_wall">

          <h1 class="settings-param-name">Материал стен</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.walls_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Температура внутреннего воздуха, °С</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.temp_inside">

          <h1 class="settings-param-name">Температура наружного воздуха, °С</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.temp_outside">

          <h1 class="settings-param-name">Дата постройки</h1>
          <input class="settings-param-input" type="date" v-model="parametrs_of_build.date_construction">

          <!--- Настройки окон----------------------------->
          <h1 class="settings-param-name">Число окон в здании</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_windows">

          <h1 class="settings-param-name">Длина типового окна, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.length_windows">

          <h1 class="settings-param-name">Высота типового окна, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.height_windows">

          <h1 class="settings-param-name">Дата установки окон</h1>
          <input class="settings-param-input" type="date" v-model="parametrs_of_build.date_windows">

          <h1 class="settings-param-name">Тип окон</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.type_windows">
            <option v-for="(type_item) in type_windows" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <!--------------- Двери ------------------------------>
          <h1 class="settings-param-name">Число дверей </h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_doors">

          <h1 class="settings-param-name">Длина типовой входной двери, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.length_doors">

          <h1 class="settings-param-name">Высота типовой входной двери, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.height_doors">

          <h1 class="settings-param-name">Тип дверей </h1>
          <select class="settings-param-input" v-model="parametrs_of_build.type_doors">
            <option v-for="(type_item) in type_doors" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Материал дверей</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.doors_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Дата установки дверей</h1>
          <input class="settings-param-input" type="date" v-model="parametrs_of_build.date_doors">

          <h1 class="settings-param-name">Класс энергетической эффективности </h1>
          <h1 class="settings-param-name">ограждающих конструкций </h1>
          <select class="settings-param-input" v-model="parametrs_of_build.class_energoeff">
            <option v-for="(type_item) in class_energoeff" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Материал пола</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.floors_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <!-- Мебель и жильцы--------------------------------------------->

          <h1 class="settings-param-name">Материал мебели</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.furniture_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Число шкафов</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_closet">

          <h1 class="settings-param-name">Число диванов</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_sofa">

          <h1 class="settings-param-name">Материал диванов</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.sofa_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Число столов</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_table">

          <h1 class="settings-param-name">Материал столов</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.table_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Число навесных шкафчиков</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_small_closet">

          <h1 class="settings-param-name">Максимальное число посетителей мужчин</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_men">

          <h1 class="settings-param-name">Максимальное число посетителей женщин</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_women">

          <h1 class="settings-param-name">Максимальное число посетителей детей</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_children">

          <h1 class="settings-param-name">Среднее время пребывания посетителей</h1>
          <h1 class="settings-param-name">в сутки, ч</h1>
          <input class="settings-param-input" type="number" min=0 max=24 v-model="parametrs_of_build.time_guests">

          <h1 class="settings-param-name">Количество помещений с раковинами </h1>
          <h1 class="settings-param-name">на этаже</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_sink">

          <h1 class="settings-param-name">Тип трубы</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.type_pipe">
            <option v-for="(type_item) in type_pipe" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

          <h1 class="settings-param-name">Высота подвала, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.height_basement">

          <h1 class="settings-param-name">Период энергосбережения</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.period_energosave">
            <option v-for="(type_item) in period_energosave" :value="type_item.id" :key=type_item.id readonly>
              {{ type_item.val }}
            </option>
          </select>

        </div>
      </div>
      <!-- /Меню настроек--------------------------------------------------------------->
      <!-- Основное рабочее пространство  ----------------------------------------------------->
      <div :style="{ 'width': 100 + '%' }">
        <div class="solution" :style="{ 'padding-left': menu_check + '%' }">

          <!--- Блок выбра шаблона и года--------------------------------->
          <div class="choise-years-text-title"> Выбор отопительного сезона</div>
          <div class="block-pat-years">
            <select class="header-selector" @change="import_from_server()" v-model="parametrs_of_build.id_build">
              <option v-for="(build) in name_build" :value="build.id" :key=build.id>
                {{ build.val }}
              </option>
            </select>
            <select class="header-selector" @change="clear_results()" id="years-selector">
              <option> Тестовая дата - 01.09.2022</option>
              <option> 2014-15 - самая тёплая зима</option>
              <option> 2018-19</option>
              <option> 2019-20</option>
              <option> 2020-21 - самая холодная зима</option>
              <option> 2021-22</option>
              <option> 2022-23</option>
            </select>
          </div>
          <!--- Блок выбра шаблона и года--------------------------------->

          <!-- Блок с расчетом суммарных притоков и потерь -->
          <div class="sum-block">
            <div>
              <div id="sum-minus">
                <div class="block-title"> Теплопотери</div><br>
                <div class="block-suptitles"> Потери через ограждающие конструкции (трансмиссионные)<br>
                  <hr><br>
                </div>
                <div class="flex-between">
                  <div class="sum-titles">
                    <h2> окна</h2>
                    <h2> входная группа (двери)</h2>
                    <h2> стены</h2>
                    <h2> кровля</h2>
                    <h2> пол и фундамент</h2>
                  </div>
                  <div v-if="results.heat_los_win != ''" class="sum-results">
                    <h2>{{ printVal(results.heat_los_win, 'Гкал') ?? "" }} </h2>
                    <h2>{{ printVal(results.heat_los_inpgr, 'Гкал') ?? "" }} </h2>
                    <h2>{{ printVal(results.heat_los_heatcond_benv, 'Гкал') ?? "" }} </h2>
                    <h2>{{ printVal(results.heat_los_heatcond_roof, 'Гкал') ?? "" }} </h2>
                    <h2>{{ printVal(results.heat_los_floor, 'Гкал') ?? "" }} </h2>
                  </div>
                </div>
                <div class="block-suptitles"> <br> Потери инфильтрационные<br>
                  <hr><br>
                </div>
                <div class="flex-between">
                  <div class="sum-titles">
                    <h2> окна </h2>
                    <h2> входная группа (двери) </h2>
                    <h2> ограждающие конструкции с учётом ветровой нагрузки</h2>
                    <h2> система естественной вентиляции </h2>
                  </div>
                  <div v-if="results.inf_win != ''" class="sum-results">
                    <h2>{{ printVal(results.inf_win, 'Гкал') ?? "" }} </h2>
                    <h2> {{ printVal(results.inf_inpgr, 'Гкал') ?? "" }} </h2>
                    <h2 style="color: var(--global-fon); margin:0"> space</h2>
                    <h2 v-if="results.inf_inpgr != ''"> 100.217 Гкал </h2>
                    <h2>{{printVal(results.heat_los_vent, 'Гкал') ?? "" }}</h2>
                  </div>
                </div>
                <div class="flex-between">
                  <div class="sum-titles">
                    <br>
                    <h2 style="font-weight: 600;"> Прогрев здания перед рабочим днем </h2>
                    <hr><br>
                  </div>
                  <div v-if="results.add_heatcosts != ''" class="sum-results">
                    <br>
                    <h2>{{ printVal(results.add_heatcosts, 'Гкал') ?? "" }}</h2><br>
                  </div>
                </div>
              </div>

              <div id="sum-plus">
                <div class="block-title"> Теплопритоки</div><br>
                <div class="block-suptitles" style="color: var(--global-fon); margin:0"> space<br><br></div>
                <div class="sum-titles">
                  <h2> от людей </h2>
                  <h2> от магистральных трубопроводов и стояков ГВС к рукомойникам</h2>
                  <h2> от магистральных трубопроводов и стояков ГВС к душевым</h2>
                  <h2> от электрооборудования </h2>
                  <h2> от неизолированных трубопроводов ГВС</h2>
                  <h2> от неизолированных трубопроводов отопления</h2>
                </div>

                <div v-if="results.heat_gains_people != ''" class="sum-results">
                  <h2>{{ printVal(results.heat_gains_people, 'Гкал') ?? "" }} </h2>
                  <h2 style="color: var(--global-fon); margin:0"> space</h2>
                  <h2>{{ printVal(results.heat_gains_washstands, 'Гкал') ?? "" }} </h2>
                  <h2 style="color: var(--global-fon); margin:0"> space</h2>
                  <h2>{{ printVal(results.heat_gains_showers, 'Гкал') ?? "" }} </h2>
                  <h2>{{ printVal(results.heat_gains_electriclighting, 'Гкал') ?? "" }}</h2>
                  <h2>{{ printVal(results.heat_gains_GVS, 'Гкал') ?? "" }}</h2>
                  <h2 style="color: var(--global-fon); margin:0"> space</h2>
                  <h2>{{ printVal(results.heat_gains_pipelines, 'Гкал') ?? "" }}</h2>
                </div>
              </div>
            </div>

            <!-- Вывод суммарных теплопотерь и теплопритоков --------------------------------------->
            <div v-if="dop_results.sum_add != '' && dop_results.sum_los != ''" class="flex-between borders">
              <div class="flex-between flex-between-sumlos">
                <div class="sum-text-text"> &Sum; <sub>теплопотерь</sub></div>
                <div class="sum-text-res"> {{ printVal(dop_results.sum_los, 'Гкал') }} </div>
              </div>
              <div class="flex-between flex-between-sumadd">
                <div class="sum-text-text"> &Sum; <sub>теплопритоков</sub></div>
                <div class="sum-text-res"> {{ printVal(dop_results.sum_add, 'Гкал') }} </div>
              </div>
            </div>
            <!-- /Вывод суммарных теплопотерь и теплопритоков --------------------------------------->
          </div>
          <!-- Конец блока c расчетом суммарных притоков и потерь ------------------------------------------------------------->

          <!-- Пространство кнопок расчетов  ------------------------------------------------------>
          <div class="buttons-for-calc">
            <!-- Формульный расчет по СП -->
            <div class="math-calc-block">
              <div class="flex-between">
                <button class="btn-calc" @click="calc_all()">
                  <div class=btn-calc-text> Формульный расчет по СП 50.13330.2012</div>
                </button>
                <a @click="download_excel()" class="btn-calc btn-download" href="#">
                  <img class="img-download" src="@/download.png">
                </a>
              </div>
            </div>

            <!-- Расчет искусственной нейронной сетью -->
            <div class="math-calc-block-INS">
              <div class="flex-between">

                <button class="btn-calc btn-calc-INS" @click="calc_INS()">
                  <div class=btn-calc-text id="neuro_calc_id"> Расчет искусственной нейронной сетью </div>
                </button>

                <select class="select-INS" v-model="ins_model" id="neuro_select_id">
                  <option value=1>128-128-128 50 MAE sigmoid 0.6%</option>
                  <option value=2>64-256 100 MAE tanh 7.8%</option>
                  <option value=3>64-256 150 MAE tanh 7.9%</option>
                  
                  <option value=4>A - 256-64  50 MSE sigmoid 1.3%</option>
                  <option value=5>A - 256-64 50 MSE tanh 1.79%</option>
                  <option value=6>A - 256-256  100 MSE tanh 1.72%</option>
                  <option value=7>Е - 256-256  100 MAPE sigmoid 1,33%</option>
                  <option value=8>Е - 256-256  100 MАE sigmoid 0,71%</option>
                  <option value=9>Е - 256-256  100 MАE tanh  0,89%</option>
                </select>

                <a @click="download_excel()" class="btn-calc btn-download" href="#" :download=url_to_download_math>
                  <img class="img-download" src="@/download.png">
                </a>
              </div>
            </div>

            <!-- Отпуск тепловой энергии ТЭЦ -->
            <div class="math-calc-block math-calc-block-CTP">
              <button class="btn-calc btn-TC" @click="calc_tec()">
                <div class=btn-calc-text> Расчет ТЭЦ и ЦТП </div>
              </button>
            </div>
          </div>
          <!-- /Пространство кнопок расчетов---------------------------------------------------->


          <div v-if="showResults === true" class="sum-block">
            <div>
              <div id="sum-minus">
                <div class="block-title"> Результаты расчётов</div><br>
                <div v-if="dop_results.razn_los_add != ''" class="res-subblock">
                  <div class="block-suptitles"> Формульный расчет по СП 50.13330.2012 <br>
                    <hr><br>
                  </div>
                  <div class="flex-between">
                    <div class="sum-titles">
                      <h2> Разница теплопотерь и теплопритоков</h2>
                    </div>
                    <div class="sum-results">
                      <h2>{{ printVal(dop_results.razn_los_add, 'Гкал') ?? "" }} </h2>
                    </div>
                  </div>
                </div>

                <div v-if="results.ins != ''" class="res-subblock">
                  <div class="block-suptitles"> Расчет искуственной нейронной сетью <br><hr><br></div>
                  <div class="flex-between">
                    <div class="sum-titles">
                      <h2> Разница теплопотерь и теплопритоков</h2>
                    </div>
                    <div class="sum-results">
                      <h2>{{ printVal(results.ins, 'Гкал') ?? "" }} </h2>
                    </div>
                  </div>
                </div>

                <div v-if="dop_results.razn_tec_ctp !== ''" class="res-subblock">
                  <div class="block-suptitles"> Расчет ТЭЦ и ЦТП <br><hr><br></div>
                  <div class="flex-between">
                    <div class="sum-titles">
                      <h2> ТЭЦ</h2>
                      <h2> ЦТП</h2>
                      <h2> Разница ТЭЦ и ЦТП</h2>
                    </div>
                    <div class="sum-results">
                      <h2>{{ printVal(results.tec, 'Гкал') ?? "" }} </h2>
                      <h2>{{ printVal(results.ctp, 'Гкал') ?? "" }} </h2>
                      <h2>{{ printVal(dop_results.razn_tec_ctp, 'Гкал') ?? "" }} </h2>
                    </div>
                  </div>
                </div>
              </div>

              <div id="sum-plus">
                <div class="block-title"> Экологический ущерб</div><br>
                <div v-if="dop_results.razn_los_add != ''" class="res-subblock">
                  <div class="block-suptitles"> Формульный расчет по СП 50.13330.2012 <br>
                    <hr><br>
                  </div>
                  <div class="flex-between">       
                    <h2>{{ printVal(dop_results.eclg_sp_tut, 'т.у.т')  ?? "" }} </h2>
                    <h2>{{ printVal(dop_results.eclg_sp_co2, 'кг CO2/год') ?? "" }} </h2>    
                 </div>
                </div>

                <div v-if="results.ins != ''" class="res-subblock">
                  <div class="block-suptitles"> Расчет искуственной нейронной сетью <br><hr><br></div>
                  <div class="flex-between">
                    <h2>{{ printVal(dop_results.eclg_ins_tut, 'т.у.т') ?? "" }} </h2>
                    <h2>{{ printVal(dop_results.eclg_ins_co2, 'кг CO2/год') ?? "" }} </h2>
                  </div>
                </div>

                <div v-if="dop_results.razn_tec_ctp !== ''" class="res-subblock">
                  <div class="block-suptitles"> Расчет ТЭЦ и ЦТП <br><hr><br></div>
                  <div class="flex-between">
                    <h2>{{ printVal(dop_results.eclg_tec_ctp_tut, 'т.у.т') ?? "" }} </h2>
                    <h2>{{ printVal(dop_results.eclg_tec_ctp_co2, 'кг CO2/год') ?? "" }} </h2>
                  </div>
                </div>
              </div>
            </div>
            <!-- <h1>: Разница теплопотерь и теплопритоков</h1>  -->
          </div>

          <!--Отрисовка информационных блоков--------------------------------------------------->
          <div v-if="show_dop_info_title" class="informations-glob-title"> Дополнительная информация о расчетах </div>
          <!-- Надежность -->
          <div v-show="reliability_section.check">
            <div class="mega-block-title"> {{ reliability_section.title }} </div>
            <div class="mega-block-sections">
              <div class="collection-reliability">
                <div class="parametrs-info-block-borders rel-param-info-borders">
                  <div class="mega-block-subtitle"> Тепловой пункт </div>
                  <div class="parametrs-info-block">
                    <input class="info-values" type="radio" id='elev' name="elev-itp-radio" value=1
                      v-model="parametrs_of_reliability.elev_itp">
                    <label class="info-text" for="elev">Элеватор</label>
                  </div>
                  <div class="parametrs-info-block">
                    <input class="info-values" type="radio" id='itp' name="elev-itp-radio" value=0
                      v-model="parametrs_of_reliability.elev_itp">
                    <label class="info-text" for="itp">ИТП</label>
                  </div>
                  <div v-if="parametrs_of_reliability.elev_itp == 0">
                    <div class="parametrs-info-block">
                      <div class="info-text"> Тип насоса</div>
                      <select class="info-values" v-model="parametrs_of_reliability.type_pump">
                        <option v-for="(type_item) in type_pump" :value="type_item.id" :key=type_item.id readonly>
                          {{ type_item.val }}
                        </option>
                      </select>
                    </div>
                    <div class="parametrs-info-block">
                      <div class="info-text"> Тип теплообменника</div>
                      <select class="info-values" v-model="parametrs_of_reliability.type_heatexchanger">
                        <option v-for="(type_item) in type_heatexchanger" :value="type_item.id" :key=type_item.id
                          readonly>
                          {{ type_item.val }}
                        </option>
                      </select>
                    </div>
                  </div>
                  <div class="parametrs-info-block">
                    <input class="info-values" type="checkbox" id='vetsys' v-model="parametrs_of_reliability.ventsys"
                      true-value='1' false-value='0'>
                    <label class="info-text" for="vetsys">Наличие подогрева приточного воздуха</label>
                  </div>
                  <div v-if="parametrs_of_reliability.ventsys === 1 || parametrs_of_reliability.ventsys === '1'">
                    <div class="mega-block-subtitle"> Система подогрева приточного воздуха </div>
                    <div class="parametrs-info-block">
                      <div class="info-text"> Число установок</div>
                      <input class="info-values" type="number" min=0 max=100
                        v-model="parametrs_of_reliability.count_installations">
                      <div class="info-text"> ед </div>
                    </div>
                    <div class="parametrs-info-block">
                      <div class="info-text"> Длина трубы от ТП до установки №1</div>
                      <input class="info-values" type="number" min=0 max=100
                        v-model="parametrs_of_reliability.length_pipe1">
                      <div class="info-text"> м </div>
                    </div>
                    <div class="parametrs-info-block">
                      <div class="info-text"> Длина трубы от ТП до установки №2</div>
                      <input class="info-values" type="number" min=0 max=100
                        v-model="parametrs_of_reliability.length_pipe2">
                      <div class="info-text"> м </div>
                    </div>
                  </div>
                  <div class="mega-block-subtitle"> Система ГВС с рециркуляцией </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Число подъёмов ГВС</div>
                    <input class="info-values" type="number" min=0 max=100
                      v-model="parametrs_of_reliability.count_up_hws">
                    <div class="info-text"> ед </div>
                  </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Число опусков ГВС</div>
                    <input class="info-values" type="number" min=0 max=100
                      v-model="parametrs_of_reliability.count_down_hws">
                    <div class="info-text"> ед </div>
                  </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Число кранов на каждом этаже (от одного опуска)</div>
                    <input class="info-values" type="number" min=0 max=100
                      v-model="parametrs_of_reliability.count_crane">
                    <div class="info-text"> ед </div>
                  </div>
                  <div class="mega-block-subtitle"> Система отопления здания </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Число подъёмов от ТП до чердака</div>
                    <input class="info-values" type="number" min=0 max=100
                      v-model="parametrs_of_reliability.count_up_loft">
                    <div class="info-text"> ед </div>
                  </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Число опусков от чердака до ТП</div>
                    <input class="info-values" type="number" min=0 max=100
                      v-model="parametrs_of_reliability.count_down_loft">
                    <div class="info-text"> ед </div>
                  </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Число отопительных приборов на этаже (от одного опуска)</div>
                    <input class="info-values" type="number" min=0 max=100
                      v-model="parametrs_of_reliability.count_radiator">
                    <div class="info-text"> ед </div>
                  </div>
                  <div class="mega-block-subtitle"> Параметры здания</div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Тип запорной арматуры</div>
                    <select class="info-values" v-model="parametrs_of_reliability.type_armature">
                      <option v-for="(type_item) in type_armature" :value="type_item.id" :key=type_item.id readonly>
                        {{ type_item.val }}
                      </option>
                    </select>
                  </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Тип трубы</div>
                    <select class="info-values" v-model="parametrs_of_reliability.type_pipe">
                      <option v-for="(type_item) in type_pipe" :value="type_item.id" :key=type_item.id readonly>
                        {{ type_item.val }}
                      </option>
                    </select>
                  </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Тип радиатора</div>
                    <select class="info-values" v-model="parametrs_of_reliability.type_radiator">
                      <option v-for="(type_item) in type_radiator" :value="type_item.id" :key=type_item.id readonly>
                        {{ type_item.val }}
                      </option>
                    </select>
                  </div>
                  <div class="parametrs-info-block">
                    <div class="info-text"> Тип крана</div>
                    <select class="info-values" v-model="parametrs_of_reliability.type_crane">
                      <option v-for="(type_item) in type_crane" :value="type_item.id" :key=type_item.id readonly>
                        {{ type_item.val }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="results-info-block-borders">
                <div v-if="results.reliability !== ''">
                  <div class="info-text"> Результаты расчетов </div>
                  <div class="info-text"> {{ printVal(results.reliability * 100, '%') }} </div>
                </div>
                <button class="btn-calc" @click="calc_reliability()" style="position:sticky; top: 90%; bottom: 10%;">
                  Выполнить расчет</button>
              </div>
            </div>
          </div>

          <div v-for="(section, index_section) in sections" :key=index_section>
            <div v-show="section.check">
              <div class="mega-block-title"> {{ section.title }} </div>
              <div class="mega-block-sections">
                <div class="parametrs-info-block-borders">
                  <div class="mega-block-subtitle"> {{ section.subtitle }} </div>
                  <div v-for="(item, index) in section.title_fields" :key=index>
                    <div v-if="section.value_fields[index] == 'class_energoeff'" class="parametrs-info-block"
                      style="flex-direction: column">
                      <div class="info-text"> {{ item }} </div>
                      <div class="info-values">
                        {{ printInfoVal(section.value_fields[index]) }}
                      </div>
                    </div>
                    <div v-else class="parametrs-info-block">
                      <div class="info-text"> {{ item }} </div>
                      <div class="info-values">
                        {{ printInfoVal(section.value_fields[index]) }}
                      </div>
                      <div class="info-text"> {{ section.ue_fields[index] }} </div>
                    </div>
                  </div>
                </div>
                <div v-if="results[section.name] !== ''" class="results-info-block-borders">
                  <div class="info-text"> Результаты расчетов </div>
                  <div class="info-text"> {{ printVal(results[section.name], 'Гкал') }} </div>
                </div>
              </div>
            </div>
          </div>
          <!--/Отрисовка информационных блоков--------------------------------------------------->
        </div> <!--solution-->
      </div> <!--/ Основное рабочее пространство-->
    </div> <!--body-->
    <!--/Тело ----------------------------------------------------------------------->

    <dialogbox-login v-model:show=login_reg_check>
    </dialogbox-login>
    <dialogbox-reg v-model:show=login_reg_check>
    </dialogbox-reg>
    <!-- модальное окно вывода прогресса расчетов p.s. в идеале было сделать в виде отдельного компонента, но у меня не получилось :( -->
    <div class="progress-window" v-if="showProgress">
      <div class="progress-main">
        <h1 id='loading_name'>Выполняется расчёт</h1>
        <h1 id='loading_calc'>Прогресс</h1>
      </div>
    </div>
    <!-- модальное окно -->
  </div>
</template>

<script src='@/scripts.js'>
</script>