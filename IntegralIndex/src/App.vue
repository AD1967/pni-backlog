<template>
<div class="app">
  <div class="header">
    <div style="display: flex;">
      <input class="cb_transparent" type="checkbox" id="id_menu" v-model="menu_check" true-value="0" false-value="20"/>
      <label for="id_menu" class="header_menu">
        <label for="id_menu" class="strip"></label>
        <label for="id_menu" class="strip"></label>
        <label for="id_menu" class="strip"></label>
      </label>
    </div>
    <div class="header_text">
      <div class="header_title">Интегральный индекс</div>
      <div class="header_registration">
        <!-- <input class="cb_transparent" type="checkbox" id="login_but" v-model="login_reg_check[0]" true-value=true false-value=false/> -->
        <!-- <label for="login_but" class="reg_label">Вход</label> -->
        <!-- <input class="cb_transparent" type="checkbox" id="reg_but" v-model="login_reg_check[1]" true-value=true false-value=false/> -->
        <!-- <label for="reg_but" class="reg_label">Регистрация</label> -->
        <!-- @click="Change_check_loadpat(top.name)" -->
        <div for="login_but" class="reg_label" @click="logout()">Выход</div>
      </div>
    </div>
  </div>
  <div class="main">  
    <div v-show="menu_check==='20'">
      <div class="function">
        <div v-for="tname in topics_name" v-bind:key=tname>
          <div v-if="tname.name!=='Общая характеристика здания'">
            <h4 class="treecb1">
              {{tname.name}}
            </h4>
            <div v-for="top in topics" v-bind:key=top>
              <div v-if="top.topic===tname.name">
                <h5 class="treecb2">
                  <input type="checkbox" :id=top.name v-model="top.check" true-value="true" false-value="false"/>
                  <label :for=top.name> {{top.title}} </label>  
                </h5>
              </div>
            </div>
          </div>
        </div>
      </div> 
    </div>
    <div :style="{'width': 100+'%'}">
    <div class="solution" :style="{'padding-left': menu_check+'%'}">
      <div class="btn_div_global">
        <div class="btn_patterns" >  
          <div class="btn_loadpat">
            <button class="btn_pat" @click="check_loadpat = !check_loadpat">
              <div style="margin: 2%;"> Загрузить шаблон </div>
            </button>
            <div class="show_pat" v-if="check_loadpat">
              <div class="content"> 
                <b>Выберите шаблон</b>
                
                <select  v-model="load_pat.select.picked">
                  <option style="" v-for="(build) in load_pat.select.variants" v-bind:key=build >
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
        </div>
        <button class="btn_calc" @click="calc_all()">
          <div style="margin: 2%;"> Расчёт </div>
        </button>
      </div>
      <div v-for="top in topics" v-bind:key=top>
        <div v-show="top.check==='true'">
        <div class="topics" :id="top.id">
          <div class="mega_block_title"> {{top.title}} </div>
          <div class="mega_block_borders">
            <div class="mega_block">
              <div class="main_block" :style="{'width': top.main_block_width+'%'}">
                <div v-for="(func, index1) in functions" v-bind:key=func>
                  <div v-if="func.id===top.name && func.render !== false">
                    <div class="block" :id="func.id +'_'+ index1">
                      <div class="block_title">{{ func.title }}</div><br>
                      <div v-for="(inp, indexinp) in func.input" v-bind:key=inp>
                      <div v-if="(inp[6]===undefined || inp[6]===null) || inp[6]()">
                        <div v-if="inp[5]===undefined || inp[5]===null">
                            {{inp[0]}}
                            <input class="block_inp" type="text" :id="func.id +'_'+ index1+'_inp_'+indexinp" 
                            :value="inp[2]" @input="changes(index1, 'input', indexinp, $event.target.value)">
                            {{inp[1]}}
                            <div v-if="!inp[4]">
                            <b style="color:red" v-if="String(inp[2]).trim() === ''">поле не заполнено</b>
                            <b style="color:red" v-if="String(inp[2]).trim() !== '' && (inp[3] == 'int' || inp[3] == 'uint') ">неправильный формат числа</b>
                            </div>
                        </div>
                        <div v-else>
                            {{inp[0]}}
                            <input class="block_inp" type="text" :id="func.id +'_'+ index1+'_inp_'+indexinp" 
                            :value="functions[inp[5][0]].input[inp[5][1]][2]" readonly>
                            {{inp[1]}} <b style="color:grey">{{inp[5][2]}}</b>
                            <div v-if="!functions[inp[5][0]].input[inp[5][1]][4]">
                            <b style="color:red" v-if="String(functions[inp[5][0]].input[inp[5][1]][2]).trim() === ''">поле не заполнено</b>
                            <b style="color:red" v-if="String(functions[inp[5][0]].input[inp[5][1]][2]).trim() !== '' && (functions[inp[5][0]].input[inp[5][1]][3] == 'int' || functions[inp[5][0]].input[inp[5][1]][3] == 'uint') ">неправильный формат числа</b>
                            </div>
                        </div>
                        </div>  
                      </div>
                                               <!-- v-model="newPortalSelect" -->
                       <!-- :value="func.radio_elem[0]" :change="changes(index1, 'radio', 0, $event.target.value)" -->
                      <div v-for="(btn, indexrbtn) in func.r_btn" v-bind:key=btn>
                        <input type="radio" name={{func}} :id="func.id +'_'+ index1+'_rbtn_'+indexrbtn"
                         :value=btn
                          v-on:change="changes(index1, 'radio', 0, $event.target.value)"
                         :checked="btn==func.radio_elem[0]"
                         >
                        <label>{{btn}}</label>
                      </div>
                      <table>
                        <tr>
                          <div v-for="(sel, indexsel) in func.select" v-bind:key=sel>  
                          <div v-if="(sel[5]===undefined || sel[5]===null) || sel[5]()">
                            <div v-if="sel[4]===undefined || sel[4]===null">
                                <td>{{sel[0]}}</td>
                                <select 
                                    :value="sel[3]" @change="changes(index1, 'select', indexsel, $event.target.value)"
                                >
                                <option style="" v-for="(selbody, indexbody) in sel[1]" v-bind:key=selbody :id="func.id +'_'+ index1+'_sel_'+indexsel+'_selnum_'+indexbody">
                                    {{selbody}}
                                </option>
                                </select>
                            </div>
                            <div v-else>
                                <td>{{sel[0] }} <b style="color:grey">{{sel[4][2]}}</b></td>
                                <select :value="functions[sel[4][0]].select[sel[4][1]][3]" disabled="True">
                                <option style="" v-for="(selbody, indexbody) in functions[sel[4][0]].select[sel[4][1]][1]" v-bind:key=selbody :id="func.id +'_'+ index1+'_sel_'+indexsel+'_selnum_'+indexbody" >
                                    {{selbody}}
                                </option>
                                </select>
                                
                            </div>
                           </div>
                        </div>
                        </tr>
                      </table>
                        <!-- :value="func.check_elem[indexcbox]" @change="changes(index1, 'checkbox', indexcbox, $event.target.value)" -->
                       <!-- :checked="func.check_elem[indexcbox]" -->
                      <p v-for="(box, indexcbox) in func.c_box" v-bind:key=box>
                        <input type="checkbox" :id="func.id +'_'+ index1+'_cbox_'+indexcbox" 
                           :checked="func.check_elem[indexcbox]"
                            v-on:input="changes(index1, 'checkbox', indexcbox, $event.target.checked)"
                        >
                        {{box}}
                      </p>
                      <div v-for="(d, indexdate) in func.date" v-bind:key=d>
                            <div v-if="d[2]===undefined || d[2]===null">
                                {{d[0]}}
                                <input type="date" :id="func.id +'_'+ index1+'_date_'+indexdate"
                                :value="d[1]" @input="changes(index1, 'date', indexdate, $event.target.value)">
                            </div>
                            <div v-else>
                                {{d[0]}}
                                <input type="date" :id="func.id +'_'+ index1+'_date_'+indexdate"
                                :value="functions[d[2][0]].date[d[2][1]][1]" readonly>
                                <b  style="color:grey">{{d[2][2]}}</b>
                            </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-show="top.name!=='general'" class="res_block">
                <div class="block_r">
                  <div v-for="result in results" v-bind:key=result>
                    <div v-if="result.id===top.name">
                      <span v-html="result.val"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-for="result in results" v-bind:key=result>
              <div v-if="result.id===top.name" >
                <div class="btn_div">
                  <!--
                  <div class="btn_patterns" :style="{'width': top.main_block_width+'%'}">  
                    <div class="btn_loadpat">
                      <button class="btn_pat" @click="Change_check_loadpat(top.name)">
                        Загрузить шаблон
                      </button>
                      <div class="show_pat" v-if="top.check_loadpat">
                        <div class="content"> 
                          <b>Выберите шаблон</b>
                          <select  v-model="load_pat.select.picked">
                              <option style="" v-for="(build) in load_pat.select.variants" v-bind:key=build >
                                {{build}}
                              </option>
                          </select>
                          <div v-if="top.loadpat_error.show">
                            <div v-if="top.loadpat_error.text == ''">
                            <b style="color:red">
                              Ошибка загрузки шаблона
                            </b>
                            </div>
                            <div v-if="top.loadpat_error.text != ''">
                            <b style="color:red">
                                {{top.loadpat_error.text}}
                            </b>
                            </div>
                          </div>
      
                        </div>
                        <div class="pat_buttons">
                          <button class="pat_btn"  @click="import_from_server()">
                            ОК
                          </button>
                          <button class="pat_btn" @click="Change_check_loadpat(top.name)">
                            Отмена
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="btn_savepat">
                      <button class="btn_pat" @click="Change_check_savepat(top.name)">
                        Сохранить шаблон
                      </button> 
                      <div class="show_pat" v-if="top.check_savepat">
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
                            <div v-if="top.savepat_error.show">
                                <div v-if="top.savepat_error.text == ''">
                                <b style="color:red"> Ошибка сохранения шаблона </b>
                                </div>
                                <div v-if="top.savepat_error.text != ''">
                                <b style="color:red">
                                    {{top.savepat_error.text}}
                                </b>
                            </div>
                          </div>
                        </div>
                        <div class="pat_buttons">
                          <button class="pat_btn"  @click="export_to_server()">
                            ОК
                          </button>
                          <button class="pat_btn" @click="Change_check_savepat(top.name)">
                            Отмена
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  -->
                  <button v-show="top.name!=='general'" class="btn_calc" v-on:click="cacl_result(result.id)">
                    <div style="margin: 2%;"> Расчёт </div>
                  </button>
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
      topics_name:
      [
        {name: 'Общая характеристика здания'},
        {name: 'Надежность'},
        {name: 'Теплопотери'},
        {name: 'Теплопритоки'}
      ],
      topics:
      [
        {  topic:'Общая характеристика здания', name: 'general', title: 'Общая характеристика здания', check: 'true', main_block_width: '100', check_savepat: false, check_loadpat: false, loadpat_error: {show: false, text: ''}, savepat_error: {show: false, text: ''}},
        {  topic:'Надежность', name: 'reliability', title: 'Надежность', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'heat_los_win', title: 'Расчет тепловых потерь через окна', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'inf_win', title: 'Расчет инфильтрации через окна', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'heat_los_inpgr', title: 'Расчет тепловых потерь через входную группу', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'inf_inpgr', title: 'Расчет инфильтрации через входную группу', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери',  name: 'heat_los_heatcond_benv', title: 'Определение теплопотерь посредством теплопроводности через ограждающие конструкции', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'heat_los_heatcond_roof', title: 'Определение теплопотерь посредством теплопроводности через кровлю', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'heat_los_floor', title: 'Расчет теплопотерь через пол', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'heat_los_vent', title: 'Расчет теплопотерь, связанных с вентиляцией', check: 'false', main_block_width: '69'},
        {  topic:'Теплопотери', name: 'add_heatcosts', title: 'Дополнительные затраты теплоты на повторный прогрев внутренних перегородок и интерьеров', check: 'false', main_block_width: '69'},
        {  topic:'Теплопритоки', name: 'heat_gains_people', title: 'Определение теплопритоков от людей', check: 'false', main_block_width: '69'},
        {  topic:'Теплопритоки', name: 'heat_gains_washstands', title: 'Определение затрат тепловой энергии на ГВС для рукомойников', check: 'false', main_block_width: '69'},
        {  topic:'Теплопритоки', name: 'heat_gains_showers', title: 'Определение затрат тепловой энергии на ГВС для душевых', check: 'false', main_block_width: '69'},
        {  topic:'Теплопритоки', name: 'heat_gains_electriclighting', title: 'Определение теплопритока от систем электроосвещения и силового электроснабжения', check: 'false', main_block_width: '69'},
        {  topic:'Теплопритоки', name: 'heat_gains_GVS', title: 'Определение теплопритока от неизолированных трубопроводов ГВС', check: 'false', main_block_width: '69'},
        {  topic:'Теплопритоки', name: 'heat_gains_pipelines', title: 'Определение теплопритока от неизолированных трубопроводов отопления', check: 'false', main_block_width: '69'},
      ],
      results: [
        {id: 'general', val: ''},
        {id: 'reliability', val: ''},
        {id: 'heat_los_win', val: ''},
        {id: 'inf_win', val: ''},
        {id: 'heat_los_inpgr', val: ''},
        {id: 'inf_inpgr', val: ''},
        {id: 'heat_los_heatcond_benv', val: ''},
        {id: 'heat_los_heatcond_roof', val: ''},
        {id: 'heat_los_floor', val: ''},
        {id: 'heat_los_vent', val: ''},
        {id: 'add_heatcosts', val: ''},
        {id: 'heat_gains_people', val: ''},
        {id: 'heat_gains_washstands', val: ''},
        {id: 'heat_gains_showers', val: ''},
        {id: 'heat_gains_electriclighting', val: ''},
        {id: 'heat_gains_GVS', val: ''},
        {id: 'heat_gains_pipelines', val: ''},
      ],
      functions:
      [
        // 0
        {
          id: 'general', 
          title:'Общая характеристика здания', 
          //input[2] - значение, input[3] - тип, input[4] - валидность, input[5] - пусто/[func_index, input_index], input[6] - пусто/условный рендер - функция проверки
          input:[['Название','', '', 'str', false],['Этажность','', '', 'uint', false],['Длина здания','м', '', 'uint', false],['Ширина здания','м', '', 'uint', false],['Длина стен на одном этаже','м', '', 'uint', false],['Высота стен','м', '', 'uint', false],['Температура внутреннего воздуха','°C',  '', 'int', false],['Температура наружного воздуха','°C',  '', 'int', false]],
          r_btn:null,
          //теперь  select[2] - массив id, select[3] - выбранный вариант, select[4]  - пусто/[func_index, select_index], select[5] - пусто/условный рендер - функция проверки
          select:null,
          c_box:null,
          date:[['Дата постройки','2011-12-15']]
        },
        // 1
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
        // 2
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
        // 3 
        {
          id: 'reliability', 
          title:'Система ГВС с рециркуляцией', 
          input:[['Число подъёмов ГВС','ед.', '', 'uint', false],['Число опусков ГВС','ед.', '', 'uint', false],['Число кранов на каждом этаже (от одного опуска)','ед.', '', 'uint', false]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        }, 
        // 4  
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
          input:[['Число окон','ед.',  '', 'uint', false],['Длина типового окна','',  '', 'uint', false],['Высота типового окна','',  '', 'uint', false], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '(берётся из основных характеристик)']]],
          r_btn:null, 
          select:[['Тип окон',['Деревянные окна с двойным остеклением','Стеклопакет 24мм (4-16-4) в корпусе ПВХ','Стеклопакет 24мм (4-16-4) в корпусе ПВХ, низкоэмиссионное покрытие','Стеклопакет 36мм (4-10-4-14-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ, низкоэмиссионное покрытие']]],
          c_box:null,
          date: [['Дата установки окон','2011-11-12'], ['Дата постройки','2011-12-15', [0, 0,'(берётся из основных характеристик)']]]
        },
        // 6
        {
          id: 'inf_win', 
          title:'Характеристика окон', 
          input:[['Число окон','ед.',  '', 'uint', false, [5, 0, '(берётся из теплопотерь через окна)']],['Длина типового окна','',  '', 'uint', false, [5, 1, '(берётся из теплопотерь через окна)']],['Высота типового окна','',  '', 'uint', false, [5, 2, '(берётся из теплопотерь через окна)']], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '(берётся из основных характеристик)']]],
          r_btn:null, 
          select:[['Тип окон',['Деревянные окна с двойным остеклением','Стеклопакет 24мм (4-16-4) в корпусе ПВХ','Стеклопакет 24мм (4-16-4) в корпусе ПВХ, низкоэмиссионное покрытие','Стеклопакет 36мм (4-10-4-14-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ','Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ, низкоэмиссионное покрытие'], [], '', [5,0, '(берётся из теплопотерь через окна)']]],
          c_box:null,
          date: [['Дата установки окон','2011-11-12', [5, 0,'(берётся из теплопотерь через окна)']], ['Дата постройки','2011-12-15', [0, 0,'(берётся из основных характеристик)']]]
        },
        // 7
        {
          id: 'heat_los_inpgr', 
          title:'Характеристика входной группы', 
          input:[['Число дверей','ед.',  '', 'uint', false],['Длина типовой входной двери','',  '', 'uint', false],['Высота типовой входной двери','',  '', 'uint', false], ['Этажность', '', '', 'uint', false, [0, 1, '(берётся из основных характеристик)']], ['Высота стен','м', '', 'uint', false, [0, 5, '(берётся из основной характеристики)']], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '(берётся из основных характеристик)']]],
          r_btn:null, 
          select:[['Тип двери',['Двери одинарные деревянные без тамбура','Двери одинарные деревянные с тамбуром между ними','Двери двойные (распашные) деревянные без тамбура','Двери двойные (распашные) деревянные с тамбуром между ними','Двери одинарные ПВХ без тамбура','Двери одинарные ПВХ с тамбуром между ними','Двери двойные (распашные) ПВХ без тамбура','Двери двойные (распашные) ПВХ с тамбуром между ними','Двери одинарные алюминиевые без тамбура','Двери одинарные алюминиевые с тамбуром между ними','Двери двойные (распашные) алюминиевые без тамбура','Двери двойные (распашные) алюминиевые с тамбуром между ними']]],
          c_box:null,
          //data[2]  - пусто/[func_index, input_index, text]
          date: [['Дата установки дверей','2011-11-12'], ['Дата постройки','2011-12-15', [0, 0,'(берётся из основных характеристик)']]]
        },
        // 8
        {
          id: 'inf_inpgr',
          title:'Характеристика входной группы', 
          input:[['Число дверей','ед.',  '', 'uint', false, [7, 0, '(берётся из теплопотерь через входную группу)']],['Длина типовой входной двери','',  '', 'uint', false, [7, 1, '(берётся из теплопотерь через входную группу)']],['Высота типовой входной двери','',  '', 'uint', false, [7, 2, '(берётся из теплопотерь через входную группу)']], ['Этажность', '', '', 'uint', false, [0, 1, '(берётся из основных характеристик)']], ['Высота стен','м', '', 'uint', false, [0, 5, '(берётся из основной характеристики)']], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'uint', false, [0, 7, '(берётся из основных характеристик)']]],
          r_btn:null, 
          select:[['Тип двери',['Двери одинарные деревянные без тамбура','Двери одинарные деревянные с тамбуром между ними','Двери двойные (распашные) деревянные без тамбура','Двери двойные (распашные) деревянные с тамбуром между ними','Двери одинарные ПВХ без тамбура','Двери одинарные ПВХ с тамбуром между ними','Двери двойные (распашные) ПВХ без тамбура','Двери двойные (распашные) ПВХ с тамбуром между ними','Двери одинарные алюминиевые без тамбура','Двери одинарные алюминиевые с тамбуром между ними','Двери двойные (распашные) алюминиевые без тамбура','Двери двойные (распашные) алюминиевые с тамбуром между ними'], [], '', [7,0, '(берётся из теплопотерь через входную группу)']]],
          c_box:null,
          date: [['Дата установки дверей','2011-11-12', [7, 0,'(берётся из теплопотерь через входную группу)' ]], ['Дата постройки','2011-12-15', [0, 0,'(берётся из основных характеристик)' ]]]
        },
        // 9
        {
          id: 'heat_los_heatcond_benv',
          title:'Характеристика класса энергетической эффективности', 
          input:[['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '(берётся из основных характеристик)']], ['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']], ['Этажность', '', '', 'uint', false, [0, 1, '(берётся из основных характеристик)']],['Высота стен','м', '', 'uint', false, [0, 5, '(берётся из основной характеристики)']], ['Число окон','ед.',  '', 'uint', false, [5, 0, '(берётся из теплопотерь через окна)']], ['Длина типового окна','',  '', 'uint', false, [5, 1, '(берётся из теплопотерь через окна)']],['Высота типового окна','',  '', 'uint', false, [5, 2, '(берётся из теплопотерь через окна)']], ['Число дверей','ед.',  '', 'uint', false, [7, 0, '(берётся из теплопотерь через входную группу)']], ['Длина типовой входной двери','',  '', 'uint', false, [7, 1, '(берётся из теплопотерь через входную группу)']], ['Высота типовой входной двери','',  '', 'uint', false, [7, 2, '(берётся из теплопотерь через входную группу)']]],
          r_btn:null, 
          select:[['Класс энергетической эффективности ограждающих конструкций',['A++ (очень высокий)','A+ (очень высокий)','A (очень высокий)','B+ (высокий)','B (высокий)','C+ (нормальный)','C (нормальный)','C- (нормальный)','D (пониженный)','E (низкий)']]],
          c_box:null,
          date:[['Дата постройки','2011-12-15', [0, 0,'(берётся из основных характеристик)' ]]],
        },
        // 10
        {
          id: 'heat_los_heatcond_roof',
          title:'Характеристика класса энергетической эффективности', 
          input:[['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '(берётся из основных характеристик)']], ['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']]],
          r_btn:null, 
          select:[['Класс энергетической эффективности кровли',['A++ (очень высокий)','A+ (очень высокий)','A (очень высокий)','B+ (высокий)','B (высокий)','C+ (нормальный)','C (нормальный)','C- (нормальный)','D (пониженный)','E (низкий)']]],
          c_box:null,
          date:null,
        },
        // 11
        {
          id: 'heat_los_floor', 
          title:'Тепловые потери через пол', 
          input:[['Высота подвала','м',  '', 'uint', false],['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '(берётся из основных характеристик)']], ['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']], ['Длина стен на одном этаже','м', '', 'uint', false, [0, 4, '(берётся из основной характеристики)']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 12
        {
          id: 'heat_los_vent', 
          title:'Тепловые потери от вентиляции', 
          input:[['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '(берётся из основных характеристик)']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '(берётся из основных характеристик)']], ['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']], ['Высота стен','м', '', 'uint', false, [0, 5, '(берётся из основной характеристики)']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 13
        {
          id: 'add_heatcosts', 
          title:'Характеристика интерьера и перегородок', 
          input:[['Число дверей','ед.',  '', 'uint', false],['Число шкафов','ед.',  '', 'uint', false],['Число диванов','ед.',  '', 'uint', false],['Число столов','ед.',  '', 'uint', false],['Число навесных шкафчиков','ед.',  '', 'uint', false], ['Этажность','', '', 'uint', false, [0, 1, '(берётся из основных характеристик)']],['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']],['Длина стен на одном этаже','м', '', 'uint', false, [0, 4, '(берётся из основных характеристик)']],['Высота стен','м', '', 'uint', false, [0, 5, '(берётся из основных характеристик)']]],
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
          input:[['Число посетителей/жильцов мужчин','чел.', '', 'uint', false],['Число посетителей/жильцов женщин','чел.', '', 'uint', false],['Среднее время пребывания посетителей/жильцов в сутки','чел./сутки', '', 'uint', false], ['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '(берётся из основных характеристик)']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 17
        {
          id: 'heat_gains_washstands', 
          title:'Определение затрат тепловой энергии на ГВС для рукомойников', 
          input:[['Число посетителей/жильцов мужчин', 'чел.', '', 'uint', false, [16, 0, '(берётся из теплопритоков от людей)']],['Число посетителей/жильцов женщин','чел.', '', 'uint', false, [16, 1, '(берётся из теплопритоков от людей)']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 18
        {
          id: 'heat_gains_showers', 
          title:'Определение затрат тепловой энергии на ГВС для душевых', 
          input:[['Число посетителей/жильцов мужчин', 'чел.', '', 'uint', false, [16, 0, '(берётся из теплопритоков от людей)']],['Число посетителей/жильцов женщин','чел.', '', 'uint', false, [16, 1, '(берётся из теплопритоков от людей)']]],
          r_btn:null, 
          select:null,
          c_box:null,
          date:null
        },
        // 19
        {
          id: 'heat_gains_electriclighting', 
          title:'Определение теплопритока от систем электроосвещения и силового электроснабжения', 
          input:[['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']], ['Этажность', '', '', 'uint', false, [0, 1, '(берётся из основных характеристик)']], ['Объём потребления электрической энергии зданием за отопительный период','кВт · ч / отоп. период', '', 'uint', false, null, this.condition_render_elec_consumption_by_period]],
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
          input:[['Температура внутреннего воздуха','°C',  '', 'uint', false, [0, 6, '(берётся из основных характеристик)']], ['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']], ['Этажность', '', '', 'uint', false, [0, 1, '(берётся из основных характеристик)']], ['Высота стен','м', '', 'uint', false, [0, 5, '(берётся из основной характеристики)']], ['Число подъёмов ГВС','ед.', '', 'uint', false, [3, 0, '(берётся из надёжности)']],['Число опусков ГВС','ед.', '', 'uint', false, [3, 1, '(берётся из надёжности)']]],
          r_btn:null, 
          select:[['Тип трубы',[], [], '', [22,1, '(берётся из надёжности)']]],
          c_box:null,
          date:null,
        },
        // 21
        {
          id: 'heat_gains_pipelines', 
          title:'Определение теплопритока от неизолированных трубопроводов отопления', 
          input:[['Температура внутреннего воздуха','°C', '', 'uint', false, [0, 6, '(берётся из основных характеристик)']], ['Длина здания','м', '', 'uint', false, [0, 2, '(берётся из основных характеристик)']],['Ширина здания','м', '', 'uint', false, [0, 3, '(берётся из основных характеристик)']], ['Этажность', '', '', 'uint', false, [0, 1, '(берётся из основных характеристик)']], ['Высота стен','м', '', 'uint', false, [0, 5, '(берётся из основной характеристики)']], ['Число подъёмов от ТП до чердака','ед.', '', 'uint', false, [4, 0, '(берётся из надёжности)']],['Число опусков от чердака до ТП','ед.', '', 'uint', false, [4, 1, '(берётся из надёжности)']]],
          r_btn:null, 
          select:[['Тип трубы',[], [], '', [22,1, '(берётся из надёжности)']]],
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
        },
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
      this.topics.forEach(function(item){
        if(item.name === name){
          item.check_loadpat = !item.check_loadpat;
        }
      })
      return name;
    },
    Change_check_savepat(name){
      this.topics.forEach(function(item){
        if(item.name === name){
          item.check_savepat = !item.check_savepat;
        }
      })
      return name;
    },
    cacl_result(id){
        let self = this
      this.results.forEach(function(item){
        if(item.id == id){
            item.val = func.calc(id, self)
            return false
        }
      })
      return id
    },
	calc_all_server(){
		let self = this
		this.topics.forEach(function(item){
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
                // console.log(this.functions[func_ind].radio_elem[0])
                // console.log(new_val)
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
input[type="date"]{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.25%;
  width: 20%;
}
input[type="checkbox"]{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  transform:scale(1.2);
}
select{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.25%;
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
.header{
  position: fixed;
  display: flex;
  flex-direction: row;
  margin: auto;
  width: 100%;
  height: 50px;
  background: #26495c;
  
  color: #e5e5dc;
}
.header_title{
  font-size: 36px;
}
.cb_transparent{
  opacity: 0;
}
.header_registration{
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  height: 100%;
}
.reg_label{
  display: flex;
  align-items: center;
  user-select: none; 
  height: 100%;
}
.header_menu{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50px;
}
.strip{
  width: 35px;
  height: 6px;
  background-color: #e5e5dc;
  margin-top: 4px;
  margin-bottom: 4px;
}
.header_text{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 10px;
  padding-right: 10px;
  width: 100%;
}
.main{
  margin-top: 50px;
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: row;
}
.function{
  position: fixed;
  background: #e28a16;
  top: 50px;
  bottom: 0px;
  width: 20%;
  overflow-y: scroll;
  min-width: 170px;
}
.solution{ 
  display: flex;
  flex-direction: column;
  width: 100%;
}
.treecb1{
  display: flex;
  flex-direction: row;
  align-items: center;
  margin: 1%;
  color: #e5e5dc;
  font-size: 16px;
}
.treecb2{
  display: flex;
  flex-direction: row;
  align-items: center;
  min-height: 35px;
  margin: 2%;
  color: #0b161d;
  border-bottom: 2px dotted rgb(0, 0, 0);
  user-select: none;
}
.treecb2:hover{
  background-color: #e0886563;
  cursor: pointer;
  transition: background-color 300 ms;
}
.topics{
  display: flex; 
  flex-direction: column;
  margin: 1%;
}
.mega_block_borders{
  display: flex; 
  flex-direction: column;
  justify-content: right;
  background-color: #e5e5dc; 
  border: 2px solid #e28a16;
  border-radius: 10px; 
  box-shadow: 0 0 10px #cf7b0c;
  margin: 1% 1% 0%;
}
.mega_block_title{
  font-size: 20px;
}
.btn_div{
  display: flex;
  align-items: center;
  justify-content: right;
  margin: 1%;
}
.btn_div_global{
  display: flex;
  align-items: start;
  justify-content: space-between;
  margin: 2%;
}
.btn_patterns{
  display: flex;
  align-items: start;
  justify-content: space-between;
  width: 69%;
}
.show_pat{
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;

  background: #e5e5dc;
  border: 2px solid #e28a16;
  border-radius: 4px; 
  padding: 2%;
  margin: 1%;
}
.content{
  display: flex;
  flex-direction: column;
  margin: 1%;
}
.inp_pat{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.25%;
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
.btn_savepat{
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 48%; 
}
.btn_loadpat{
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
.btn_calc{
  display: flex;
  justify-content: center;
  width: 29%; 
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
  width: 29%; 
  background-color: #26495c; 
  border: 2px solid #234455;
  border-radius: 10px; 
  box-shadow: 0 0 5px #1e3a49 inset;
  color: #e5e5dc;
}
.mega_block{
  display: flex;
  flex-direction: row;
}
.main_block{
  margin: 1% 1% 0%;
}
.res_block{
  width: 29%;
  margin: 1% 1% 0%;
}
.block{
  background-color: #e5e5dc; 
  border: 2px solid #e28a16;
  border-radius: 10px; 
  box-shadow: 0 0 10px #cf7b0c;
  width: 100%;
  margin-bottom: 1%;
  padding: 20px 40px;
}
.block_title{
  font-size: 16px;
  color:#1e3a49;
}
.block_inp{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.25%;
  width: 25%;
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
</style>
