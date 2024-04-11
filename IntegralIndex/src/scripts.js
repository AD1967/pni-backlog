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
        time : 2019,
        sections:
        [
          {  section:'хар-ка здания',  name: 'general',  title: 'Общая характеристика здания', check: 'false'}, //удалить потом
          
          // {  section:'Надежность' ,     name: 'reliability',                  title: 'Надежность', check: 'false'},
          { section:'Теплопотери',     
            name: 'heat_los_win',                 
            title: 'Расчет тепловых потерь через окна', 
            subtitle: 'Характеристика окон',
            check: 'false',
            title_fields: ['Число окон',    'Длина типового окна', 'Высота типового окна', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип окон',     'Дата установки окон', 'Дата постройки'],
            value_fields: ['count_windows', 'length_windows',      'height_windows',       'temp_inside',                     'temp_outside',                  'type_windows', 'date_windows',        'date_construction'],
            ue_fields:    ['ед.', 'м', 'м', '°С', '°С','ед.', 'ед.', 'ед.']
          },
          {  section:'Теплопотери',     
             name: 'inf_win',                      
             title: 'Расчет инфильтрации через окна',
             subtitle: 'Характеристика окон', 
             check: 'false',
             title_fields:  ['Число окон',    'Длина типового окна', 'Высота типового окна', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип окон',     'Дата установки окон', 'Дата постройки'],
             value_fields: ['count_windows', 'length_windows',      'height_windows',       'temp_inside',                     'temp_outside',                  'type_windows', 'date_windows',        'date_construction'],
             ue_fields:    ['ед.', 'м', 'м', '°С', '°С','ед.', 'ед.', 'ед.']
          },
          {  section:'Теплопотери',     
             name: 'heat_los_inpgr',               
             title: 'Расчет тепловых потерь через входную группу',
             subtitle: 'Характеристика входной группы',
             check: 'false',
             title_fields: ['Число дверей', 'Длина типовой входной двери', 'Высота типовой входной двери', 'Этажность', 'Высота стен', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип двери', 'Дата установки дверей', 'Дата постройки'],
             value_fields: ['count_doors', 'length_doors', 'height_doors', 'floors', 'height_wall', 'temp_inside', 'temp_outside', 'type_doors', 'date_doors', 'date_construction'],
             ue_fields:    ['ед.', 'м', 'м', 'ед.', 'м', '°С', '°С', 'ед.', 'ед.', 'ед.']
            },
          {  section:'Теплопотери',     
             name: 'inf_inpgr',                    
             title: 'Расчет инфильтрации через входную группу', 
             subtitle: 'Характеристика входной группы',
             check: 'false',
             title_fields: ['Число дверей', 'Длина типовой входной двери', 'Высота типовой входной двери', 'Этажность', 'Высота стен', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Тип двери', 'Дата установки дверей', 'Дата постройки'],
             value_fields: ['count_doors', 'length_doors', 'height_doors', 'floors', 'height_wall', 'temp_inside', 'temp_outside', 'type_doors', 'date_doors', 'date_construction'],
             ue_fields:    ['ед.', 'м', 'м', 'ед.', 'м', '°С', '°С', 'ед.', 'ед.', 'ед.']
          },
          {  section:'Теплопотери',     
             name: 'heat_los_heatcond_benv',       
             title: 'Определение теплопотерь посредством теплопроводности через ограждающие конструкции', 
             subtitle: 'Характеристика класса энергетической эффективности',
             check: 'false',
             title_fields: ['Длина здания', 'Ширина здания', 'Этажность', 'Высота стен', 'Число окон', 'Длина типового окна', 'Высота типового окна', 'Число дверей', 'Длина типовой входной двери', 'Высота типовой входной двери', 'Класс энергетической эффективности ограждающих конструкций', 'Температура внутреннего воздуха', 'Температура наружного воздуха', 'Дата постройки'],
             value_fields: ['length_build', 'width_build', 'floors', 'height_wall', 'count_windows', 'length_windows', 'height_windows', 'count_doors', 'length_doors', 'height_doors', 'class_energoeff', 'temp_inside', 'temp_outside', 'date_construction'],
             ue_fields:    ['м', 'м', 'ед.', 'м',  'ед.', 'м', 'м', 'ед.', 'м', 'м', 'ед.', '°С', '°С', 'ед.']
          },
          {  section:'Теплопотери',     
             name: 'heat_los_heatcond_roof',       
             title: 'Определение теплопотерь посредством теплопроводности через кровлю', 
             subtitle: 'Характеристика класса энергетической эффективности',
             check: 'false',
             title_fields: ['Температура внутреннего воздуха', 'Температура наружного воздуха', 'Длина здания', 'Ширина здания', 'Класс энергетической эффективности ограждающих конструкций'],
             value_fields: ['temp_inside', 'temp_outside', 'length_build', 'width_build', 'class_energoeff'],
             ue_fields:    ['°С', '°С', 'м', 'м', 'ед.']
         },
         {  section:'Теплопотери',     
            name: 'heat_los_floor',               
            title: 'Расчет теплопотерь через пол', 
            subtitle: 'Тепловые потери через пол',
            check: 'false',
            title_fields: ['Длина здания', 'Ширина здания', 'Длина стен на одном этаже', 'Высота подвала', 'Температура внутреннего воздуха', 'Температура наружного воздуха'],
            value_fields: ['length_build', 'width_build', 'length_wall', 'height_basement', 'temp_inside', 'temp_outside'],
            ue_fields:    ['м', 'м', 'м', 'м','°С', '°С']
         },
         {  section:'Теплопотери',     
            name: 'heat_los_vent',                
            title: 'Расчет теплопотерь, связанных с вентиляцией', 
            subtitle: 'Тепловые потери связанные с вентиляцией',
            check: 'false',
            title_fields: ['Длина здания', 'Ширина здания', 'Высота стен на одном этаже', 'Температура внутреннего воздуха', 'Температура наружного воздуха'],
            value_fields: ['length_build', 'width_build', 'height_wall',  'temp_inside', 'temp_outside'],
            ue_fields:    ['м', 'м', 'м','°С', '°С']
         },
         {  section:'Теплопотери',     
            name: 'add_heatcosts',                
            title: 'Дополнительные затраты теплоты на повторный прогрев внутренних перегородок и интерьеров',
            subtitle: 'Характеристика интерьера и внутренних перегородок',
            check: 'false',
            title_fields: ['Число дверей', 'Число шкафов', 'Число диванов', 'Число столов', 'Число навесных шкафчиков', 'Этажность', 'Длина здания', 'Ширина здания','Длина стен на одном этаже' ,'Высота стен на одном этаже'],
            value_fields: ['count_doors', 'count_closet', 'count_sofa', 'count_table', 'count_small_closet', 'floors', 'length_build', 'width_build', 'length_wall', 'height_wall'],
            ue_fields:    ['ед.', 'ед.', 'ед.', 'ед.', 'ед.', 'ед.', 'м', 'м', 'м', 'м']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_people',            
             title: 'Определение теплопритоков от людей', 
             subtitle: 'Теплопритоки от людей',
             check: 'false',
             title_fields: ['Число посетителей/жильцов мужчин', 'Число посетителей/жильцов женщин','Число посетителей/жильцов детей', 'Среднее время пребывания посетителей/жильцов в сутки', 'Температура внутреннего воздуха'],
             value_fields: ['count_men', 'count_women', 'count_children', 'time_guests', 'temp_inside'],
             ue_fields: ['чел', 'чел', 'чел', 'чел/сутки', '°С']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_washstands',        
             title: 'Определение затрат тепловой энергии на ГВС для рукомойников', 
             check: 'false',
             title_fields: ['Число посетителей/жильцов мужчин', 'Число посетителей/жильцов женщин','Число посетителей/жильцов детей'],
             value_fields: ['count_men', 'count_women', 'count_children'],
             ue_fields:    ['чел', 'чел', 'чел']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_showers',           
             title: 'Определение затрат тепловой энергии на ГВС для душевых', 
             check: 'false',
             title_fields: ['Число посетителей/жильцов мужчин', 'Число посетителей/жильцов женщин','Число посетителей/жильцов детей'],
             value_fields: ['count_men', 'count_women', 'count_children'],
             ue_fields:    ['чел', 'чел', 'чел']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_electriclighting',  
             title: 'Определение теплопритока от систем электроосвещения и силового электроснабжения', 
             check: 'false',
             title_fields: ['Длина здания', 'Ширина здания','Этажность'],
             value_fields: ['length_build', 'width_build', 'floors'],
             ue_fields:    ['м', 'м', 'ед.']
          },
          {  section:'Теплопритоки',  //тип трубы?? труба металлопластиковая  
             name: 'heat_gains_GVS',               
             title: 'Определение теплопритока от неизолированных трубопроводов ГВС', 
             check: 'false',
             title_fields: ['Длина здания', 'Ширина здания','Этажность', 'Высота стен на одном этаже', 'Число помещений с раковинами на этаже', 'Температура внутреннего воздуха'],
             value_fields: ['length_build', 'width_build', 'floors', 'height_wall', 'count_sink',  'temp_inside'],
             ue_fields:    ['м', 'м', 'ед.', 'м', 'ед.', '°С']
          },
          {  section:'Теплопритоки',    
             name: 'heat_gains_pipelines',   //тип трубы?? труба металлопластиковая        
             title: 'Определение теплопритока от неизолированных трубопроводов отопления', 
             check: 'false',
             title_fields: ['Длина здания', 'Ширина здания','Этажность', 'Высота стен на одном этаже', 'Количество окон', 'Температура внутреннего воздуха'],
             value_fields: ['length_build', 'width_build', 'floors', 'height_wall', 'count_windows',  'temp_inside'],
             ue_fields:    ['м', 'м', 'ед.', 'м', 'ед.', '°С']
          },
        ],

        results: [
          {id: 'general',                     val: ''}, //0
          {id: 'reliability',                 val: ''}, //1
          {id: 'heat_los_win',                val: ''}, //2
          {id: 'inf_win',                     val: ''}, //3
          {id: 'heat_los_inpgr',              val: ''}, //4
          {id: 'inf_inpgr',                   val: ''}, //5
          {id: 'heat_los_heatcond_benv',      val: ''}, //6
          {id: 'heat_los_heatcond_roof',      val: ''}, //7
          {id: 'heat_los_floor',              val: ''}, //8
          {id: 'heat_los_vent',               val: ''}, //9
          {id: 'add_heatcosts',               val: ''}, //10
          {id: 'heat_gains_people',           val: ''}, //11
          {id: 'heat_gains_washstands',       val: ''}, //12
          {id: 'heat_gains_showers',          val: ''}, //13
          {id: 'heat_gains_electriclighting', val: ''}, //14
          {id: 'heat_gains_GVS',              val: ''}, //15
          {id: 'heat_gains_pipelines',        val: ''}, //16
          {id: 'tec',                         val: ''}, //17
          {id: 'cpt',                         val: ''}  //18
        ],
        dop_results:[
          {id: 'sum_pritok',                  val: ''}, //0
          {id: 'sum_poter',                   val: ''}, //1
          {id: 'razn_poter_pritok',           val: ''}, //2
          {id: 'razn_tec_cpt',                val: ''}, //3
          {id: 'eclg_sp_tut',                 val: ''}, //4
          {id: 'eclg_sp_co2',                 val: ''}, //5
          {id: 'eclg_tc_cpt_tut',             val: ''}, //6
          {id: 'eclg_tc_cpt_co2',             val: ''}, //7
        ],

        parametrs_of_build:[
          {floors:              ''},
          {length_build:        ''},
          {width_build:         ''},
          {length_wall:         ''},
          {height_wall:         ''},
          {temp_inside:         ''},
          {temp_outside:        ''},
          {date_construction:   ''},
          {count_windows:       ''},
          {length_windows:      ''},
          {height_windows:      ''},
          {date_windows:        ''},
          {type_windows:        ''},
          {count_doors:         ''},
          {length_doors:        ''},
          {height_doors:        ''},
          {type_doors:          ''},
          {date_doors:          ''},
          {class_energoeff:     ''},
          {count_closet:        ''},
          {count_sofa:          ''},
          {count_table:         ''},
          {count_small_closet:  ''},
          {count_men:           ''},
          {count_women:         ''},
          {count_children:      ''},
          {time_guests:         ''},
          {count_sink:          ''},
          {height_basement:     ''}
        ],

       type_windows:[
          {id: 1, val: "Деревянные окна с двойным остеклением"},
          {id: 2, val: "Стеклопакет 24мм (4-16-4) в корпусе ПВХ"},
          {id: 3, val: "Стеклопакет 24мм (4-16-4) в корпусе ПВХ, низкоэмиссионное покрытие"},
          {id: 4, val: "Стеклопакет 36мм (4-10-4-14-4) в корпусе ПВХ"},
          {id: 5, val: "Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ"},
          {id: 6, val: "Стеклопакет 44мм (4-12-4-20-4) в корпусе ПВХ, низкоэмиссионное покрытие"},
        ],
        
        type_doors:[
          {id: 1,  val: "Двери одинарные деревянные без тамбура"},
          {id: 2,  val: "Двери одинарные деревянные с тамбуром между ними"},
          {id: 3,  val: "Двери двойные (распашные) деревянные без тамбура"},
          {id: 4,  val: "Двери двойные (распашные) деревянные с тамбуром между ними"},
          {id: 5,  val: "Двери одинарные ПВХ без тамбура"},
          {id: 6,  val: "Двери одинарные ПВХ с тамбуром между ними"},
          {id: 7,  val: "Двери двойные (распашные) ПВХ без тамбура"},
          {id: 8,  val: "Двери двойные (распашные) ПВХ с тамбуром между ними"},
          {id: 9,  val: "Двери одинарные алюминиевые без тамбура"},
          {id: 10, val: "Двери одинарные алюминиевые с тамбуром между ними"},
          {id: 11, val: "Двери двойные (распашные) алюминиевые без тамбура"},
          {id: 12, val: "Двери двойные (распашные) алюминиевые с тамбуром между ними"}
        ],
        

        class_energoeff:[
          {id: 1,   val: "A++ (очень высокий, R = 8.8 м² °С/В)"},
          {id: 2,   val: "A+  (очень высокий, R = 7.5 м² °С/В)"},
          {id: 3,   val: "A   (очень высокий, R = 6.5 м² °С/В)"},
          {id: 4,   val: "B+  (высокий, R = 5.5 м² °С/В)"},
          {id: 5,   val: "В   (высокий, R = 4.5 м² °С/В)"},
          {id: 6,   val: "C+  (нормальный, R = 3.8 м² °С/В)"},
          {id: 7,   val: "С   (нормальный, R = 3.5 м² °С/В)"},
          {id: 8,   val: "С-  (нормальный, R = 3.2 м² °С/В)"},
          {id: 9,   val: "D   (пониженный, R = 2.8 м² °С/В)"},
          {id: 10,  val: "E   (низкий, R = 2.5 м² °С/В)"}    
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
            select:[['Класс энергетической эффективности ограждающих конструкций',['A++ (очень высокий)+++++++++++','A+ (очень высокий)','A (очень высокий)','B+ (высокий)','B (высокий)','C+ (нормальный)','C (нормальный)','C- (нормальный)','D (пониженный)','E (низкий)']]],
            c_box:null,
            date:[['Дата постройки','2011-12-15', [0, 0,'' ]]],
          },
          // 10
          {
            id: 'heat_los_heatcond_roof',
            title:'Характеристика класса энергетической эффективности', 
            input:[['Температура внутреннего воздуха','°C',  '', 'int', false, [0, 6, '']],['Расчётная температура наружного воздуха','°C',  '', 'int', false, [0, 7, '']], ['Длина здания','м', '', 'uint', false, [0, 2, '']],['Ширина здания','м', '', 'uint', false, [0, 3, '']]],
            r_btn:null, 
            select:[['Класс энергетической эффективности кровли',['A++ (очень высокий)','A++ (очень высокий)','A (очень высокий)','B+ (высокий)','B (высокий)','C+ (нормальный)','C (нормальный)','C- (нормальный)','D (пониженный)','E (низкий)']]],
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

    numberWithSpaces(x) {
      var parts = x.toString().split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, " ");
      return parts.join(".");
    },
    printVal(val, ue){
      return this.numberWithSpaces(parseFloat(val).toFixed(3)) + ' ' +  ue;
    },
    calc_dop_results(){
      if (this.results[2].val != ''){
        this.dop_results[0].val = parseFloat(this.results[2].val)  + parseFloat(this.results[3].val)  + parseFloat(this.results[4].val)  + parseFloat(this.results[5].val)  + parseFloat(this.results[6].val)  + parseFloat(this.results[7].val) + parseFloat(this.results[8].val) + parseFloat(this.results[9].val) + parseFloat(this.results[10].val);
        this.dop_results[1].val = parseFloat(this.results[11].val) + parseFloat(this.results[12].val) + parseFloat(this.results[13].val) + parseFloat(this.results[14].val) + parseFloat(this.results[15].val) + parseFloat(this.results[16].val);
        this.dop_results[2].val = this.dop_results[0].val - this.dop_results[1].val;
        this.dop_results[4].val = this.dop_results[2].val * 0.1486;
        this.dop_results[5].val = this.dop_results[2].val * 276.28;
      }
      if (this.results[18].val != '' && this.results[17].val != ''){
        this.dop_results[3].val = parseFloat(this.results[17].val) - parseFloat(this.results[18].val);
        this.dop_results[6].val = this.dop_results[3].val * 0.1486;
        this.dop_results[7].val = this.dop_results[3].val * 276.28;
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
          if (item.name !=='general')
                item.check = flag })
      }         
       ,
       set_all_checkbox(){  
          this.set_all_flag = !this.set_all_flag;  
          this.set_all_check_left_panel(this.set_all_flag.toString()); 
       } ,


       
      calc_result(id){
        let self = this
        this.results.forEach(function(item){
          if(item.id == id){
              let year = document.getElementById('years-selector');
              let calc_res = func.calc(id, self, year.value)
              item.val = calc_res[0]
              return false
          }
        })
        return id
      },
    calc_all_server(){
      let self = this
      this.sections.forEach(function(item){
          self.calc_result(item.name)
      })
    },
      calc_all(){
        this.set_all_check_left_panel("true")
        this.calc_all_server()
        this.set_all_check_left_panel("false")
        this.calc_dop_results();
      },
      calc_neuro(){
        this.choise_NM = !this.choise_NM;
      },
      calc_tec(){
        let self = this
        self.calc_result("tec", self)
        this.calc_dop_results()
      },
      calc_cpt(){
        let self = this
        self.calc_result("cpt", self)
        this.calc_dop_results()
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
    download_excel(){
      let downl_res = func.download_excel()
      console.log(downl_res)        
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
            console.log(this.functions[func_ind].select[dataid][3])
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
        this.clear_dop_results();
      },
      clear_dop_results(){
        this.dop_results.forEach(function(item){
          item.val = '';
        })  
      }
    },
    computed:{
      type_windows_selected(){
        if (this.parametrs_of_build.type_windows !== undefined)
            return this.type_windows[this.parametrs_of_build.type_windows-1].val      
      },
      type_doors_selected(){
        if (this.parametrs_of_build.type_doors !== undefined)
            return this.type_doors[this.parametrs_of_build.type_doors-1].val 
      },
      class_energoeff_selected(){
        if (this.parametrs_of_build.class_energoeff !== undefined)
            return this.class_energoeff[this.parametrs_of_build.class_energoeff-1].val   
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