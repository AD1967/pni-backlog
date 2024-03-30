<template>
  <div class="flex-wrap">
    <!-- Заголовок сайта ------------------------------------------------------------------------>
    <div class="header"> 
      <div class="flex-wrap">
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
        <input class="settings-param-input" type="text" :value="functions[0].input[1][2]" @input="changes(0, 'input', 1, $event.target.value)" >
        <h1 class="settings-param-name">Длина здания, м</h1>
        <input class="settings-param-input" type="text" :value="functions[0].input[2][2]" @input="changes(0, 'input', 2, $event.target.value)">
        <h1 class="settings-param-name">Ширина здания, м</h1>
        <input class="settings-param-input" type="text" :value="functions[0].input[3][2]" @input="changes(0, 'input', 3, $event.target.value)">
        <h1 class="settings-param-name">Длина стен на одном этаже, м</h1>
        <input class="settings-param-input" type="text" :value="functions[0].input[4][2]" @input="changes(0, 'input', 4, $event.target.value)">
        <h1 class="settings-param-name">Высота стен на одном этаже, м </h1>
        <input class="settings-param-input" type="text" :value="functions[0].input[5][2]" @input="changes(0, 'input', 5, $event.target.value)">
        <h1 class="settings-param-name">Температура внутреннего воздуха, грд C</h1>
        <input class="settings-param-input" type="text" :value="functions[0].input[6][2]" @input="changes(0, 'input', 6, $event.target.value)">
        <h1 class="settings-param-name">Температура наружного воздуха, грд C</h1>
        <input class="settings-param-input" type="text" :value="functions[0].input[7][2]" @input="changes(0, 'input', 7, $event.target.value)">
        <h1 class="settings-param-name">Дата постройки</h1>
        <input class="settings-param-input" type="date" :value="functions[0].date[0][1]"   @input="changes(0, 'date', 0, $event.target.value)">
        
        <!--- Настройки окон----------------------------->  
        <h1 class="settings-param-name">Число окон в здании</h1>
        <input class="settings-param-input" type="text" :value="functions[5].input[0][2]" @input="changes(5, 'input', 0, $event.target.value)">
        <h1 class="settings-param-name">Длина типового окна, м</h1>
        <input class="settings-param-input" type="text" :value="functions[5].input[1][2]" @input="changes(5, 'input', 1, $event.target.value)">
        <h1 class="settings-param-name">Высота типового окна, м</h1>
        <input class="settings-param-input" type="text" :value="functions[5].input[2][2]" @input="changes(5, 'input', 2, $event.target.value)" >
        <h1 class="settings-param-name">Дата установки окон</h1>
        <input class="settings-param-date" type="date" :value="functions[5].date[0][1] " @input="changes(5, 'date', 0, $event.target.value)">     
        <h1 class="settings-param-name">Тип окон</h1>
        <div v-for="(sel, indexsel) in functions[5].select" :key=sel>  
          <div v-if="(sel[5]===undefined || sel[5]===null) || sel[5]()">  
            <select class="settings-param-select" :value="sel[3]" @change="changes(5, 'select', indexsel, $event.target.value)">
            <option v-for="(selbody) in sel[1]" :key=selbody  readonly>
                {{selbody}}
            </option> 
            </select>
          </div>
        </div>
        
        <!--------------- Двери ------------------------------>
        <h1 class="settings-param-name">Число дверей </h1>
        <input class="settings-param-input" type="text" :value="functions[7].input[0][2]" @input="changes(7, 'input', 0, $event.target.value)">
        <h1 class="settings-param-name">Длина типовой двери, м</h1>
        <input class="settings-param-input" type="text" :value="functions[7].input[1][2]" @input="changes(7, 'input', 1, $event.target.value)">
        <h1 class="settings-param-name">Высота типовой входной двери, м</h1>
        <input class="settings-param-input" type="text" :value="functions[7].input[2][2]" @input="changes(7, 'input', 2, $event.target.value)">
        <h1 class="settings-param-name">Тип дверей </h1>
        <div v-for="(sel, indexsel) in functions[7].select" :key=sel>  
          <div v-if="(sel[5]===undefined || sel[5]===null) || sel[5]()">  
            <select class="settings-param-select" :value="sel[3]" @change="changes(7, 'select', indexsel, $event.target.value)">
            <option v-for="(selbody) in sel[1]" :key=selbody  readonly>
                {{selbody}}
            </option> 
            </select>
          </div>
        </div>
        <h1 class="settings-param-name">Дата установки дверей</h1>
        <input class="settings-param-date" type="date" :value="functions[7].date[0][1]"   @input="changes(7, 'date', 0, $event.target.value)">
        <h1 class="settings-param-name">Класс энергетической эффективности </h1>
        <h1 class="settings-param-name">ограждающих конструкций </h1>
        
        <div v-for="(sel, indexsel) in functions[9].select" :key=sel>  
            <select class="settings-param-select" :value="sel[3]" @change="changes(9, 'select', indexsel, $event.target.value)">
            <option v-for="(selbody) in sel[1]" :key=selbody  readonly>
                {{selbody}}
            </option> 
            </select>
        </div>

        <!-- <select>
          <option readonly> A++ (очень высокий) </option> 
          <option readonly> A+  (очень высокий) </option> 
          <option readonly> A   (очень высокий) </option> 
          <option readonly> B+  (высокий)       </option> 
          <option readonly> B   (высокий)       </option> 
          <option readonly> C+  (нормальный)    </option>
          <option readonly> С   (нормальный)    </option>  
          <option readonly> С-  (нормальный)    </option> 
          <option readonly> D   (пониженный)    </option> 
          <option readonly> E   (низкий)       </option> 
        </select> -->

        <!-- Мебель и жильцы--------------------------------------------->
        <h1 class="settings-param-name">Число шкафов</h1>
        <input class="settings-param-input" type="text" :value="functions[13].input[1][2]" @input="changes(13, 'input', 1, $event.target.value)">
        <h1 class="settings-param-name">Число диванов</h1>
        <input class="settings-param-input" type="text" :value="functions[13].input[2][2]" @input="changes(13, 'input', 2, $event.target.value)">
        <h1 class="settings-param-name">Число столов</h1>
        <input class="settings-param-input" type="text" :value="functions[13].input[3][2]" @input="changes(13, 'input', 3, $event.target.value)">
        <h1 class="settings-param-name">Число навесных шкафчиков</h1>
        <input class="settings-param-input" type="text" :value="functions[13].input[4][2]" @input="changes(13, 'input', 4, $event.target.value)">
        <h1 class="settings-param-name">Максимальное число посетителей мужчин</h1>
        <input class="settings-param-input" type="text" :value="functions[16].input[0][2]" @input="changes(16, 'input', 0, $event.target.value)">
        <h1 class="settings-param-name">Максимальное число посетителей женщин</h1>
        <input class="settings-param-input" type="text" :value="functions[16].input[1][2]" @input="changes(16, 'input', 1, $event.target.value)">
        <h1 class="settings-param-name">Максимальное число посетителей детей</h1>
        <input class="settings-param-input" type="text" :value="functions[16].input[2][2]" @input="changes(16, 'input', 2, $event.target.value)">
        <h1 class="settings-param-name">Среднее время пребывания посетителей</h1>
        <h1 class="settings-param-name">в сутки</h1>
        <input class="settings-param-input" type="text" :value="functions[16].input[3][2]" @input="changes(16, 'input', 3, $event.target.value)">
        <h1 class="settings-param-name">Количество помещений с раковинами </h1>
        <h1 class="settings-param-name">на этаже</h1>
        <input class="settings-param-input" type="text" :value="functions[20].input[5][2]" @input="changes(16, 'input', 5, $event.target.value)">
        <h1 class="settings-param-name">Высота подвала, м</h1>
        <input class="settings-param-input" type="text" :value="functions[11].input[0][2]" @input="changes(11, 'input', 0, $event.target.value)">
        </div> 
      </div>
      <!-- /Меню настроек--------------------------------------------------------------->
      

      <!-- Основное рабочее пространство  ------------------ ----------------------------------->
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
            <select class="header-selector" @change="import_from_server()" id="years-selector">
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
                  <div class="sum_titles">
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
                  <div class="sum_results">
                    <div v-if="results[2].val != ''">
                      <h1><sub> {{printVal(results[2].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub> {{printVal(results[3].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub> {{printVal(results[4].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub> {{printVal(results[5].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub> {{printVal(results[6].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub> {{printVal(results[7].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub> {{printVal(results[8].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub> {{printVal(results[9].val, 'Гкал')}}  </sub> </h1>
                      <h1><sub>{{printVal(results[10].val, 'Гкал')}} </sub> <sub></sub> </h1> 
                    </div>
                  </div>              
              </div>            
              <div id="sum-plus">
                  <div class="block-title"> Теплопритоки</div><br> 
                  <div class="sum_titles">
                    <h1> от людей <sub> </sub></h1>
                    <h1> от ГВС рукомойников <sub> </sub></h1>
                    <h1> от ГВС душевых <sub> </sub></h1>
                    <h1> от электрооборудования <sub> </sub></h1>
                    <h1> от неизолированных трубопроводов ГВС<sub> </sub></h1>
                    <h1> от неизолированных трубопроводов отопления<sub> </sub></h1>
                  </div>
                  
                  <div class="sum_results">
                    <div v-if="results[11].val != ''">
                      <h1><sub>{{printVal(results[11].val, 'Гкал')}} </sub> </h1>
                      <h1><sub>{{printVal(results[12].val, 'Гкал')}} </sub> </h1>
                      <h1><sub>{{printVal(results[13].val, 'Гкал')}} </sub> </h1>
                      <h1><sub>{{printVal(results[14].val, 'Гкал')}} </sub> </h1>
                      <h1><sub>{{printVal(results[15].val, 'Гкал')}} </sub> </h1>
                      <h1><sub>{{printVal(results[16].val, 'Гкал')}} </sub> </h1>
                      <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                      <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                      <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                    </div>
                  </div>                            
              </div> 
            </div>
            <div v-if="dop_results[0].val != -1" >
              <h1 style="color:var(--white-text-color)">.</h1>
              <div style="display:flex; justify-content: space-between">
                <hr style="width: 45%; margin-left:4%; margin-right:2%;">
                <hr style="width: 45%; margin-right:4%">
              </div>
              

              <div style="display:flex; justify-content: space-between">         
                <div style="width: 45%; margin-left: 4%; margin-right: 0; display:flex; justify-content: space-between">
                  <div>
                    <h1 class="sum-text"> &Sum;<sub style="font-size:20px">теплопотерь</sub></h1>   
                  </div>
                  <div> 
                    <h1 class="sum-text"> <sub> {{printVal(dop_results[0].val, 'Гкал')}} </sub> </h1>
                  </div>
                </div>
                <div style="width: 45%; margin-right:4%; display:flex; justify-content: space-between">
                  <div> 
                    <h1 class="sum-text"> &Sum;<sub style="font-size:20px">теплопритоков</sub> </h1> 
                  </div>
                  <div>
                    <h1 class="sum-text"> <sub> {{printVal(dop_results[1].val, 'Гкал')}} </sub> </h1>
                  </div> 
                </div>
              </div>

            </div>
          </div>
          <!-- Конец блока c расчетом суммарных притоков и потерь ------------------------------------------------------------->
          
          <!-- Пространство кнопок расчетов  ------------------------------------------------------>
          <div class="buttons_for_calc">

            <!-- Формульный расчет по СП -->
            <div class="math_calc_block">
              <div class="calc_download_block">            
                <button class="btn_calc" @click="calc_all()">
                  <div class=btn_calc_text> Формульный расчет по СП 50.13330.2012</div>
                </button> 
                  <a @click="download_excel()" class="btn_calc btn_download" href="#"> 
                    <img class="img_download" src="@/download.png"> 
                  </a>           
              </div>
              <div v-if="dop_results[2].val != -1">
                <p class="comment_text" style="width:150%">Разница теплопотерь и теплопритоков</p> 
                <input class="output_field" type="text" 
                :value="printVal(dop_results[2].val, 'Гкал')" readonly>
                <p class="comment_text">Экологический ущерб </p> 
                <input class="output_field" style="margin-top: 10px;" type="text" :value="printVal(dop_results[4].val, 'т.у.т')" readonly>
                <input class="output_field" style="margin-top: 10px;" type="text" :value="printVal(dop_results[5].val, 'кг CO2/год')" readonly>
              </div>         
            </div>
          
            <!-- Расчет искусственной нейронной сетью -->
            <div class="math_calc_block">
              <div class="calc_download_block">   

                <div style="display: block;">
                  <button class="btn_calc" style="width: 100%">
                    <div class=btn_calc_text id="neuro_calc_id" @click="calc_neuro()"> Расчет искусственной нейронной сетью </div>
                  </button>     
                  
                  <select v-if="choise_NM == true" class="btn_calc" style="width: 100%; margin: 8px; margin-left:0; margin-right: 0;">
                    <option>Модель 1</option>
                    <option>Модель 2</option>
                    <option>Модель 3</option>
                  </select>
                </div>

                <a @click="download_excel()" class="btn_calc btn_download" href="#" :download=url_to_download_math> 
                    <img class="img_download" src="@/download.png"> 
                </a> 
              </div>
              <input v-if="0 == 1" class="output_field" type="text" readonly>         
            </div>
            
            <div style="display:block; width: 50%;">
              <div style=" width: 100%; display: flex; justify-content: space-between;"> 
                  <!-- Отпуск тепловой энергии ТЭЦ -->
                  <div class="calc_TC_CPT_block">
                    <button class="btn_calc btn_TC" @click="calc_tec()">
                      <div class=btn_calc_text> Отпуск тепловой энергии ТЭЦ </div>
                    </button>         
                    <input v-if="results[17].val != ''" class="output_field" type="text" :value="printVal(results[17].val, 'Гкал')" readonly>         
                  </div>

                  <!-- Потребление тепловой энергии от ЦПТ  -->
                  <div class="calc_TC_CPT_block">                
                      <button class="btn_calc btn_TC" @click="calc_cpt()">
                        <div class=btn_calc_text> Потребление тепловой энергии от ЦПТ </div>
                      </button>   
                      <input v-if="results[18].val != ''" class="output_field" type="text" :value="printVal(results[18].val, 'Гкал')" readonly>                
                      <div v-if="(dop_results[3].val != -1)">
                        <p class="comment_text" style="text-align:right">Разница ТЭЦ и ЦПТ</p>
                        <input  class="output_field" style="margin-bottom: 2px; margin-top: 10px;" type="text" :value="printVal(dop_results[3].val, 'Гкал')" readonly>
                        <p class="comment_text" style="text-align:right">Экологический ущерб </p> 
                        <input class="output_field" style="margin-top: 10px;" type="text" :value="printVal(dop_results[6].val, 'т.у.т')" readonly>
                        <input class="output_field" style="margin-top: 10px;" type="text" :value="printVal(dop_results[7].val, 'кг СО2/год')" readonly> 
                      </div> 
                  </div>
              </div>
            </div>
          </div>         


    
          
          <!-- /Пространство кнопок расчетов--------- ------------------------------------------->
          
          <!-- Отрисовка основных блоков расчета ------------------------------------------------>
          <div v-for="section in sections" :key=section>
            <div v-show="section.check==='true'">
              <div class="mega_block_sections">
                <div class="mega_block_title"> {{section.title}} </div>
                <div class="mega_block_borders">
                  <div class="mega_block">
                    <div :class="[section.name == 'reliability' || section.name == 'add_heatcosts' ? 'rel_block' : 'main_block']" :style="{'width': section.main_block_width+'%'}"> 
                      <!-- Формы ввода для основных блоков   ------------------------------------->
                      <div v-for="(func, ind) in functions" :key=func>
                        <div v-if="func.id===section.name && func.render !== false">
                          <div :class="[section.name == 'general'|| section.name == 'reliability' || section.name == 'add_heatcosts' ? 'gen_block' : 'block']">
                            <div class="block-title">{{ func.title }}</div><br>
                            <div v-for="(inp, indexinp) in func.input" :key=inp>
                              <div v-if="(inp[6]===undefined || inp[6]===null) || inp[6]()">
                                <div v-if="inp[5]===undefined || inp[5]===null">
                                    {{inp[0]}}  <!-- текстовый вывод названия поля -->
                                    <input :class="[indexinp==0 && section.name == 'general' ? 'field_inp_name':'field_inp']" type="text" 
                                    :value="inp[2]" @input="changes(ind, 'input', indexinp, $event.target.value)" readonly>
                                    {{inp[1]}} <!--текстовый вывод ед.измерения-->
                                    <div v-if="!inp[4]">  <!-- проверка заполнения -->
                                    <b style="color:red" v-if="String(inp[2]).trim() === ''">Поле не заполнено.</b>
                                    <b style="color:red" v-if="String(inp[2]).trim() !== '' && (inp[3] == 'int' || inp[3] == 'uint') ">Неверный формат числа.</b>
                                    </div>
                                </div>
                                <div v-else>
                                  {{inp[0]}}
                                  <input :class="[indexinp==0 && section.name == 'general' ? 'field_inp_name':'field_inp']" type="text"
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
                                    <input v-if="func.id != 'add_heatcosts'" class="field_select_readonly" type="text" :value="sel[3]" @change="changes(ind, 'select', indexsel, $event.target.value)" readonly>
                                    <select id="big_select" v-else :value="sel[3]" @change="changes(index1, 'select', indexsel, $event.target.value)">
                                      <option style="" v-for="(selbody, indexbody) in sel[1]" v-bind:key=selbody :id="func.id +'_'+ index1+'_sel_'+indexsel+'_selnum_'+indexbody">
                                          {{selbody}}
                                      </option>
                                    </select>
                                  </div>
                                  <div v-else>
                                      <td>{{sel[0] }}</td>
                                      <input class="field_select_readonly" type="text" :value="functions[sel[4][0]].select[sel[4][1]][3]" readonly>
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
                                        <input type="date" :id="func.id +'_'+ ind+'_date_'+indexdate"
                                        :value="d[1]" @input="changes(ind, 'date', indexdate, $event.target.value)" readonly>
                                    </div>
                                    <div v-else>
                                        {{d[0]}}
                                        <input type="date" :id="func.id +'_'+ ind+'_date_'+indexdate"
                                        :value="functions[d[2][0]].date[d[2][1]][1]" readonly>
                                        <b style="color:green">{{d[2][2]}}</b>
                                    </div>
                              </div>
                          </div> 
                        </div>
                      </div>         
                    </div> 
                <!-- /Формы ввода для основных блоков   ----------------------------------->
                    <div v-if="section.name!=='general'" class="res_block">
                      <div class= "res_block block_r">
                        <div v-for="result in results" :key=result>
                          <div v-if="result.id===section.name">
                            <span v-html="result.val"></span>
                          </div>
                        </div>
                      </div>
                    </div>               
                  </div>
                </div>   
              </div>
            </div>
          </div>
          <!-- /Отрисовка основных блоков расчета --------------------------------------------->
        </div>
      </div>
    </div>
    <!--/Тело ----------------------------------------------------------------------->
    <dialogbox-login v-model:show=login_reg_check>
    </dialogbox-login> 
    <dialogbox-reg v-model:show=login_reg_check>
    </dialogbox-reg> 
  </div>
  </template>



  <script src='@/scripts.js'>
  </script>