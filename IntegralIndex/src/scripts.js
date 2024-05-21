import func from '@/connect/funcs'
  import login_funcs from '@/connect/login'
  export default{
    data(){
      return {
        url_to_download_math : "",
        login_reg_check:[false,false],
        menu_check: '0',
        settings_check: '0',
        set_all_flag: false,
        choise_NM: false,
        build_changes: new Set(),
        savepat: {
          radio: {
            picked: 'Сохранять только из выбранных расчётов'
          }
        },
        loadpat_error: {show: false, text: ''},
        
        big_sections_name:
        [
          {name: 'Теплопотери'},
          {name: 'Теплопритоки'}
        ],
        time : 2019,
        reliability_section: {
          check: false,
          title: 'Надежность'
        },
        sections:
        [    
          { section:'Теплопотери',     
            name: 'heat_los_win',                 
            title: 'Расчет тепловых потерь через окна', 
            subtitle: 'Характеристика окон',
            check: false,
            title_fields: ['Число окон',    'Длина типового окна', 'Высота типового окна', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип окон',     'Дата установки окон', 'Дата постройки'],
            value_fields: ['count_windows', 'length_windows',      'height_windows',       'temp_inside',                     'temp_outside',                  'type_windows', 'date_windows',        'date_construction'],
            ue_fields:    ['ед.', 'м', 'м', '°С', '°С','', '', '']
          },
          {  section:'Теплопотери',     
             name: 'inf_win',                      
             title: 'Расчет инфильтрации через окна',
             subtitle: 'Характеристика окон', 
             check: false,
             title_fields:  ['Число окон',    'Длина типового окна', 'Высота типового окна', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип окон',     'Дата установки окон', 'Дата постройки'],
             value_fields: ['count_windows', 'length_windows',      'height_windows',       'temp_inside',                     'temp_outside',                  'type_windows', 'date_windows',        'date_construction'],
             ue_fields:    ['ед.', 'м', 'м', '°С', '°С','', '', '']
          },
          {  section:'Теплопотери',     
             name: 'heat_los_inpgr',               
             title: 'Расчет тепловых потерь через входную группу',
             subtitle: 'Характеристика входной группы',
             check: false,
             title_fields: ['Число дверей', 'Длина типовой входной двери', 'Высота типовой входной двери', 'Этажность', 'Высота стен', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип двери', 'Дата установки дверей', 'Дата постройки'],
             value_fields: ['count_doors', 'length_doors', 'height_doors', 'floors', 'height_wall', 'temp_inside', 'temp_outside', 'type_doors', 'date_doors', 'date_construction'],
             ue_fields:    ['ед.', 'м', 'м', 'ед.', 'м', '°С', '°С', '', '', '']
            },
          {  section:'Теплопотери',     
             name: 'inf_inpgr',                    
             title: 'Расчет инфильтрации через входную группу', 
             subtitle: 'Характеристика входной группы',
             check: false,
             title_fields: ['Число дверей', 'Длина типовой входной двери', 'Высота типовой входной двери', 'Этажность', 'Высота стен', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип двери', 'Дата установки дверей', 'Дата постройки'],
             value_fields: ['count_doors', 'length_doors', 'height_doors', 'floors', 'height_wall', 'temp_inside', 'temp_outside', 'type_doors', 'date_doors', 'date_construction'],
             ue_fields:    ['ед.', 'м', 'м', 'ед.', 'м', '°С', '°С', '', '', '']
          },
          {  section:'Теплопотери',     
             name: 'heat_los_heatcond_benv',       
             title: 'Определение теплопотерь посредством теплопроводности через ограждающие конструкции', 
             subtitle: 'Характеристика класса энергетической эффективности',
             check: false,
             title_fields: ['Длина здания', 'Ширина здания', 'Этажность', 'Высота стен', 'Число окон', 'Длина типового окна', 'Высота типового окна', 'Число дверей', 'Длина типовой входной двери', 'Высота типовой входной двери', 'Класс энергетической эффективности ограждающих конструкций', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Дата постройки'],
             value_fields: ['length_build', 'width_build', 'floors', 'height_wall', 'count_windows', 'length_windows', 'height_windows', 'count_doors', 'length_doors', 'height_doors', 'class_energoeff', 'temp_inside', 'temp_outside', 'date_construction'],
             ue_fields:    ['м', 'м', 'ед.', 'м',  'ед.', 'м', 'м', 'ед.', 'м', 'м', '', '°С', '°С', '']
          },
          {  section:'Теплопотери',     
             name: 'heat_los_heatcond_roof',       
             title: 'Определение теплопотерь посредством теплопроводности через кровлю', 
             subtitle: 'Характеристика класса энергетической эффективности',
             check: false,
             title_fields: ['Температура внутреннего воздуха', 'Температура наружного воздуха', 'Длина здания', 'Ширина здания', 'Класс энергетической эффективности ограждающих конструкций'],
             value_fields: ['temp_inside', 'temp_outside', 'length_build', 'width_build', 'class_energoeff'],
             ue_fields:    ['°С', '°С', 'м', 'м', '']
         },
         {  section:'Теплопотери',     
            name: 'heat_los_floor',               
            title: 'Расчет теплопотерь через пол', 
            subtitle: 'Тепловые потери через пол',
            check: false,
            title_fields: ['Длина здания', 'Ширина здания', 'Длина стен на одном этаже', 'Высота подвала', 'Температура внутреннего воздуха', 'Температура наружного воздуха'],
            value_fields: ['length_build', 'width_build', 'length_wall', 'height_basement', 'temp_inside', 'temp_outside'],
            ue_fields:    ['м', 'м', 'м', 'м','°С', '°С']
         },
         {  section:'Теплопотери',     
            name: 'heat_los_vent',                
            title: 'Расчет теплопотерь, связанных с вентиляцией', 
            subtitle: 'Тепловые потери связанные с вентиляцией',
            check: false,
            title_fields: ['Длина здания', 'Ширина здания', 'Высота стен на одном этаже', 'Температура внутреннего воздуха', 'Температура наружного воздуха'],
            value_fields: ['length_build', 'width_build', 'height_wall',  'temp_inside', 'temp_outside'],
            ue_fields:    ['м', 'м', 'м','°С', '°С']
         },
         {  section:'Теплопотери',     
            name: 'add_heatcosts',                
            title: 'Дополнительные затраты теплоты на повторный прогрев внутренних перегородок и интерьеров',
            subtitle: 'Характеристика интерьера и внутренних перегородок',
            check: false,
            title_fields: ['Число дверей', 'Число шкафов', 'Число диванов', 'Число столов', 'Число навесных шкафчиков', 'Этажность', 'Длина здания', 'Ширина здания','Длина стен на одном этаже' ,'Высота стен на одном этаже'],
            value_fields: ['count_doors', 'count_closet', 'count_sofa', 'count_table', 'count_small_closet', 'floors', 'length_build', 'width_build', 'length_wall', 'height_wall'],
            ue_fields:    ['ед.', 'ед.', 'ед.', 'ед.', 'ед.', 'ед.', 'м', 'м', 'м', 'м']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_people',            
             title: 'Определение теплопритоков от людей', 
             subtitle: 'Теплопритоки от людей',
             check: false,
             title_fields: ['Число посетителей/жильцов мужчин', 'Число посетителей/жильцов женщин','Число посетителей/жильцов детей', 'Среднее время пребывания посетителей/жильцов в сутки', 'Температура внутреннего воздуха'],
             value_fields: ['count_men', 'count_women', 'count_children', 'time_guests', 'temp_inside'],
             ue_fields: ['чел', 'чел', 'чел', 'чел/сутки', '°С']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_washstands',        
             title: 'Определение затрат тепловой энергии на ГВС для рукомойников', 
             check: false,
             title_fields: ['Число посетителей/жильцов мужчин', 'Число посетителей/жильцов женщин','Число посетителей/жильцов детей'],
             value_fields: ['count_men', 'count_women', 'count_children'],
             ue_fields:    ['чел', 'чел', 'чел']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_showers',           
             title: 'Определение затрат тепловой энергии на ГВС для душевых', 
             check: false,
             title_fields: ['Число посетителей/жильцов мужчин', 'Число посетителей/жильцов женщин','Число посетителей/жильцов детей'],
             value_fields: ['count_men', 'count_women', 'count_children'],
             ue_fields:    ['чел', 'чел', 'чел']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_electriclighting',  
             title: 'Определение теплопритока от систем электроосвещения и силового электроснабжения', 
             check: false,
             title_fields: ['Длина здания', 'Ширина здания','Этажность'],
             value_fields: ['length_build', 'width_build', 'floors'],
             ue_fields:    ['м', 'м', 'ед.']
          },
          {  section:'Теплопритоки',  //тип трубы?? труба металлопластиковая  
             name: 'heat_gains_GVS',               
             title: 'Определение теплопритока от неизолированных трубопроводов ГВС', 
             check: false,
             title_fields: ['Длина здания', 'Ширина здания','Этажность', 'Высота стен на одном этаже', 'Число помещений с раковинами на этаже', 'Температура внутреннего воздуха'],
             value_fields: ['length_build', 'width_build', 'floors', 'height_wall', 'count_sink',  'temp_inside'],
             ue_fields:    ['м', 'м', 'ед.', 'м', 'ед.', '°С']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_pipelines',   //тип трубы?? труба металлопластиковая        
             title: 'Определение теплопритока от неизолированных трубопроводов отопления', 
             check: false,
             title_fields: ['Длина здания', 'Ширина здания','Этажность', 'Высота стен на одном этаже', 'Количество окон', 'Температура внутреннего воздуха'],
             value_fields: ['length_build', 'width_build', 'floors', 'height_wall', 'count_windows',  'temp_inside'],
             ue_fields:    ['м', 'м', 'ед.', 'м', 'ед.', '°С']
          },
        ],

        results: {
          reliability:                  '',
          heat_los_win:                 '', 
          inf_win:                      '', 
          heat_los_inpgr:               '', 
          inf_inpgr:                    '', 
          heat_los_heatcond_benv:       '', 
          heat_los_heatcond_roof:       '', 
          heat_los_floor:               '', 
          heat_los_vent:                '', 
          add_heatcosts:                '', 
          heat_gains_people:            '', 
          heat_gains_washstands:        '', 
          heat_gains_showers:           '', 
          heat_gains_electriclighting:  '', 
          heat_gains_GVS:               '', 
          heat_gains_pipelines:         '', 
          tec:                          '', 
          ctp:                          '',
          ins1:                         ''
        },
        dop_results:{
          sum_los:             '', 
          sum_add:             '', 
          razn_los_add:        '', 
          razn_tec_ctp:        '', 
          eclg_sp_tut:         '', 
          eclg_sp_co2:         '', 
          eclg_tec_ctp_tut:    '', 
          eclg_tec_ctp_co2:    '', 
        },
        parametrs_of_reliability:{
          id_build:             '',
          elev_itp:             '',
          ventsys:              '',
          count_installations:  '',
          length_pipe1:         '',
          length_pipe2:         '',
          count_up_hws:         '',
          count_down_hws:       '',
          count_crane:          '',
          count_up_loft:        '',
          count_down_loft:      '',
          count_radiator:       '',
          type_armature:        '',
          type_radiator:        '',
          type_crane:           '',
          type_pipe:            '',
          type_pump:            '',
          type_heatexchanger:   ''  
        },
        parametrs_of_build:{
          id_build:             '',
          name_build:           '',
          floors:               '',
          length_build:         '',
          width_build:          '',
          length_wall:          '',
          height_wall:          '',
          temp_inside:          '',
          temp_outside:         '',
          date_construction:    '',
          count_windows:        '',
          length_windows:       '',
          height_windows:       '',
          date_windows:         '',
          type_windows:         '',
          count_doors:          '',
          length_doors:         '',
          height_doors:         '',
          type_doors:           '',
          date_doors:           '',
          class_energoeff:      '',
          count_closet:         '',
          count_sofa:           '',
          count_table:          '',
          count_small_closet:   '',
          count_men:            '',
          count_women:          '',
          count_children:       '',
          time_guests:          '',
          count_sink:           '',
          height_basement:      '',
          period_energosave:    '',     
          walls_material:       '', 
          floors_material:      '', 
          doors_material:       '', 
          furniture_material:   '', 
          sofa_material:        '', 
          table_material:       '', 
          type_pipe:            ''
      },
      name_build:[
        {id: 1,  val: 'Тестовая схема здания'},
        {id: 2,  val: 'Коттедж ИЖС на одну семью'},
        {id: 3,  val: 'МКД "хрущёвка" 5 этажей, 3 подьезда,1980г.'},
        {id: 4,  val: 'МКД монолит 128 , 16 этажей, 2 подъезда, 2012'},
        {id: 5,  val: 'Офисный центр, 13 этажей, 2020г'},
        {id: 6,  val: 'МКД панельная, 9 этажей, 3 подъезда, 2012г.'},
        {id: 7,  val: 'Школа тип Самолёт, 1980г.'},
        {id: 8,  val: 'Школа тип Самолёт, 2020г.'} 
      ],

      type_windows:[
        {id: 1, val: 'Деревянные окна с двойным остеклением'},
        {id: 2, val: 'Стеклопакет 24мм (4-16-4) в корпусе ПВХ'},
        {id: 3, val: 'Стеклопакет 24мм (4-16-4) в корпусе ПВХ, низкоэмиссионное покрытие'},
        {id: 4, val: 'Стеклопакет 36мм (4-10-4-14-4) в корпусе ПВХ'},
        {id: 5, val: 'Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ'},
        {id: 6, val: 'Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ, низкоэмиссионное покрытие'},
      ],
      
      type_doors:[
        {id: 1,  val: 'Двери одинарные деревянные без тамбура'},
        {id: 2,  val: 'Двери одинарные деревянные с тамбуром между ними'},
        {id: 3,  val: 'Двери двойные (распашные) деревянные без тамбура'},
        {id: 4,  val: 'Двери двойные (распашные) деревянные с тамбуром между ними'},
        {id: 5,  val: 'Двери одинарные ПВХ без тамбура'},
        {id: 6,  val: 'Двери одинарные ПВХ с тамбуром между ними'},
        {id: 7,  val: 'Двери двойные (распашные) ПВХ без тамбура'},
        {id: 8,  val: 'Двери двойные (распашные) ПВХ с тамбуром между ними'},
        {id: 9,  val: 'Двери одинарные алюминиевые без тамбура'},
        {id: 10, val: 'Двери одинарные алюминиевые с тамбуром между ними'},
        {id: 11, val: 'Двери двойные (распашные) алюминиевые без тамбура'},
        {id: 12, val: 'Двери двойные (распашные) алюминиевые с тамбуром между ними'}
      ],
      
      class_energoeff:[
        {id: 1,   val: 'A++ (очень высокий, R = 8.8 м² °С/В)'},
        {id: 2,   val: 'A+  (очень высокий, R = 7.5 м² °С/В)'},
        {id: 3,   val: 'A   (очень высокий, R = 6.5 м² °С/В)'},
        {id: 4,   val: 'B+  (высокий, R = 5.5 м² °С/В)'},
        {id: 5,   val: 'В   (высокий, R = 4.5 м² °С/В)'},
        {id: 6,   val: 'C+  (нормальный, R = 3.8 м² °С/В)'},
        {id: 7,   val: 'С   (нормальный, R = 3.5 м² °С/В)'},
        {id: 8,   val: 'С-  (нормальный, R = 3.2 м² °С/В)'},
        {id: 9,   val: 'D   (пониженный, R = 2.8 м² °С/В)'},
        {id: 10,  val: 'E   (низкий, R = 2.5 м² °С/В)'}    
      ],

      period_energosave:[
        {id: 1, val: 'Еженочно в рабочие дни и все выходные дни'},
        {id: 2, val: 'Еженочно каждый календарный день'},
        {id: 3, val: 'Раз в неделю (режим загородного дома)'},
        {id: 4, val: 'Без понижения температуры'}
      ],
      type_pipe:[
        {id: 1, val: 'Труба металлическая'},
        {id: 2, val: 'Труба металлопластиковая'},
        {id: 3, val: 'Труба пластиковая'},
        {id: 4, val: 'Труба металлическая с утеплителем'},
        {id: 5, val: 'Труба металлопластиковая с утеплителем'},
        {id: 6, val: 'Труба пластиковая с утеплителем'}
      ],
      type_armature:[
        {id: 1, val: 'Запорный вентиль шаровый'},
        {id: 2, val: 'Запорный вентиль винтовой'}
      ], 

      type_radiator:[
        {id: 1, val: 'Радиатор чугунный'},
        {id: 2, val: 'Радиатор биметаллический'}
      ], 
      type_crane:[
        {id: 1, val: 'Кран типа "ёлочка"'},
        {id: 2, val: 'Кран шаровый с аэратором'},
        {id: 3, val: 'Кран сенсорный с аэратором'}
      ],
      type_pump:[
        {id: 1, val: 'Насос 1'},
        {id: 2, val: 'Насос ЧРП'}
      ],
      type_heatexchanger:[
        {id: 1, val: 'Теплообменник "труба в трубе"'},
        {id: 2, val: 'Теплообменник пластинчатый'}
      ],

      materials:[
        {id: 1,   val: 'Кирпич'},
        {id: 2,   val: 'Газобетон'},
        {id: 3,   val: 'Пенобетон'},
        {id: 4,   val: 'Железобетон'},  
        {id: 5,   val: 'Сосна'},
        {id: 6,   val: 'Пенополистерол'},
        {id: 7,   val: 'Керамзитобетон'},
        {id: 8,   val: 'Ротбанд'},  
        {id: 9,   val: 'Штукатурка'},
        {id: 10,  val: 'Воздух при 20 °С'},
        {id: 11,  val: 'ДСП, ОСП'},
        {id: 12,  val: 'Плитка'},  
        {id: 13,  val: 'Дуб'},
        {id: 14,  val: 'Клён'},
        {id: 15,  val: 'Липа'},
        {id: 16,  val: 'Пихта'},  
        {id: 17,  val: 'Линолеум'},
        {id: 18,  val: 'Клей'},
        {id: 19,  val: 'Фанера'},
        {id: 20,  val: 'Паркет'}, 
        {id: 666, val: 'Неизвестный материал'}, 
      ],

      }
    },

    methods:{
    calc_reliability(){
        let self = this
        let calc_rel = func.calc_reliability(self, self.parametrs_of_reliability)
        this.results['reliability'] = calc_rel[0]
    },
    numberWithSpaces(x) {
      var parts = x.toString().split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
      return parts.join(".");
    },
    printVal(val, ue){
      var res = this.numberWithSpaces(parseFloat(val).toFixed(3));
        return res + ' ' +  ue;
    },

    calc_dop_results(){
        this.dop_results.sum_los      = parseFloat(this.results.heat_los_win)  + parseFloat(this.results.inf_win)  + parseFloat(this.results.heat_los_inpgr)  + parseFloat(this.results.inf_inpgr)  + parseFloat(this.results.heat_los_heatcond_benv)  + parseFloat(this.results.heat_los_heatcond_roof) + parseFloat(this.results.heat_los_floor) + parseFloat(this.results.heat_los_vent) + parseFloat(this.results.add_heatcosts);
        this.dop_results.sum_add      = parseFloat(this.results.heat_gains_people) + parseFloat(this.results.heat_gains_washstands) + parseFloat(this.results.heat_gains_showers) + parseFloat(this.results.heat_gains_electriclighting) + parseFloat(this.results.heat_gains_GVS) + parseFloat(this.results.heat_gains_pipelines);
        this.dop_results.razn_los_add = this.dop_results.sum_los - this.dop_results.sum_add
        this.dop_results.eclg_sp_tut  = this.dop_results.razn_los_add * 0.1486
        this.dop_results.eclg_sp_co2  = this.dop_results.razn_los_add * 276.28 
        this.dop_results.razn_tec_ctp = parseFloat(this.results.tec) - parseFloat(this.results.ctp)
        this.dop_results.eclg_tec_ctp_tut = this.dop_results.razn_tec_ctp * 0.1486
        this.dop_results.eclg_tec_ctp_co2 = this.dop_results.razn_tec_ctp * 276.28
        
        for (var key in this.dop_results)
        {
          if (isNaN(this.dop_results[key]))
            this.dop_results[key] = ''
        }
    },
      logout(){
        localStorage.setItem("token", null)
        login_funcs.logout()
        window.location.href = "/"
      },

      async save_current_calc(){
        func.save_cur(this.parametrs_of_build, this.results, this.dop_results)
      },

      left_panel_show(){
        let elem = document.getElementById('neuro_calc_id')
        if (getComputedStyle(elem).fontSize == '18px')
          elem.style = 'font-size: 16px'
        else
           elem.style = 'font-size: 18px'
      },
      set_all_check_left_panel(flag){
          this.sections.forEach(function(item){
            item.check = flag 
          })
          this.reliability_section.check = flag
      }         
       ,
       set_all_checkbox(){  
          this.set_all_flag = !this.set_all_flag;  
          this.set_all_check_left_panel(this.set_all_flag); 
       } ,
      
       calc_all(){
        let self = this
        let year = document.getElementById('years-selector');
        setTimeout(func.calc, 10, "formula_calc", self, year.value)
      },

      calc_INS(){
        this.results.ins1 = 5;
      },
      calc_tec(){
        let self = this
        let year = document.getElementById('years-selector');
        setTimeout(func.calc, 100, "tec", self, year.value)
      },
      calc_ctp(){
        let self = this
        let year = document.getElementById('years-selector');
        setTimeout(func.calc, 100, "ctp", self, year.value)
      },
    download_excel(){
      let downl_res = func.download_excel()
      console.log(downl_res)        
    },

    printInfoVal(val){
      let select_list = ['type_windows', 'type_doors', 'class_energoeff','period_energosave', 'walls_material', 'floors_material','doors_material', 'furniture_material', 'sofa_material', 'table_material', 'type_pipe', 'type_armature', 'type_radiator', 'type_crane']
      let reliability_list = ['count_installations', 'length_pipe1', 'length_pipe2', 'count_up_hws', 'count_down_hws', 'count_crane', 'count_up_loft', 'count_down_loft', 'count_radiator']
      if (select_list.indexOf(val) != -1)
        return this.selected_item(val)                      
      else 
        if (reliability_list.indexOf(val) != -1)
            return this.parametrs_of_reliability[val]
        else 
            return this.parametrs_of_build[val]                     
    },

    selected_item(name){
      let param = this.parametrs_of_build[name] 
      if (param == undefined)
        param = this.parametrs_of_reliability[name]
      if (param !== '')
      switch (name) {
        case 'type_windows':
          return this.type_windows[param-1].val
        case 'type_doors':
          return this.type_doors[param-1].val
        case 'class_energoeff':
          return this.class_energoeff[param-1].val
        case 'period_energosave':
          return this.period_energosave[param-1].val
        case 'walls_material' || 'floors_material' || 'doors_material' || 'furniture_material' || 'sofa_material' || 'table_material':
          return this.materials[param-1].val
        case 'type_pipe':
          return this.type_pipe[param-1].val
        case 'type_armature':
          return this.type_armature[param-1].val
        case 'type_radiator':
          return this.type_radiator[param-1].val
        case 'type_crane':
          return this.type_crane[param-1].val
        default:
          break;
      }
                  
    },

    //это тоже удалить потом
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

    
    import_from_server(){
      func.import(this)
      this.clear_results();
    },
    clear_results(){
      for (var key in this.results)
        this.results[key] = ''

      for (var key1 in this.dop_results)
        this.dop_results[key1] = ''
    }
    },
    computed:{
      type_windows_selected(){
        if (this.parametrs_of_build.type_windows !== '')
            return this.type_windows[this.parametrs_of_build.type_windows-1].val      
      },
      type_doors_selected(){
        if (this.parametrs_of_build.type_doors !== '')
            return this.type_doors[this.parametrs_of_build.type_doors-1].val 
      },
      class_energoeff_selected(){
        if (this.parametrs_of_build.class_energoeff !== '')
            return this.class_energoeff[this.parametrs_of_build.class_energoeff-1].val   
      },
      show_dop_info_title(){
        return this.reliability_section.check || this.sections.find((item) => item.check)
      }
    },
    mounted() {
        // Проверить валидность токена
        let user_token = {"token": localStorage.getItem("token")}
        let res = func.check_token_before_render(user_token)
        if (res){
          // Закрываем окно входа
          this.login_reg_check[0] = false
          func.start(this)
          func.load(this)     
        } else {
          // Переходим на страницу входа
          this.login_reg_check[0] = true
        }  
    },
  }