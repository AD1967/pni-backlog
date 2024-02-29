<template>
<div class="app">
  <!-- Заголовок сайта ------------------------------------------------------------------------>
  <div class="header"> 
    <div style="display: flex;">
      <input class="header_cb_transparent" type="checkbox" id="id_menu" v-model="menu_check" true-value="0" false-value="20"/>
      <label for="id_menu" class="header_menu">
        <label for="id_menu" class="strip"></label>
        <label for="id_menu" class="strip"></label>
        <label for="id_menu" class="strip"></label>
      </label>
    </div>

    <div class="header_text">
      <div class="header_title">Интегральный индекс</div>
      <div style="display: flex; position: relative; left: 100px;">
        <input class="header_cb_transparent" type="checkbox" id="id_settings" v-model="settings_check" true-value="0" false-value="20" style=" position: relative; left: 180px;" />
        <div style="display:flex; position: relative; left: 240px"> 
          <label for="id_settings" class="header_menu"  style="width:28px; height: 28px;">
            <img for="id_settings" src="@/settings.jpg" style="width:28px; position: relative; right: 350%;"/> 
          </label>
        </div>
      </div>
      <div class="exit_label" @click="logout()">Выход</div>
    </div>
  </div>
  <!--/Заголовок сайта------------------------------------------------------------------------>

  <!-- Основная часть ------------------------------------------------------------------------>
  <div class="body">  

    <!-- Выпадающее меню слева---------------------------------------------------------------->
    <div v-show="menu_check==='20'">
      <div class="left_panel">
        <div v-for="bgsec_name in big_sections_name" :key=bgsec_name>
          <div>
            <h4 class="glob_section_title">
              {{bgsec_name.name}}
            </h4>
            <div v-for="sec in sections" :key=sec>
              <div v-if="sec.section===bgsec_name.name">
                <h5 class="sub_section_title">
                  <input type="checkbox" :id=sec.name v-model="sec.check" true-value="true" false-value="false"/>
                  <label :for=sec.name> {{sec.title}} </label>  
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
      <div class="right_panel">
      <h1 class="settings_title">Настройка параметров </h1> 
      
      <!-------Основные настройки------------------------->
      <h1 class="settings_param_name">Этажность здания</h1>
      <input class="settings_param_input" type="text" :value="functions[0].input[1][2]" @input="changes(0, 'input', 1, $event.target.value)" >
      <h1 class="settings_param_name">Длина здания, м</h1>
      <input class="settings_param_input" type="text" :value="functions[0].input[2][2]" @input="changes(0, 'input', 2, $event.target.value)">
      <h1 class="settings_param_name">Ширина здания, м</h1>
      <input class="settings_param_input" type="text" :value="functions[0].input[3][2]" @input="changes(0, 'input', 3, $event.target.value)">
      <h1 class="settings_param_name">Длина стен на одном этаже, м</h1>
      <input class="settings_param_input" type="text" :value="functions[0].input[4][2]" @input="changes(0, 'input', 4, $event.target.value)">
      <h1 class="settings_param_name">Высота стен на одном этаже, м </h1>
      <input class="settings_param_input" type="text" :value="functions[0].input[5][2]" @input="changes(0, 'input', 5, $event.target.value)">
      <h1 class="settings_param_name">Температура внутреннего воздуха, грд C</h1>
      <input class="settings_param_input" type="text" :value="functions[0].input[6][2]" @input="changes(0, 'input', 6, $event.target.value)">
      <h1 class="settings_param_name">Температура наружного воздуха, грд C</h1>
      <input class="settings_param_input" type="text" :value="functions[0].input[7][2]" @input="changes(0, 'input', 7, $event.target.value)">
      <h1 class="settings_param_name">Дата постройки</h1>
      <input class="settings_param_date" type="date" :value="functions[0].date[0][1]"   @input="changes(0, 'date', 0, $event.target.value)">
      

      <!--- Настройки окон----------------------------->  
      <h1 class="settings_param_name">Число окон в здании</h1>
      <input class="settings_param_input" type="text" :value="functions[5].input[0][2]" @input="changes(5, 'input', 0, $event.target.value)">
      <h1 class="settings_param_name">Длина типового окна, м</h1>
      <input class="settings_param_input" type="text" :value="functions[5].input[1][2]" @input="changes(5, 'input', 1, $event.target.value)">
      <h1 class="settings_param_name">Высота типового окна, м</h1>
      <input class="settings_param_input" type="text" :value="functions[5].input[2][2]" @input="changes(5, 'input', 2, $event.target.value)" >
      <h1 class="settings_param_name">Дата установки окон</h1>
      <input class="settings_param_input" type="date" :value="functions[5].date[0][1] " @input="changes(5, 'date', 0, $event.target.value)">     
      <h1 class="settings_param_name">Тип окон</h1>
      <div v-for="(sel, indexsel) in functions[5].select" :key=sel>  
        <div v-if="(sel[5]===undefined || sel[5]===null) || sel[5]()">  
          <select :value="sel[3]" @change="changes(5, 'select', indexsel, $event.target.value)">
          <option v-for="(selbody) in sel[1]" :key=selbody  readonly>
              {{selbody}}
          </option> 
          </select>
        </div>
      </div>
      
      <!--------------- Двери ------------------------------>
      <h1 class="settings_param_name">Число дверей </h1>
      <input class="settings_param_input" type="text" :value="functions[7].input[0][2]" @input="changes(7, 'input', 0, $event.target.value)">
      <h1 class="settings_param_name">Длина типовой двери, м</h1>
      <input class="settings_param_input" type="text" :value="functions[7].input[1][2]" @input="changes(7, 'input', 1, $event.target.value)">
      <h1 class="settings_param_name">Высота типовой входной двери, м</h1>
      <input class="settings_param_input" type="text" :value="functions[7].input[2][2]" @input="changes(7, 'input', 2, $event.target.value)">
      <h1 class="settings_param_name">Тип дверей </h1>
      <div v-for="(sel, indexsel) in functions[7].select" :key=sel>  
        <div v-if="(sel[5]===undefined || sel[5]===null) || sel[5]()">  
          <select :value="sel[3]" @change="changes(7, 'select', indexsel, $event.target.value)">
          <option v-for="(selbody) in sel[1]" :key=selbody  readonly>
              {{selbody}}
          </option> 
          </select>
        </div>
      </div>
      <h1 class="settings_param_name">Дата установки дверей</h1>
      <input class="settings_param_input" type="date" :value="functions[7].date[0][1]"   @input="changes(7, 'date', 0, $event.target.value)">
      <h1 class="settings_param_name">Класс энергетической эффективности </h1>
      <h1 class="settings_param_name">ограждающих конструкций </h1>
      <div v-for="(sel, indexsel) in functions[9].select" :key=sel>  
        <div v-if="(sel[5]===undefined || sel[5]===null) || sel[5]()">  
          <select :value="sel[3]" @change="changes(9, 'select', indexsel, $event.target.value)">
          <option v-for="(selbody) in sel[1]" :key=selbody  readonly>
              {{selbody}}
          </option> 
          </select>
        </div>
      </div>

      <!-- Мебель и жильцы--------------------------------------------->
      <h1 class="settings_param_name">Число шкафов</h1>
      <input class="settings_param_input" type="text" :value="functions[13].input[1][2]" @input="changes(13, 'input', 1, $event.target.value)">
      <h1 class="settings_param_name">Число диванов</h1>
      <input class="settings_param_input" type="text" :value="functions[13].input[2][2]" @input="changes(13, 'input', 2, $event.target.value)">
      <h1 class="settings_param_name">Число столов</h1>
      <input class="settings_param_input" type="text" :value="functions[13].input[3][2]" @input="changes(13, 'input', 3, $event.target.value)">
      <h1 class="settings_param_name">Число навесных шкафчиков</h1>
      <input class="settings_param_input" type="text" :value="functions[13].input[4][2]" @input="changes(13, 'input', 4, $event.target.value)">
      <h1 class="settings_param_name">Максимальное число посетителей мужчин</h1>
      <input class="settings_param_input" type="text" :value="functions[16].input[0][2]" @input="changes(16, 'input', 0, $event.target.value)">
      <h1 class="settings_param_name">Максимальное число посетителей женщин</h1>
      <input class="settings_param_input" type="text" :value="functions[16].input[1][2]" @input="changes(16, 'input', 1, $event.target.value)">
      <h1 class="settings_param_name">Максимальное число посетителей детей</h1>
      <input class="settings_param_input" type="text" :value="functions[16].input[2][2]" @input="changes(16, 'input', 2, $event.target.value)">

      <h1 class="settings_param_name">Среднее время пребывания посетителей</h1>
      <h1 class="settings_param_name">в сутки</h1>
      <input class="settings_param_input" type="text" :value="functions[16].input[3][2]" @input="changes(16, 'input', 3, $event.target.value)">
      <h1 class="settings_param_name">Количество помещений с раковинами </h1>
      <h1 class="settings_param_name">на этаже</h1>
      <input class="settings_param_input" type="text" :value="functions[20].input[5][2]" @input="changes(16, 'input', 5, $event.target.value)">
      <h1 class="settings_param_name">Высота подвала, м</h1>
      <input class="settings_param_input" type="text" :value="functions[11].input[0][2]" @input="changes(11, 'input', 0, $event.target.value)">
      </div> 
    </div>
    <!-- /Меню настроек--------------------------------------------------------------->

    <!-- Основное рабочее пространство  ------------------ ----------------------------------->
    <div :style="{'width': 100+'%'}">
      <div class="solution" :style="{'padding-left': menu_check+'%'}">

        <input id="name_of_scheme" type="text" :value="functions[0].input[0][2]" @input="changes(0, 'input', 0, $event.target.value)">
        <!-- Блок с расчетом суммарных притоков и потерь -->
        <div class="sum_block">
          <div id="sum_minus">
                <div class="block_title"> Теплопотери</div><br> 
                <div class="sum_titles">
                  <h1> Q<sub>окон</sub> </h1>
                  <h1> Q<sub>рез.окон </sub> </h1>
                  <h1> Q<sub>двери </sub> </h1>
                  <h1> Q<sub>рез.двери</sub></h1>
                  <h1> Q<sub>стен</sub> </h1>
                  <h1> Q<sub>стен.инф.</sub> </h1>
                  <h1> Q<sub>пол</sub> </h1>
                  <h1> Q<sub>вент</sub> </h1>
                  <h1> Q<sub>доп</sub></h1>
                  <br>
                  <hr>
                  <h1 class="red_sum"> &Sum;<sub>потерь</sub></h1> 
                  
                </div>  
                <div class="sum_results">
                  <div v-if="results[2].dec != ''">
                    <h1><sub> {{results[2].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[3].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[4].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[5].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[6].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[7].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[8].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[9].dec}} Гкал</sub> </h1>
                    <h1><sub> {{results[10].dec}}Гкал</sub> <sub></sub> </h1> 
                  </div>
                  <br>
                  <hr v-if="results[2].dec != ''">
                  <h1 v-if="results[2].dec != ''" class ="red_sum"> <sub>{{ }}</sub></h1>
                </div>              
            </div>
            
            <div id="sum_plus">
                <div class="block_title"> Теплопритоки</div><br> 
                <div class="sum_titles">
                  <h1> Q<sub>персонал</sub></h1>
                  <h1> Q<sub>рук </sub></h1>
                  <h1> Q<sub>душ </sub></h1>
                  <h1> Q<sub>ЭЭ.отоп.пер.</sub></h1>
                  <h1> Q<sub>труб</sub></h1>
                  <h1> Q<sub>труб.отопл.</sub></h1>
                  <h1> <sub sub style="color: #e5e5dc">.</sub> </h1>
                  <h1> <sub sub style="color: #e5e5dc">.</sub> </h1> 
                  <h1> <sub sub style="color: #e5e5dc">.</sub> </h1> 
                  <br>
                  <hr>
                  <h1 class="red_sum"> &Sum;<sub>притоков</sub></h1>  
                </div>
                
                <div class="sum_results">
                  <div v-if="results[11].dec != ''">
                    <h1><sub>{{results[11].dec}} Гкал</sub> </h1>
                    <h1><sub>{{results[12].dec}} Гкал</sub> </h1>
                    <h1><sub>{{results[13].dec}} Гкал</sub> </h1>
                    <h1><sub>{{results[14].dec}} Гкал</sub> </h1>
                    <h1><sub>{{results[15].dec}} Гкал</sub> </h1>
                    <h1><sub>{{results[16].dec}} Гкал</sub> </h1>
                    <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                    <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                    <h1><sub style="color: #e5e5dc;">.</sub> </h1>
                  </div>
                  <br>
                  <hr v-if="results[11].dec != ''">
                  <h1 v-if="results[11].dec != ''" class ="red_sum"> <sub></sub></h1>
                </div>                            
            </div>
        </div>
        <!-- Конец блока c расчетом суммарных притоков и потерь ------------------------------------------------------------->
        
        
        <!-- Пространство кнопок загрузки шаблонов ------------------------------------------->
        <div class="btn_div_global">
          <div class="btn_patterns" >

            <!-- Кнопка загрузки шаблона -->
            <div class="btn_loadpat">
              <button class="btn_pat" @click="check_loadpat = !check_loadpat">
                <div style="margin: 2%;"> Загрузить шаблон </div>
              </button>
              
              <div class="show_pat" v-if="check_loadpat">
                <div class="content"> 
                  <b>Выберите шаблон</b>
                  <select id="big_select" v-model="load_pat.select.picked">
                    <option style="" v-for="(build) in load_pat.select.variants" :key=build >
                      {{build}}
                    </option>
                  </select>
                  <div v-if="loadpat_error.show">
                    <div v-if="loadpat_error.text == ''">
                      <b style="color:red">
                        Ошибка загрузки шаблона
                      </b>
                    </div>
                    <div v-if="loadpat_error.text != ''">
                      <b style="color:red">
                        {{loadpat_error.text}}
                      </b>
                    </div>
                  </div>
                </div>
                <div class="pat_buttons">
                  <button class="pat_btn" @click="import_from_server()">
                    <div style="margin: 2%;"> ОК </div>
                  </button>
                  <button class="pat_btn" @click="check_loadpat = !check_loadpat">
                    <div style="margin: 2%;"> Отмена </div>
                  </button>
                </div>
              </div>
            </div>
            <!-- /Кнопка загрузки шаблона -->

            <!-- Кнопка сохранения шаблона -->
            <div class="btn_savepat">
              <button class="btn_pat" @click="check_savepat = !check_savepat; savepat_error.show = false">
                <div style="margin: 2%;"> Сохранить шаблон </div>
              </button> 
              <div class="show_pat" v-if="check_savepat">
                <div class="content"> 
                  <b>Название шаблона</b>
                  
                  <input class="inp_pat" type="text" v-model="functions[0].input[0][2]">
                  <br>
                  <div>
                    <input type="radio" value="Загружать полностью" v-model="savepat.radio.picked">
                    <label>Сохранять полностью</label>
                  </div>
                  <div>
                    <input type="radio" value="Сохранять только из выбранных расчётов" v-model="savepat.radio.picked">
                    <label>Сохранять только из выбранных расчётов</label>
                  </div>
                  <br>
                  <div v-if="savepat_error.show">
                    <div v-if="savepat_error.text == ''">
                      <b style="color:red"> Ошибка сохранения шаблона </b>
                    </div>
                    <div v-if="savepat_error.text != ''">
                      <b style="color:red">
                        {{savepat_error.text}}
                      </b>
                    </div>
                  </div>
                
                </div>
                <div class="pat_buttons">
                  <button class="pat_btn" @click="export_to_server()">  
                    <div style="margin: 2%;">ОК</div>
                  </button>
                  <button class="pat_btn" @click="check_savepat = !check_savepat">
                  <div style="margin: 2%;"> Отмена </div>
                  </button>
                </div>
              </div>
            </div>
            <!-- /Кнопка сохранения шаблона -->
          </div>

          <button class="btn_calc" @click="calc_all()">
            <div style="margin: 2%;"> Расчёт </div>
          </button>
        </div>
        <select>
            <option>2018-2019</option>
            <option>2018-2019</option>
            <option>2019-2020</option>
            <option>2020-2021</option>
            <option>2021-2022</option>
        </select>
        <!-- /Пространство кнопок загрузки шаблонов ------------------------------------------->


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
                        <div class="block_title">{{ func.title }}</div><br>
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
              <div v-for="result in results" v-bind:key=result>
                <div v-if="result.id===section.name" >
                  <div class="btn_div">
                    <button v-show="section.name!=='general'" class="btn_calc" v-on:click="cacl_result(result.id)">
                      <div style="margin: 2%;"> Расчёт </div>
                    </button>
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
  <!--/Основная часть ----------------------------------------------------------------------->



  <dialogbox-login v-model:show=login_reg_check>
  </dialogbox-login> 
  <dialogbox-reg v-model:show=login_reg_check>
  </dialogbox-reg> 
  <dialog-buttons v-model:show=dialog_buttons_check @result="calc_all_after_dialog" v-model:name="functions[0].input[0][2]" 
     @update:name="this.changes(0, 'input', 0, $event.target.value)" v-model:error_show="savepat_error.show" 
     v-model:error_text="savepat_error.text"
     >
  </dialog-buttons>     
