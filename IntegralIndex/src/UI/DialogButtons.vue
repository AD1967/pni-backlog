<template>
<div class="dialog" v-if="show" @click.stop="hide_dialog">
  <div @click.stop class="dialog_main">
    <div class="dialog_header">
      Данные изменены, как проводить расчёт?
    </div>
    <div class="content" v-if="show_name"> 
      <b>Название шаблона</b>
      
      <input class="inp_pat" type="text" :value="name" @input="update_name">
      <br>
      <div>
        <input type="radio" value="Сохранять полностью" v-model="picked">
        <label>Сохранять полностью</label>
      </div>
      <div>
        <input type="radio" value="Сохранять только из выбранных расчётов" v-model="picked">
        <label>Сохранять только из выбранных расчётов</label>
      </div>
      <br>
      <div v-if="error_show">
        <div v-if="error_text == ''">
          <b style="color:red"> Ошибка сохранения шаблона </b>
        </div>
        <div v-else>
          <b style="color:red">
            {{error_text}}
          </b>
        </div>
      </div>
      <div class="dialog_buttons">
        <button class="dialog_btn" @click="server_result()"><p> Сохранить и рассчитать</p> </button>
        <button class="dialog_btn" @click="update_click(2)"><p> Отмена </p></button>
      </div>
    </div>
    <div v-else>
      <br>
      <div class="dialog_buttons">
        <button class="dialog_btn" @click="server_show()"><p> Сохранить и рассчитать</p> </button>
        <button class="dialog_btn" @click="update_click(1)"><p> По сохранённому шаблону</p></button>
        <button class="dialog_btn" @click="update_click(2)"><p> Отмена </p></button>
      </div>
    </div>
  </div>
</div>
    
</template>

<script>
export default {
  name: 'dialog-buttons',
  props:{
    name: {
      String,
      default: ""
    },
    show:{
      type: Boolean,
      default: false
    },
    error_show: {
      type: Boolean,
      default: false
    },
    error_text:{
      type: String,
      default: ''
    }
  },
  data() {
    return {
      show_name: false,
      picked: 'Сохранять только из выбранных расчётов'
    }
  },
  watch: { 
      show: function() {
        this.$emit('update:error_show', false)
        this.show_name = false
        this.picked = 'Сохранять только из выбранных расчётов'
      }
  },
  methods:{
    hide_dialog(){
      this.$emit('update:show', false)
      this.$emit('result', [2,this.picked])
    },
    update_click(val){
      this.$emit('update:show', false)
      this.$emit('result', [val,this.picked])
    },
    server_show(){
      this.show_name = true
    },
    server_result(){
       this.$emit('result', [0,this.picked])
    },
    update_name(val){
      this.$emit('update:name', val)
    }
  }
}
</script>

<style scoped>
.dialog{
  position: fixed;
  display: flex;

  top: 0;
  bottom: 0;
  left: 0;
  right: 0;

  background: rgba(0,0,0,0.5);
}
.dialog_header{
font-weight: bold;
  font-size: 30px;
  color: #26495c;
  margin-bottom: 2%;
  text-align: center;
}
.dialog_main{
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;

  margin: auto;
  background: white;
  min-height: 10%;
  min-width: 60%;
  border: 2px solid #234455;
  border-radius: 4px; 
  padding: 1%;
}

.dialog_buttons{
  margin: 2%;
  display: flex;
  justify-content: space-between;
}
.dialog_btn{
  padding-top:1.5%;
  padding-bottom:1.5%;
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
.dialog_btn:hover{
  display: flex;
  justify-content: center;
  width: 30%; 
  background-color: #26495c; 
  border: 2px solid #234455;
  border-radius: 10px; 
  box-shadow: 0 0 5px #1e3a49 inset;
  color: #e5e5dc;
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
</style>
