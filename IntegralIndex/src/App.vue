<template>
  <div class="app">
    <!-- Заголовок сайта ------------------------------------------------------------------------>
    <div class="header"> 
      <div class="app">
        <input   class="header-cb-transparent" type="checkbox" @click="left_panel_show()" id="id_menu" v-model="menu_check" true-value="0" false-value="20"/>
        <label   for="id_menu" class="header-strips">
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
            <label for="id_settings" class="header-strips" >
                <img class="img-settings" for="id_settings" src="@/settings.png" /> 
            </label>
            <input class="header-cb-transparent" type="checkbox" id="id_settings" v-model="settings_check" true-value="0" false-value="20"/> 
          </div>  
          <div class="exit-label" @click="logout()">Выход</div>  
        </div>
      </div>
    </div>
    <!--/Заголовок сайта------------------------------------------------------------------------>
    
    <!-- Тело ------------------------------------------------------------------------>
    
    <div class="body">  
      <!-- Выпадающее меню слева---------------------------------------------------------------->
      <div v-show="menu_check==='20'">
        <div class="left-panel">
          <h5 class="sub-section-title">  
            <label class="checkbox style-c">
              <input type="checkbox" @change="set_all_checkbox()" />
              <div class="checkbox__checkmark"></div>
              <div class="checkbox__body">Выбрать все</div>
            </label>
          </h5>
          <h4  class="glob-section-title">
                {{reliability_section.title}}
          </h4>
          <h5 class="sub-section-title">  
            <label class="checkbox style-c">
              <input type="checkbox" v-model="reliability_section.check"  />
              <div class="checkbox__checkmark"></div>
              <div class="checkbox__body">Надежность</div>
            </label>
          </h5>
          <div v-for="bgsec_name in big_sections_name" :key=bgsec_name>
            <div>
              <h4  class="glob-section-title">
                {{bgsec_name.name}}
              </h4>
              <div v-for="sec in sections" :key=sec>
                <div v-if="sec.section===bgsec_name.name">
                  <h5 class="sub-section-title">  
                    <label :for=sec.name class="checkbox style-c">
                      <input type="checkbox" :id=sec.name v-model="sec.check" />
                      <div class="checkbox__checkmark"></div>
                      <div class="checkbox__body">{{sec.title}}</div>
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
      <div v-show="settings_check==='20'">
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
              {{type_item.val}}
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
              {{type_item.val}}
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
              {{type_item.val}}
            </option> 
          </select>

          <h1 class="settings-param-name">Материал дверей</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.doors_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
            </option> 
          </select>
          
          <h1 class="settings-param-name">Дата установки дверей</h1>
          <input class="settings-param-input" type="date" v-model="parametrs_of_build.date_doors">

          <h1 class="settings-param-name">Класс энергетической эффективности </h1>
          <h1 class="settings-param-name">ограждающих конструкций </h1>   
          <select class="settings-param-input" v-model="parametrs_of_build.class_energoeff">
            <option v-for="(type_item) in class_energoeff" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
            </option> 
          </select>

          <h1 class="settings-param-name">Материал пола</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.floors_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
            </option> 
          </select>

          <!-- Мебель и жильцы--------------------------------------------->

          <h1 class="settings-param-name">Материал мебели</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.furniture_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
            </option> 
          </select>

          <h1 class="settings-param-name">Число шкафов</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_closet">

          <h1 class="settings-param-name">Число диванов</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_sofa">

          <h1 class="settings-param-name">Материал диванов</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.sofa_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
            </option> 
          </select>

          <h1 class="settings-param-name">Число столов</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_table">

          <h1 class="settings-param-name">Материал столов</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.table_material">
            <option v-for="(type_item) in materials" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
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
          <h1 class="settings-param-name">в сутки</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.time_guests">

          <h1 class="settings-param-name">Количество помещений с раковинами </h1>
          <h1 class="settings-param-name">на этаже</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.count_sink">

          <h1 class="settings-param-name">Тип трубы</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.type_pipe">
            <option v-for="(type_item) in type_pipe" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
            </option> 
          </select>

          <h1 class="settings-param-name">Высота подвала, м</h1>
          <input class="settings-param-input" type="text" v-model.number="parametrs_of_build.height_basement">

          <h1 class="settings-param-name">Период энергосбережения</h1>
          <select class="settings-param-input" v-model="parametrs_of_build.period_energosave">
            <option v-for="(type_item) in period_energosave" :value="type_item.id" :key=type_item.id readonly>
              {{type_item.val}}
            </option> 
          </select>

        </div> 
      </div>
      <!-- /Меню настроек--------------------------------------------------------------->
      

      <!-- Основное рабочее пространство  ----------------------------------------------------->
      <div :style="{'width': 100+'%'}">
        <div class="solution" :style="{'padding-left': menu_check+'%'}">

          <!--- Блок выбра шаблона и года--------------------------------->
          <div class="choise-years-text-title"> Выбор отопительного сезона</div>
          <div class="block-pat-years">
              <select class="header-selector" @change="import_from_server()" v-model="parametrs_of_build.id_build">
                <option v-for="(build) in name_build" :value="build.id" :key=build.id >
                  {{build.val}} 
                </option>
              </select>     
              <select class="header-selector" @change="clear_dop_results()" id="years-selector">
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
          <div class="sum-block" >
            <div>
              <div id="sum-minus">
                <div class="block-title"> Теплопотери</div><br> 
                <div class="sum-titles">
                  <h1> трансмиссионные через окна <sub> </sub> </h1>
                  <h1> инфильтрационные через окна  <sub> </sub></h1>
                  <h1> трансмиссионные через входную группу<sub> </sub></h1>
                  <h1> инфильтрационные через входную группу<sub> </sub></h1>
                  <h1> теплопроводность через стены<sub> </sub></h1>
                  <h1> теплопроводность через кровлю<sub> </sub></h1>
                  <h1> теплопроводность через пол<sub> </sub></h1>
                  <h1> через систему вытяжной вентиляции <sub> </sub> </h1>
                  <h1> прогрев здания перед рабочим днем <sub> </sub></h1>
                </div>  
                <div class="sum-results">
                  <div v-if="results.heat_los_win != ''">
                    <h1><sub> {{printVal(results.heat_los_win, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.inf_win, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.heat_los_inpgr, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.inf_inpgr, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.heat_los_heatcond_benv, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.heat_los_heatcond_roof, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.heat_los_floor, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.heat_los_vent, 'Гкал')}}  </sub> </h1>
                    <h1><sub> {{printVal(results.add_heatcosts, 'Гкал')}} </sub> <sub></sub> </h1> 
                  </div>
                </div>              
              </div>            
              <div id="sum-plus">
                <div class="block-title"> Теплопритоки</div><br> 
                <div class="sum-titles">
                  <h1> от людей <sub> </sub></h1>
                  <h1> от ГВС рукомойников <sub> </sub></h1>
                  <h1> от ГВС душевых <sub> </sub></h1>
                  <h1> от электрооборудования <sub> </sub></h1>
                  <h1> от неизолированных трубопроводов ГВС<sub> </sub></h1>
                  <h1> от неизолированных трубопроводов отопления<sub> </sub></h1>
                </div>
                
                <div class="sum-results">
                  <div v-if="results.heat_gains_people != ''">
                    <h1><sub>{{printVal(results.heat_gains_people, 'Гкал')}} </sub> </h1>
                    <h1><sub>{{printVal(results.heat_gains_washstands, 'Гкал')}} </sub> </h1>
                    <h1><sub>{{printVal(results.heat_gains_showers, 'Гкал')}} </sub> </h1>
                    <h1><sub>{{printVal(results.heat_gains_electriclighting, 'Гкал')}} </sub> </h1>
                    <h1><sub>{{printVal(results.heat_gains_GVS, 'Гкал')}} </sub> </h1>
                    <h1><sub>{{printVal(results.heat_gains_pipelines, 'Гкал')}} </sub> </h1>
                    <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                    <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                    <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                  </div>
                </div>                            
              </div> 
            </div>

            <!-- Вывод суммарных теплопотерь и теплопритоков --------------------------------------->
            <div v-if="dop_results.sum_los !== ''" >
              <h1 style="color:var(--white-text-color)">.</h1>
              <div class="flex-between">
                <hr style="width: 45%; margin-left:4%; margin-right:2%;">
                <hr style="width: 45%; margin-right:4%">
              </div>
              <div class="flex-between">         
                <div style="width: 45%; margin-left: 4%; margin-right: 0;" class="flex-between">
                  <div>
                    <h1 class="sum-text"> &Sum;<sub style="font-size:20px">теплопотерь</sub></h1>   
                  </div>
                  <div> 
                    <h1 class="sum-text"> <sub> {{printVal(dop_results.sum_los, 'Гкал')}} </sub> </h1>
                  </div>
                </div>
                <div style="width: 45%; margin-right:4%;" class="flex-between">
                  <div> 
                    <h1 class="sum-text"> &Sum;<sub style="font-size:20px">теплопритоков</sub> </h1> 
                  </div>
                  <div>
                    <h1 class="sum-text"> <sub> {{printVal(dop_results.sum_add, 'Гкал')}} </sub> </h1>
                  </div> 
                </div>
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

              <div v-if="dop_results.razn_los_add != ''">
                <input class="output-field" type="text" :value="printVal(dop_results.razn_los_add, 'Гкал')" readonly>
                <p class="comment-text">Разница теплопотерь и теплопритоков</p> 
              </div>         
            </div>

            <!-- Расчет искусственной нейронной сетью -->
            <div class="math-calc-block">
              <div class="flex-between">   

                <div style="display: block;">
                  <button class="btn-calc" style="width: 100%" @click="calc_INS()">
                    <div class=btn-calc-text id="neuro_calc_id"> Расчет искусственной нейронной сетью </div>
                  </button>     
                  
                  <!-- <select v-if="choise_NM == true" class="btn-calc" style="width: 100%; margin: 8px; margin-left:0; margin-right: 0;">
                    <option>Модель 1</option>
                    <option>Модель 2</option>
                    <option>Модель 3</option>
                  </select> -->
                </div>

                <a @click="download_excel()" class="btn-calc btn-download" href="#" :download=url_to_download_math> 
                    <img class="img-download" src="@/download.png"> 
                </a> 
              </div>
              <input v-if="results.ins1 !== ''" class="output-field" type="text" :value="printVal(results.ins1, 'Гкал')" readonly>         
            </div>

            <!-- Отпуск тепловой энергии ТЭЦ -->
            <div class="math-calc-block">
              <button class="btn-calc btn-TC" @click="calc_tec()">
                <div class=btn-calc-text> Отпуск тепловой энергии ТЭЦ </div>
              </button>    
              <div v-if="results.tec != ''">      
                <input class="output-field" type="text" :value="printVal(results.tec, 'Гкал')" readonly>  
                <p class="comment-text">Расчет ТЭЦ</p>
              </div>         
            </div>

            <!-- Потребление тепловой энергии от ЦТП  -->
            <div class="math-calc-block">                
              <button class="btn-calc btn-TC" @click="calc_ctp()">
                <div class=btn-calc-text> Потребление тепловой энергии от ЦТП </div>
              </button> 
              <div v-if="results.ctp != ''">
                <input class="output-field" type="text" :value="printVal(results.ctp, 'Гкал')" readonly>                
                <p class="comment-text">Расчет ЦТП</p>  
              </div>     
            </div>
          </div>   

          <div class="razn-TC-CTP-block" v-if="(dop_results.razn_tec_ctp !== '')">
            <input class="output-field" type="text" :value="printVal(dop_results.razn_tec_ctp, 'Гкал')" readonly>
            <p class="comment-text">Разница ТЭЦ и ЦТП</p>    
          </div>

          <!-- Экологический ущерб ------------------------>
          <div class="ecology-block" v-if="(dop_results.razn_los_add !== '') || (dop_results.razn_tec_ctp !== '')">
            <p class="block-title">Экологический ущерб </p> 
            <div class="flex-between">
              <div v-if="(dop_results.razn_los_add !== '')" class="math-calc-block">
                <input class="output-field" type="text" :value="printVal(dop_results.eclg_sp_tut, 'т.у.т')" readonly>
                <input class="output-field" type="text" :value="printVal(dop_results.eclg_sp_co2, 'кг CO2/год')" readonly>
              </div>

              <div v-if="(dop_results.razn_tec_ctp !== '')" class="math-calc-block">
                <input class="output-field"  type="text" :value="printVal(dop_results.eclg_tec_ctp_tut, 'т.у.т')" readonly>
                <input class="output-field"  type="text" :value="printVal(dop_results.eclg_tec_ctp_co2, 'кг СО2/год')" readonly> 
              </div>
            </div>
          </div>       
          <!-- /Экологический ущерб ------------------------>
          <!-- /Пространство кнопок расчетов---------------------------------------------------->
          

          <!--Отрисовка информационных блоков--------------------------------------------------->
          <div v-if="show_dop_info_title" class="informations-glob-title"> Дополнительная информация о расчетах </div>
          <!-- Надежность -->
          <div v-show="reliability_section.check">
            <div class="mega-block-title"> {{reliability_section.title}} </div>
               <div class="mega-block-sections">
                  <div class="collection-reliability">
                    <div class="parametrs-info-block-borders rel-param-info-borders">   
                      <div class="mega-block-subtitle"> Тепловой пункт </div>
                      <div class="parametrs-info-block">
                        <input class="info-values" type="radio" id='elev' name="elev-itp-radio" value=1 v-model="parametrs_of_reliability.elev_itp">
                        <label class="info-text" for="elev">Элеватор</label>
                      </div>
                      <div class="parametrs-info-block">
                        <input class="info-values" type="radio" id='itp' name="elev-itp-radio" value=0 v-model="parametrs_of_reliability.elev_itp">
                        <label class="info-text" for="itp">ИТП</label>
                      </div>
                      <div class="parametrs-info-block">
                        <input class="info-values" type="checkbox" id='vetsys' v-model="parametrs_of_reliability.ventsys" true-value='1' false-value='0'>
                        <label class="info-text" for="vetsys">Наличие подогрева приточного воздуха</label>
                      </div>
                      <div v-if="parametrs_of_reliability.ventsys === 1 || parametrs_of_reliability.ventsys === '1'"> 
                        <div class="mega-block-subtitle"> Система подогрева приточного воздуха </div>
                        <div class="parametrs-info-block">
                          <div class="info-text"> Число установок</div> 
                          <input class="info-values" type="number" min=0 max=100  v-model="parametrs_of_reliability.count_installations">           
                          <div class="info-text"> ед </div>
                        </div>      
                        <div class="parametrs-info-block">
                          <div class="info-text"> Длина трубы от ТП до установки №1</div> 
                          <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.length_pipe1">           
                          <div class="info-text"> м </div>
                        </div>
                        <div class="parametrs-info-block">
                          <div class="info-text"> Длина трубы от ТП до установки №2</div> 
                          <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.length_pipe2">           
                          <div class="info-text"> м </div>
                        </div>
                      </div>
                      <div class="mega-block-subtitle"> Система ГВС с рециркуляцией </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Число подъёмов ГВС</div> 
                        <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.count_up_hws">           
                        <div class="info-text"> ед </div>
                      </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Число опусков ГВС</div> 
                        <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.count_down_hws">           
                        <div class="info-text"> ед </div>
                      </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Число кранов на каждом этаже (от одного опуска)</div> 
                        <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.count_crane">           
                        <div class="info-text"> ед </div>
                      </div>
                      <div class="mega-block-subtitle"> Система отопления здания </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Число подъёмов от ТП до чердака</div> 
                        <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.count_up_loft">           
                        <div class="info-text"> ед </div>
                      </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Число опусков от чердака до ТП</div> 
                        <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.count_down_loft">           
                        <div class="info-text"> ед </div>
                      </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Число отопительных приборов на этаже (от одного опуска)</div> 
                        <input class="info-values" type="number" min=0 max=100 v-model="parametrs_of_reliability.count_radiator">           
                        <div class="info-text"> ед </div>
                      </div>
                      <div class="mega-block-subtitle"> Параметры здания</div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Тип запорной арматуры</div> 
                        <select class="info-values" v-model="parametrs_of_reliability.type_armature">
                          <option v-for="(type_item) in type_armature" :value="type_item.id" :key=type_item.id readonly>
                            {{type_item.val}}
                          </option> 
                        </select>
                      </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Тип трубы</div> 
                        <select class="info-values" v-model="parametrs_of_reliability.type_pipe">
                          <option v-for="(type_item) in type_pipe" :value="type_item.id" :key=type_item.id readonly>
                            {{type_item.val}}
                          </option> 
                        </select>
                      </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Тип радиатора</div>
                        <select class="info-values" v-model="parametrs_of_reliability.type_radiator">
                          <option v-for="(type_item) in type_radiator" :value="type_item.id" :key=type_item.id readonly>
                            {{type_item.val}}
                          </option> 
                        </select>
                      </div>
                      <div class="parametrs-info-block">
                        <div class="info-text"> Тип крана</div> 
                        <select class="info-values" v-model="parametrs_of_reliability.type_crane">
                          <option v-for="(type_item) in type_crane" :value="type_item.id" :key=type_item.id readonly>
                            {{type_item.val}}
                          </option> 
                        </select>
                      </div>
                    </div>   
                  </div>
                  <div class="results-info-block-borders"> 
                    <div v-if="results.reliability !== ''">
                      <div class="info-text"> Результаты расчетов </div>  
                      <div class="info-text"> {{printVal(results.reliability, 'Гкал')}} </div>
                    </div>
                    <button class="btn-calc" @click="calc_reliability()" style="position:relative; top: 90%;"> Выполнить расчет</button> 
                  </div>      
               </div>    
          </div>

          <div v-for="(section, index_section) in sections" :key=index_section>     
            <div v-show="section.check">
              <div class="mega-block-title"> {{section.title}} </div>                                          
              <div class="mega-block-sections">
                <div class="parametrs-info-block-borders"> 
                  <div class="mega-block-subtitle"> {{section.subtitle}} </div>         
                  <div v-for="(item, index) in section.title_fields" :key=index>             
                    <div v-if="section.value_fields[index] == 'class_energoeff'" class="parametrs-info-block" style="flex-direction: column"> 
                      <div class="info-text"> {{item}} </div>  
                      <div class="info-values"> 
                        {{ printInfoVal(section.value_fields[index]) }}
                      </div>
                    </div>             
                    <div v-else class="parametrs-info-block">
                      <div class="info-text"> {{item}} </div>  
                      <div class="info-values"> 
                        {{ printInfoVal(section.value_fields[index]) }}
                      </div>               
                      <div class="info-text"> {{section.ue_fields[index]}} </div> 
                    </div>           
                  </div>
                </div>  
                <div v-if="results[section.name] !== ''" class="results-info-block-borders">
                  <div class="info-text"> Результаты расчетов </div>  
                  <div class="info-text"> {{printVal(results[section.name], 'Гкал')}} </div>
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
  </div>
  </template>

  <script src='@/scripts.js'>
  </script>


  