</div>
</template>



<script>
import func from '@/connect/funcs'
import login_funcs from '@/connect/login'
export default{
  data(){
    return {
      dialog_buttons_check: false,
      login_reg_check:[false,false],
      menu_check: '20',
      settings_check: '0',
      check_savepat: false,
      check_loadpat: false,
      build_changes: new Set(),
      load_pat: {
        select: {
          variants: [],
          ids: [],
          picked: ''
        }
      },
      savepat: {
        radio: {
          picked: 'Сохранять только из выбранных расчётов'
        }
      },
      loadpat_error: {show: false, text: ''},
      savepat_error: {show: false, text: ''},
      
      big_sections_name:
      [
        {name: 'Надежность'},
        {name: 'Теплопотери'},
        {name: 'Теплопритоки'}
      ],
      sections:
      [
        {  section:'Общая характеристика здания', name: 'general', title: 'Общая характеристика здания', check: 'false', main_block_width: '50', check_savepat: false, check_loadpat: false, loadpat_error: {show: false, text: ''}, savepat_error: {show: false, text: ''}},
        {  section:'Надежность', name: 'reliability', title: 'Надежность', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'heat_los_win', title: 'Расчет тепловых потерь через окна', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'inf_win', title: 'Расчет инфильтрации через окна', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'heat_los_inpgr', title: 'Расчет тепловых потерь через входную группу', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'inf_inpgr', title: 'Расчет инфильтрации через входную группу', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'heat_los_heatcond_benv', title: 'Определение теплопотерь посредством теплопроводности через ограждающие конструкции', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'heat_los_heatcond_roof', title: 'Определение теплопотерь посредством теплопроводности через кровлю', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'heat_los_floor', title: 'Расчет теплопотерь через пол', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'heat_los_vent', title: 'Расчет теплопотерь, связанных с вентиляцией', check: 'false', main_block_width: '69'},
        {  section:'Теплопотери', name: 'add_heatcosts', title: 'Дополнительные затраты теплоты на повторный прогрев внутренних перегородок и интерьеров', check: 'false', main_block_width: '69'},
        {  section:'Теплопритоки', name: 'heat_gains_people', title: 'Определение теплопритоков от людей', check: 'false', main_block_width: '69'},
        {  section:'Теплопритоки', name: 'heat_gains_washstands', title: 'Определение затрат тепловой энергии на ГВС для рукомойников', check: 'false', main_block_width: '69'},
        {  section:'Теплопритоки', name: 'heat_gains_showers', title: 'Определение затрат тепловой энергии на ГВС для душевых', check: 'false', main_block_width: '69'},
        {  section:'Теплопритоки', name: 'heat_gains_electriclighting', title: 'Определение теплопритока от систем электроосвещения и силового электроснабжения', check: 'false', main_block_width: '69'},
        {  section:'Теплопритоки', name: 'heat_gains_GVS', title: 'Определение теплопритока от неизолированных трубопроводов ГВС', check: 'false', main_block_width: '69'},
        {  section:'Теплопритоки', name: 'heat_gains_pipelines', title: 'Определение теплопритока от неизолированных трубопроводов отопления', check: 'false', main_block_width: '69'},
      ],
      results: [
        {id: 'general', val: '', dec:''},
        {id: 'reliability', val: '', dec:''},
        {id: 'heat_los_win', val: '', dec:''},
        {id: 'inf_win', val: '', dec:''},
        {id: 'heat_los_inpgr', val: '', dec:''},
        {id: 'inf_inpgr', val: '', dec:''},
        {id: 'heat_los_heatcond_benv', val: '', dec:''},
        {id: 'heat_los_heatcond_roof', val: '', dec:''},
        {id: 'heat_los_floor', val: '', dec:''},
        {id: 'heat_los_vent', val: '', dec:''},
        {id: 'add_heatcosts', val: '', dec:''},
        {id: 'heat_gains_people', val: '', dec:''},
        {id: 'heat_gains_washstands', val: '', dec:''},
        {id: 'heat_gains_showers', val: '', dec:''},
        {id: 'heat_gains_electriclighting', val: '', dec:''},
        {id: 'heat_gains_GVS', val: '', dec:''},
        {id: 'heat_gains_pipelines', val: '', dec:''},
      ],
      functions:
      [    
        // 0 общая характеристика здания  ---------------------------------------------------------------------
        {
          id: 'general', 
          title:'Параметры', 
          //input[2] - значение, input[3] - тип, input[4] - валидность, input[5] - пусто/[func_index, input_index], input[6] - пусто/условный рендер - функция проверки
          input:[['Название','', '', 'str', false],['Этажность','', '', 'uint', false],['Длина здания','м', '', 'uint', false],['Ширина здания','м', '', 'uint', false],['Длина стен на одном этаже','м', '', 'uint', false],['Высота стен','м', '', 'uint', false],['Температура внутреннего воздуха','°C',  '', 'int', false],['Температура наружного воздуха','°C',  '', 'int', false]],
          r_btn:null,
          //теперь  select[2] - массив id, select[3] - выбранный вариант, select[4]  - пусто/[func_index, select_index], select[5] - пусто/условный рендер - функция проверки
          select:null,
          c_box:null,
          date:[['Дата постройки','2011-12-15']]
        },
        //------------------------------------------------------------------------------------------------------------------
        // 1 Надежность - блок 1
        {
          id: 'reliability', 
          title:'Тепловой пункт', 
          input:null,
          r_btn:['Элеватор',  'ИТП'], 
          select:[['Тип насоса',['Насос ЧРП','Насос 1'], [], '', null, this.condition_render_itp],['Тип теплообменика',['Теплообменик пластинчатый','Теплообменник \'труба в трубе\''], [], '', null, this.condition_render_itp]],
          c_box:['Наличие подогрева приточного воздуха'],
          date:null, 
          radio_elem: ['ИТП'], // хранит выбранный r_btn
          check_elem: [false]     // хранит значения чекбоксов
        },
        // 2 Надежность - блок 2
        {
          id: 'reliability', 
          title:'Система подогрева приточного воздуха', 
          input:[['Число установок','ед.', '', 'uint', false],['Длина трубы от ТП до установки №1','м', '', 'uint', false],['Длина трубы от ТП до установки №2','м',  '', 'uint', false]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null,
          render: false //отвечает за отрисовку
        },
        // 3 Надежность - блок 3
        {
          id: 'reliability', 
          title:'Система ГВС с рециркуляцией', 
          input:[['Число подъёмов ГВС','ед.', '', 'uint', false],['Число опусков ГВС','ед.', '', 'uint', false],['Число кранов на каждом этаже (от одного опуска)','ед.', '', 'uint', false]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        }, 
        // 4 Надежность - блок 4
        {
          id: 'reliability', 
          title:'Система отопления здания', 
          input:[['Число подъёмов от ТП до чердака','ед.', '', 'uint', false],['Число опусков от чердака до ТП','ед.', '', 'uint', false],['Число отопительных приборов на этаже (от одного опуска)','ед.', '', 'uint', false]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },      
        // 5
        {
          id: 'heat_los_win', 
          title:'Характеристика окон', 
          input:[['Число окон','ед.', '', 'uint', false],['Длина типового окна','м',  '', 'uint', false],['Высота типового окна','м',  '', 'uint', false], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '']]],
          r_btn:null, 
          select:[['Тип окон',['Деревянные окна с двойным остеклением','Стеклопакет 24мм (4-16-4) в корпусе ПВХ','Стеклопакет 24мм (4-16-4) в корпусе ПВХ, низкоэмиссионное покрытие','Стеклопакет 36мм (4-10-4-14-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ, низкоэмиссионное покрытие']]],
          c_box:null,
          date: [['Дата установки окон','2011-11-12'], ['Дата постройки','2011-12-15', [0, 0,'']]]
        },
        // 6
        {
          id: 'inf_win', 
          title:'Характеристика окон', 
          input:[['Число окон','ед.',  '', 'uint', false, [5, 0, '']],['Длина типового окна','м',  '', 'uint', false, [5, 1, '']],['Высота типового окна','м',  '', 'uint', false, [5, 2, '']], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '']]],
          r_btn:null, 
          select:[['Тип окон',['Деревянные окна с двойным остеклением','Стеклопакет 24мм (4-16-4) в корпусе ПВХ','Стеклопакет 24мм (4-16-4) в корпусе ПВХ, низкоэмиссионное покрытие','Стеклопакет 36мм (4-10-4-14-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ, низкоэмиссионное покрытие'], [], '', [5,0, '']]],
          c_box:null,
          date: [['Дата установки окон','2011-11-12', [5, 0,'']], ['Дата постройки','2011-12-15', [0, 0,'']]]
        },
        // 7
        {
          id: 'heat_los_inpgr', 
          title:'Характеристика входной группы', 
          input:[['Число дверей','ед.',  '', 'uint', false],['Длина типовой входной двери','м',  '', 'uint', false],['Высота типовой входной двери','м',  '', 'uint', false], ['Этажность', '', '', 'uint', false, [0, 1, '']], ['Высота стен','м', '', 'uint', false, [0, 5, '']], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '']]],
          r_btn:null, 
          select:[['Тип двери',['Двери одинарные деревянные без тамбура','Двери одинарные деревянные с тамбуром между ними','Двери двойные (распашные) деревянные без тамбура','Двери двойные (распашные) деревянные с тамбуром между ними','Двери одинарные ПВХ без тамбура','Двери одинарные ПВХ с тамбуром между ними','Двери двойные (распашные) ПВХ без тамбура','Двери двойные (распашные) ПВХ с тамбуром между ними','Двери одинарные алюминиевые без тамбура','Двери одинарные алюминиевые с тамбуром между ними','Двери двойные (распашные) алюминиевые без тамбура','Двери двойные (распашные) алюминиевые с тамбуром между ними']]],
          c_box:null,
          //data[2]  - пусто/[func_index, input_index, text]
          date: [['Дата установки дверей','2011-11-12'], ['Дата постройки','2011-12-15', [0, 0,'']]]
        }, 
        
        // 8
        {
          id: 'inf_inpgr',
          title:'Характеристика входной группы', 
          input:[['Число дверей','ед.',  '', 'uint', false, [7, 0, '']],['Длина типовой входной двери','м',  '', 'uint', false, [7, 1, '']],['Высота типовой входной двери','м',  '', 'uint', false, [7, 2, '']], ['Этажность', '', '', 'uint', false, [0, 1, '']], ['Высота стен','м', '', 'uint', false, [0, 5, '']], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '']]],
          r_btn:null, 
          select:[['Тип двери',['Двери одинарные деревянные без тамбура','Двери одинарные деревянные с тамбуром между ними','Двери двойные (распашные) деревянные без тамбура','Двери двойные (распашные) деревянные с тамбуром между ними','Двери одинарные ПВХ без тамбура','Двери одинарные ПВХ с тамбуром между ними','Двери двойные (распашные) ПВХ без тамбура','Двери двойные (распашные) ПВХ с тамбуром между ними','Двери одинарные алюминиевые без тамбура','Двери одинарные алюминиевые с тамбуром между ними','Двери двойные (распашные) алюминиевые без тамбура','Двери двойные (распашные) алюминиевые с тамбуром между ними'], [], '', [7,0, '']]],
          c_box:null,
          date: [['Дата установки дверей','2011-11-12', [7, 0,'' ]], ['Дата постройки','2011-12-15', [0, 0,'' ]]]
        },
        // 9
        {
          id: 'heat_los_heatcond_benv',
          title:'Характеристика класса энергетической эффективности', 
          input:[['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '']], ['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']], ['Этажность', '', '', 'uint', false, [0, 1, '']],['Высота стен','м', '', 'uint', false, [0, 5, '']], ['Число окон','ед.',  '', 'uint', false, [5, 0, '']], ['Длина типового окна','',  '', 'uint', false, [5, 1, '']],['Высота типового окна','',  '', 'uint', false, [5, 2, '']], ['Число дверей','ед.',  '', 'uint', false, [7, 0, '']], ['Длина типовой входной двери','',  '', 'uint', false, [7, 1, '']], ['Высота типовой входной двери','',  '', 'uint', false, [7, 2, '']]],
          r_btn:null, 
          select:[['Класс энергетической эффективности ограждающих конструкций',['A++ (очень высокий)','A+ (очень высокий)','A (очень высокий)','B+ (высокий)','B (высокий)','C+ (нормальный)','C (нормальный)','C- (нормальный)','D (пониженный)','E (низкий)']]],
          c_box:null,
          date:[['Дата постройки','2011-12-15', [0, 0,'' ]]],
        },
        // 10
        {
          id: 'heat_los_heatcond_roof',
          title:'Характеристика класса энергетической эффективности', 
          input:[['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '']], ['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']]],
          r_btn:null, 
          select:[['Класс энергетической эффективности кровли',['A++ (очень высокий)','A+ (очень высокий)','A (очень высокий)','B+ (высокий)','B (высокий)','C+ (нормальный)','C (нормальный)','C- (нормальный)','D (пониженный)','E (низкий)']]],
          c_box:null,
          date:null,
        },
        // 11
        {
          id: 'heat_los_floor', 
          title:'Тепловые потери через пол', 
          input:[['Высота подвала','м',  '', 'uint', false],['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '']], ['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']], ['Длина стен на одном этаже','м', '', 'uint', false, [0, 4, '']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 12
        {
          id: 'heat_los_vent', 
          title:'Тепловые потери от вентиляции', 
          input:[['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '']], ['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']], ['Высота стен','м', '', 'uint', false, [0, 5, '']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 13
        {
          id: 'add_heatcosts', 
          title:'Характеристика интерьера и перегородок', 
          input:[['Число дверей','ед.',  '', 'uint', false],['Число шкафов','ед.',  '', 'uint', false],['Число диванов','ед.',  '', 'uint', false],['Число столов','ед.',  '', 'uint', false],['Число навесных шкафчиков','ед.',  '', 'uint', false], ['Этажность','', '', 'uint', false, [0, 1, '']],['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']],['Длина стен на одном этаже','м', '', 'uint', false, [0, 4, '']],['Высота стен','м', '', 'uint', false, [0, 5, '']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 14
        {
          id: 'add_heatcosts', 
          title:'В здании многофункционального назначения реализовано энергосберегающее мероприятие – введение в нерабочее время пониженного (до +12°С) температурного графика отопления', 
          input:null,
          r_btn:null, 
          select:[['Периодичность',['Еженочно в рабочие дни и все выходные дни','Еженочно каждый календарный день','Раз в неделю (режим загородного дома)','Без понижения температуры']]],
          c_box:null,
          date:null
        },
        // 15
        {
          id: 'add_heatcosts', 
          title:'Выберите варианты состава основных объектов', 
          input:null,
          r_btn:null, 
          select:[['Стены',['Штукатурка + ротбанд + кирпич глиняный пустотелый + ротбанд + штукатурка','Штукатурка + ротбанд + газобетон + ротбанд + штукатурка','Штукатурка + ротбанд + Пенобетон + ротбанд + штукатурка','Штукатурка + ротбанд + железобетон + ротбанд + штукатурка','Штукатурка + ротбанд + дерево (сосна) + ротбанд + штукатурка','Штукатурка + ротбанд + Пенополистерол + ротбанд + штукатурка','Штукатурка + ротбанд + Керамзитобетон + ротбанд + штукатурка']],['Полы',['Линолеум','Плиточный клей + плитка','Фанера (сосна) + паркет (сосна)','Фанера (сосна) + паркет (пихта)','Фанера (сосна) + паркет (клён)','Фанера (сосна) + паркет (липа)','Фанера (сосна) + паркет (дуб)']],['Двери',['Сосна','Пихта','Клён','Липа','Дуб','ДСП']],['Твёрдокорпусная мебель',['Сосна','Пихта','Клён','Липа','Дуб','ДСП']],['Диван/кровать',['Сосна','Пихта','Клён','Липа','Дуб','ДСП']], ['Столы',['Сосна','Пихта','Клён','Липа','Дуб','ДСП']],['Навесные шкафы',['Сосна','Пихта','Клён','Липа','Дуб','ДСП']]],
          c_box:null,
          date:null
        },
        // 16
        {
          id: 'heat_gains_people', 
          title:'Определение теплопритоков людей', 
          input:[['Число посетителей/жильцов мужчин','чел.', '', 'uint', false],['Число посетителей/жильцов женщин','чел.', '', 'uint', false],['Число посетителей/жильцов детей','чел.', '', 'uint', false], ['Среднее время пребывания посетителей/жильцов в сутки','чел./сутки', '', 'uint', false], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 17
        {
          id: 'heat_gains_washstands', 
          title:'Определение затрат тепловой энергии на ГВС для рукомойников', 
          input:[['Число посетителей/жильцов мужчин', 'чел.', '', 'uint', false, [16, 0, '']],['Число посетителей/жильцов женщин','чел.', '', 'uint', false, [16, 1, '']],['Число посетителей/жильцов детей','чел.', '', 'uint', false, [16, 2, '']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 18
        {
          id: 'heat_gains_showers', 
          title:'Определение затрат тепловой энергии на ГВС для душевых', 
          input:[['Число посетителей/жильцов мужчин', 'чел.', '', 'uint', false, [16, 0, '']],['Число посетителей/жильцов женщин','чел.', '', 'uint', false, [16, 1, '']], ['Число посетителей/жильцов детей','чел.', '', 'uint', false, [16, 2, '']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 19
        {
          id: 'heat_gains_electriclighting', 
          title:'Определение теплопритока от систем электроосвещения и силового электроснабжения', 
          input:[['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']], ['Этажность', '', '', 'uint', false, [0, 1, '']], ['Объём потребления электрической энергии зданием за отопительный период','кВт · ч / отоп. период', '', 'uint', false, null, this.condition_render_elec_consumption_by_period]],
          r_btn:null, 
          select:null,
          c_box:['Определить расчётным способом'],
          date:null,
          check_elem: [false]     // хранит значения чекбоксов
        },
        // 20
        {
          id: 'heat_gains_GVS', 
          title:'Определение теплопритока от неизолированных трубопроводов ГВС', 
          input:[['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '']], ['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']], ['Этажность', '', '', 'uint', false, [0, 1, '']], ['Высота стен','м', '', 'uint', false, [0, 5, '']], ['Число помещений с раковинами на этаже','ед.', '', 'uint', false, [3, 0, '']]],
          r_btn:null, 
          select:[['Тип трубы',[], [], '', [22,1, '']]],
          c_box:null,
          date:null,
        },
        // 21
        {
          id: 'heat_gains_pipelines', 
          title:'Определение теплопритока от неизолированных трубопроводов отопления', 
          input:[['Температура внутреннего воздуха','°C', '', 'uint', false, [0, 6, '']], ['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']], ['Этажность', '', '', 'uint', false, [0, 1, '']], ['Высота стен','м', '', 'uint', false, [0, 5, '']], ['Количество окон','ед.', '', 'uint', false, [4, 0, '']]],
          r_btn:null, 
          select:[['Тип трубы',[], [], '', [22,1, '']]],
          c_box:null,
          date:null,
        },
        // 22
        {
          id: 'reliability', 
          title:'Данные из общей характеристики здания', 
          input:null,
          r_btn:null, 
          select:[['Тип запорной арматуры',[]],['Тип трубы',[]],['Тип радиатора',[]],['Тип крана',[]]],
          c_box:null,
          date:null
        }
      ]
    }
  },
  watch: {
     // для системы подогрева (блок появляется если ihp = true)
      // при каждом изменении 'functions[2].input[0][2]' эта функция будет запускаться
      'functions.1.check_elem.0' (new_val) {
         this.functions[2].render = new_val
      },
      // для системы подогрева (к-во полей ввода зависит от числа в input'e)
      // при каждом изменении 'functions[2].input[0][2]' эта функция будет запускаться
      'functions.2.input.0.2' (new_val) {
        if(new_val != "" && !isNaN(Number(new_val)) && this.functions[2].input.length-1 != new_val) {
          let len = this.functions[2].input.length-1
          if(len < new_val){
            for(let i = 0; i != new_val-len; ++i){
              console.log("push")
              this.functions[2].input.push(['Длина трубы от ТП до установки №'+(len+i+1),'м',  '', 'uint', false])
            }
          }
          else if(len > new_val){
            for(let i = 0; i != len-new_val; ++i){
               this.functions[2].input.pop()
            }
          }
        }
      }
    },
  methods:{
    logout(){
      localStorage.setItem("token", null)
      login_funcs.logout()
      window.location.href = "/"
    },
    Change_check_loadpat(name){
      this.sections.forEach(function(item){
        if(item.name === name){
          item.check_loadpat = !item.check_loadpat;
        }
      })
      return name;
    },
    Change_check_savepat(name){
      this.sections.forEach(function(item){
        if(item.name === name){
          item.check_savepat = !item.check_savepat;
        }
      })
      return name;
    },
    cacl_result(id){
        let self = this
        console.log(self)
      this.results.forEach(function(item){
        if(item.id == id){
            let calc_res = func.calc(id, self)
            console.log(calc_res)
            item.val = calc_res[0]
            item.dec = func.calc_dec(id, self, calc_res[1])
            return false
        }
      })
      return id
    },
  calc_all_server(){
    let self = this
    this.sections.forEach(function(item){
      if(item.check){
        self.cacl_result(item.name, self)
      }
    })
  },
    calc_all(){
        console.log(this.functions[1].radio_elem)
    if(this.build_changes.size > 0){
      this.dialog_buttons_check = true
    }
    else{
      this.calc_all_server()
    }
    },
  calc_all_after_dialog(val_pair){
    let val = val_pair[0]
    let mode = val_pair[1]
    switch (val) {
      //save
      case 0:
        this.export_to_server_and_calc(mode)
        break;
      //server
      case 1:
        this.calc_all_server()
        break;
      //отмена
      case 2:
        break;
      default:
        console.log("calc_all_after_dialog:logic_error")
        break;
    }
  },
    validate_input(val, type){
      if(type == 'str'){
        return val.length > 0
      }
      else if(type == 'uint'){
        let num = Number(val)
        return val != "" && !isNaN(num) && num >= 0
      }
      else  if(type == 'int'){
        let num = Number(val)
        return val != "" && !isNaN(num)
      }
      return true
    },
    condition_render_itp(){
        return this.functions[1].radio_elem && this.functions[1].radio_elem[0]  == 'ИТП'
    },
    condition_render_elec_consumption_by_period(){
        return !this.functions[19].check_elem[0]
    },
    // отслеживание изменений
    changes(func_ind, type, dataid, new_val){
        let result = false
        if(type == 'input'){
            if(this.functions[func_ind].input[dataid][2] !== new_val){
                this.functions[func_ind].input[dataid][2] = new_val
                this.functions[func_ind].input[dataid][4] = 
                    this.validate_input(new_val.trim(), this.functions[func_ind].input[dataid][3])
                result = true
            }
        }
        else if(type == "select"){
            if(this.functions[func_ind].select[dataid][3] !== new_val){
                this.functions[func_ind].select[dataid][3] = new_val
                result = true
            }
        }
        else if(type == "checkbox"){
            if(this.functions[func_ind].check_elem[dataid] !=  new_val){
                this.functions[func_ind].check_elem[dataid] = new_val
                result = true
            }
        }
        else if(type == "radio"){
            if(this.functions[func_ind].radio_elem[0] !== new_val){
                this.functions[func_ind].radio_elem[0] = new_val
                result = true
            }
        }
        else if(type == "date"){
            if(this.functions[func_ind].date[dataid][1] !== new_val){
                this.functions[func_ind].date[dataid][1] = new_val
                result = true
            }
        }
        if(result){
            console.log("changed")
            this.build_changes.add(this.functions[func_ind].id)
        }
    },  
    export_to_server(){
      func.export(this, this.savepat.radio.picked != 'Сохранять только из выбранных расчётов', true)
    },
    export_to_server_and_calc(mode){
      func.export(this, mode != 'Сохранять только из выбранных расчётов', true, function(self){self.calc_all()})
    },
    import_from_server(){
      func.import(this)
    }
  },
  beforeCreate(){
    
  },
  mounted() {
      // Проверить валидность токена
      let user_token = {"token": localStorage.getItem("token")}
      let res = func.check_token_before_render(user_token)
      if (res){
        // Закрываем окно входа
        this.login_reg_check[0] = false
        //console.log(this.login_reg_check)
        func.start(this)
        func.load(this)
        
      } else {
        // Переходим на страницу входа
        this.login_reg_check[0] = true
        //console.log(this.login_reg_check)
      }  
  },
}
</script>

<style>
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box; 
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
}
/* Глобальные --------------------------------------------------------------- */
select{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin:0.25%;
  margin-left: 2%;
  width: 26%;
}
#big_select{
  width:100%;
}
label{
  margin-left: 2%;
  cursor: inherit;
  user-select: inherit;
  width: 100%;
}
.app{
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
br{
margin: 0;
padding: 0;
}
/* /Глобальные --------------------------------------------------------------- */


/*--Заголовок---------------------------------------------------------------- */
.header{
  position: fixed;
  display: flex;
  flex-direction: row;
  margin: auto;
  width: 100%;
  height: 50px;
  background: #26495c;
  color: #e5e5dc;
  z-index: 20;
}
.exit_label{
  display: flex;
  align-items: center;
  user-select: none; 
  font-size: 150%;
  height: 100%;
}
.settings_title
{
  margin-top: 10px;
  margin-left: 3%;
  margin-bottom: 2%;
  font-size: 130%;
  color: #435d6b;
}

.settings_param_name
{
  color: black;
  margin: 0.3%;
  margin-left: 2%;
}
.settings_param_input{
  background-color: #e5e5dc;
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.3%;
  margin-left: 2%;
  width: 26%;
}
.settings_param_date{
  background-color: #e5e5dc;
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.3%;
  margin-left: 2%;
}

.header_menu{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50px;
}
.header_text{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 20px;
  padding-right: 20px;
  width: 90%;
}
.header_title{
  font-size: 36px;
}
.header_cb_transparent{
  opacity: 0;
}
.strip{
  width: 35px;
  height: 5px;
  background-color: #e5e5dc;
  margin-top: 3px;
  margin-bottom: 3px;
}
/*--/Заголовок--------------------------------------------------------------- */


.body{
  margin-top: 50px;
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: row;
}
.right_panel
{
  position: fixed;
  border-left: 5px solid #435d6b;
  background: #e5e5dc;
  top: 50px;
  bottom: 0px;
  left: 70%; 
  width: 100%;
  overflow-y: scroll;
  z-index: 100;
}
/*-- Вкладки в левой части экрана ------------------------------------------- */
.left_panel{
  position: fixed;
  background: #e28a16;
  top: 50px;
  bottom: 0px;
  width: 20%;
  overflow-y: scroll;
  min-width: 170px;
  z-index: 20;
}
.glob_section_title{
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 1%;
  color: #e5e5dc;
  font-size: 16px;
}
.sub_section_title{
  display: flex;
  flex-direction: row;
  align-items: center;
  min-height: 38px;
  margin: 2%;
  color: #0b161d;
  border-bottom: 2px dotted rgb(0, 0, 0);
  user-select: none;
}
.sub_section_title:hover{
  background-color: #e0886563;
  cursor: pointer;
  transition: background-color 300 ms;
}
/*-- /Вкладки в левой части экрана ------------------------------------------- */


/* Основное рабочее пространство ---------------------------------------------*/
.solution{ 
  display: flex;
  flex-direction: column;
  width: 100%;
}

  /* Пространство кнопок загрузки шаблонов и расчета */
.btn_div_global{
  display: flex;
  justify-content: space-between;
  margin: 2%;
  margin-left:  8%;
  margin-right: 8%;
  align-items: start;
}
.btn_patterns{
  display: flex;
  align-items: start; 
  justify-content: space-between;
  width: 73%;
}

.btn_loadpat{
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 48%;
}

.btn_savepat{
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 48%; 
}

.btn_pat{
  width: 100%; 
  background-color: #e28a16; 
  border: 2px solid #d47e0c;
  border-radius: 10px; 
  box-shadow: 0 0 10px #b96e0b;
  color: #e5e5dc;
  transition: box-shadow 300ms ease-in-out, color 300ms ease-in-out;
}
.btn_pat:hover{
  width: 100%; 
  background-color: #e28a16; 
  border: 2px solid #d47e0c;
  border-radius: 10px; 
  box-shadow: 0 0 5px #b96e0b inset;
  color: #e5e5dc;
}
.show_pat{
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;
  background: #e5e5dc;
  border: 2px solid #e28a16;
  position: relative;
  border-radius: 4px; 
  padding: 2%;
  margin: 1%;
}
.content{
  display: flex;
  flex-direction: column;
  margin: 1%;
}
.pat_buttons{
  display: flex;
  justify-content: space-between;
}
.pat_btn{
  display: flex;
  justify-content: center;
  width: 30%; 
  background-color: #26495c; 
  border: 2px solid #234455;
  border-radius: 10px; 
  box-shadow: 0 0 10px #1e3a49;
  color: #e5e5dc;
  transition: box-shadow 300ms ease-in-out, color 300ms ease-in-out;
}
.pat_btn:hover{
  display: flex;
  justify-content: center;
  width: 30%; 
  background-color: #26495c; 
  border: 2px solid #234455;
  border-radius: 10px; 
  box-shadow: 0 0 5px #1e3a49 inset;
  color: #e5e5dc;
}

.inp_pat{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.25%;
}
.btn_calc{
  display: flex;
  justify-content: center;
  width: 25%; 
  background-color: #26495c; 
  border: 2px solid #234455;
  border-radius: 10px; 
  box-shadow: 0 0 10px #1e3a49;
  color: #e5e5dc;
  transition: box-shadow 300ms ease-in-out, color 300ms ease-in-out;
}
.btn_calc:hover{
  display: flex;
  justify-content: center;
  width: 25%; 
  background-color: #26495c; 
  border: 2px solid #234455;
  border-radius: 10px; 
  box-shadow: 0 0 5px #1e3a49 inset;
  color: #e5e5dc;
}
  /* /Пространство кнопок загрузки шаблонов и расчета */

  /* Отрисовка основных блоков расчета */
.mega_block_sections{
display: flex; 
flex-direction: column;
margin: 1%;
margin-left: 6%;
margin-right: 6%;
}
.mega_block_title{
  font-size: 20px;
  margin-left: 2%;
}
.mega_block_borders{
  display: flex; 
  flex-direction: column;
  justify-content: right;
  border: 2px solid #e28a16;
  border-radius: 10px; 
  box-shadow: 0 0 10px #cf7b0c;
  background-color: #f9d2a2; 
  margin: 1% 1% 0%;
}
.mega_block{
  display: flex;
  flex-direction: row;
  background-color: #f9d2a2; 
  border: 6px solid #f9d2a2; 
  border-top: #e28a16; 
  border-right: #e28a16; 
  border-radius: 10px; 
}
.main_block{
  margin: 1% 2% 0%;
  position: relative;
  display: block;
}
.rel_block{
  flex-direction: column;
  margin: 1% 2% 0%;
  position: relative;
  display: flex;
}
.block{
  background-color: #e5e5dc; 
  border: 2px solid #e28a16;
  border-radius: 10px; 
  box-shadow: 0 0 10px #cf7b0c;
  width: 100%;
  margin-bottom: 1%;
  padding: 10px;
}
.gen_block{
  background-color: #e5e5dc; 
  border: 2px solid #e28a16;
  border-radius: 10px; 
  box-shadow: 0 0 10px #cf7b0c;
  width: 100%;
  margin-bottom: 1%;
  padding: 10px;
}

.block_title{
  font-size: 16px;
  color:#1e3a49;
}
.field_inp, .field_inp_name, .field_select_readonly{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.55%;
  width: 15%;
}
.field_inp_name{
  width: 75%;
}
.field_select_readonly{
  width: 280%;
}
.sum_block{
  background-color: #e5e5dc; 
  margin: 2%;
  margin-left:  8%;
  margin-right: 8%;
  padding: 10px;
  border-radius: 10px;
  border: 2px solid #e28a16;
  box-shadow: 0 0 10px #cf7b0c;
  
}
#sum_minus {
float: left; 
display: block;
width: 44%;
margin-left: 4%;
position: relative;
justify-content: space-between;
}
#sum_plus {
float: right;
display: block;
width: 44%;
margin-left: 4%;
margin-right: 4%;
position: relative;
justify-content: space-between;
}
.red_sum{
  color: #234455;
  vertical-align: text-bottom ;
  display: inline;
}
.sum_titles{
  display: flexbox;
  float: left;
  width: 30%;
}
.sum_results{
  display: flexbox;
  float: right;
  width: 68%;
  margin-right: 2%;
  text-align: right;
}
.res_block{
  width: 29%;
  margin: 1% 1% 0%;
}
.block_r{
  background-color: #e5e5dc; 
  border: 2px solid #26495c;
  border-radius: 10px; 
  box-shadow: 0 0 10px #1e3a49;
  width: 100%;
  height: 99%;
  margin-bottom: 1%;
  padding: 20px 40px;
}
.btn_div{
  display: flex;
  align-items: center;
  justify-content: right;
  margin: 1%;
  background-color: #f9d2a2;
}
input[type="date"]{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.25%;
  margin-left: 2%;
  width: 26%;
}
input[type="checkbox"]{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  transform:scale(1.2);
}

#name_of_scheme
{
  font-size: 24px;
  margin: 2%;
  margin-left: 8%;
  margin-right: 8%;
  margin-bottom: 0%;
  border: 2px solid #435d6b;
  box-shadow: 0 0 10px #1e3a49;
  border-radius: 4px;
  padding-left: 1%;
}
  /* /Отрисовка основных блоков расчета */

/* /Основное рабочее пространство--------------------------------------------*/

</style>
