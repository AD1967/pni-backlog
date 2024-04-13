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
          <div v-for="bgsec_name in big_sections_name" :key=bgsec_name>
            <div >
              <h4  class="glob-section-title">
                {{bgsec_name.name}}
              </h4>
              <div v-for="sec in sections" :key=sec>
                <div v-if="sec.section===bgsec_name.name">
                  <h5 class="sub-section-title">  
                    <label :for=sec.name class="checkbox style-c">
                      <input type="checkbox" :id=sec.name v-model="sec.check" true-value="true" false-value="false"/>
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
              <select class="header-selector" @change="import_from_server()" id="name_of_scheme"  v-model="load_pat.select.picked">
                <option v-for="(build) in load_pat.select.variants" :key=build >
                  {{build}} 
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

            <!-- пока пропустила ------------------------------------------->
            <!-- Расчет искусственной нейронной сетью -->
            <div class="math-calc-block">
              <div class="flex-between">   

                <div style="display: block;">
                  <button class="btn-calc" style="width: 100%">
                    <div class=btn-calc-text id="neuro_calc_id" @click="calc_neuro()"> Расчет искусственной нейронной сетью </div>
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
              <input v-if="0 == 1" class="output-field" type="text" readonly>         
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
          <div v-for="(section, index_section) in sections" :key=index_section>     
            <div v-show="section.check==='true'">
              <div class="mega-block-title"> {{section.title}} </div>                                          
              <div class="mega-block-sections">
                <div class="parametrs-info-block-borders"> 
                  <div class="mega-block-subtitle"> {{section.subtitle}} </div>         
                  <div v-for="(item, index) in section.title_fields" :key=index>             
                    <div class="parametrs-info-block">
                      <div class="info-text"> {{item}} </div>  
                      <div class="info-values"> 
                        <div v-if="section.value_fields[index] === 'type_windows'"> 
                          {{ type_windows_selected }}
                        </div>
                        <div v-else> 
                          <div v-if="section.value_fields[index] === 'type_doors'"> 
                            {{ type_doors_selected }}
                          </div>
                          <div v-else> 
                            <div v-if="section.value_fields[index] === 'class_energoeff'"> 
                              {{ class_energoeff_selected }}
                            </div>
                            <div v-else>
                              {{parametrs_of_build[section.value_fields[index]]}}
                            </div>
                          </div>
                        </div> 
                      </div>               
                      <div class="info-text"> {{section.ue_fields[index]}} </div> 
                    </div>           
                  </div>
                </div>  
                <div class="results-info-block-borders">
                  <div class="info-text"> {{results.general}} </div>  
                </div>       
              </div>  
            </div>
          </div>
          <!--/Отрисовка информационных блоков--------------------------------------------------->

          <!-- старое--------------------------------->
          <div v-for="section in sections" :key=section>
            <!-- <div v-show="section.check==='true'">  -->
              <div v-show="'false'==='true'"> 
              <div class="mega-block-sections">
                <div class="mega-block-title"> {{section.title}} </div>
                
                  <div class="mega-block">
                    <div :class="[section.name == 'reliability' || section.name == 'add_heatcosts' ? 'rel-block' : 'main-block']" > 
                      <!-- Формы ввода для основных блоков   ------------------------------------->
                      <div v-for="(func, ind) in functions" :key=func>
                        <div v-if="func.id===section.name && func.render !== false">
                          <div class="block">
                            <div class="block-title">{{ func.title }}</div><br>
                            <div v-for="(inp, indexinp) in func.input" :key=inp>
                              <div v-if="(inp[6]===undefined || inp[6]===null) || inp[6]()">
                                <div v-if="inp[5]===undefined || inp[5]===null">
                                    {{inp[0]}} 
                                    <input class="field-inp" type="text" 
                                    :value="inp[2]" @input="changes(ind, 'input', indexinp, $event.target.value)" readonly>
                                    {{inp[1]}} 
                                    <div v-if="!inp[4]"> 
                                    <b style="color:red" v-if="String(inp[2]).trim() === ''">Поле не заполнено.</b>
                                    <b style="color:red" v-if="String(inp[2]).trim() !== '' && (inp[3] == 'int' || inp[3] == 'uint') ">Неверный формат числа.</b>
                                    </div>
                                </div>
                                <div v-else> 
                                  {{inp[0]}}
                                  <input class="field-inp" type="text"
                                  :value="functions[inp[5][0]].input[inp[5][1]][2]" readonly>
                                  {{inp[1]}} <b style="color:grey">{{inp[5][2]}}</b>
                                  <div v-if="!functions[inp[5][0]].input[inp[5][1]][4]">
                                  <b style="color:red" v-if="String(functions[inp[5][0]].input[inp[5][1]][2]).trim() === ''">поле не заполнено</b>
                                  <b style="color:red" v-if="String(functions[inp[5][0]].input[inp[5][1]][2]).trim() !== '' && (functions[inp[5][0]].input[inp[5][1]][3] == 'int' || functions[inp[5][0]].input[inp[5][1]][3] == 'uint') ">неправильный формат числа</b>
                                  </div>
                              </div>
                              </div>  
                            </div>
                            <div v-for="(btn, indexrbtn) in func.r_btn" :key=btn>
                              <input type="radio" name={{func}} :id="func.id +'_'+ ind+'_rbtn_'+indexrbtn"
                              :value=btn
                                v-on:change="changes(ind, 'radio', 0, $event.target.value)"
                              :checked="btn==func.radio_elem[0]" readonly
                              >
                              <label>{{btn}}</label>
                            </div>
                            <table>
                              <tr>
                                <div v-for="(sel, indexsel) in func.select" :key=sel>  
                                <div v-if="(sel[5]===undefined || sel[5]===null) || sel[5]()"> 
                                  <div v-if="sel[4]===undefined || sel[4]===null">
                                    <td>{{sel[0]}}</td>
                                    <input v-if="func.id != 'add_heatcosts'" class="field-inp-select" type="text" :value="sel[3]" @change="changes(ind, 'select', indexsel, $event.target.value)" readonly>
                                    <select id="big-select" v-else :value="sel[3]" @change="changes(index1, 'select', indexsel, $event.target.value)">
                                      <option style="" v-for="(selbody, indexbody) in sel[1]" v-bind:key=selbody :id="func.id +'_'+ index1+'_sel_'+indexsel+'_selnum_'+indexbody">
                                          {{selbody}}
                                      </option>
                                    </select>
                                  </div>
                                  <div v-else>
                                      <td>{{sel[0] }}</td>
                                      <input class="field-inp-select" type="text" :value="functions[sel[4][0]].select[sel[4][1]][3]" readonly>
                                  </div>
                                </div> 
                              </div>
                              </tr>
                            </table>
                              <p v-for="(box, indexcbox) in func.c_box" :key=box>
                                <input type="checkbox" :id="func.id +'_'+ ind+'_cbox_'+indexcbox" 
                                  :checked="func.check_elem[indexcbox]"
                                    v-on:input="changes(ind, 'checkbox', indexcbox, $event.target.checked)"
                                    readonly
                                  >
                                {{box}}
                              </p>
                              <div v-for="(d, indexdate) in func.date" :key=d>
                                    <div v-if="d[2]===undefined || d[2]===null">
                                        {{d[0]}}
                                        <input class="field-inp" type="date" :id="func.id +'_'+ ind+'_date_'+indexdate"
                                        :value="d[1]" @input="changes(ind, 'date', indexdate, $event.target.value)" readonly>
                                    </div>
                                    <div v-else>
                                        {{d[0]}}
                                        <input class="field-inp" type="date" :id="func.id +'_'+ ind+'_date_'+indexdate"
                                        :value="functions[d[2][0]].date[d[2][1]][1]" readonly>
                                        <b style="color:green">{{d[2][2]}}</b>
                                    </div>
                              </div>
                          </div> 
                        </div>
                      </div>                       
                  </div>
                </div>   
              </div>
            </div>
          </div>
          <!-- старое--------------------------------->


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


  