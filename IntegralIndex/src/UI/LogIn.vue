<template>
<!-- <div class="dialog" v-if="show[0]" @click.stop="hide_dialog"> -->
<div class="dialog" v-if="show[0]">
  <div @click.stop class="dialog_main">
    <div class="dialog_header">
      Войти
    </div>
    <h style="color: red" v-if="Flag">Все поля должны быть заполнены!</h>
    <h style="color: red" v-if="Flag2">Неверный логин или пароль, попробуйте ещё раз!</h>
    <div class="dialog_content">
      <div class="content"> 
        <b>Логин</b>
        <input class="dialog_inp" type="text" :id="login" v-model="login_">
      </div>
      <div class="content">
        <b>Пароль</b>
        <input class="dialog_inp" type="password" :id="password" v-model="psw">
      </div>
    </div>
    <div class="dialog_buttons">
      <button class="dialog_btn" v-on:click="enter_()">
        Войти
      </button>
      <button class="dialog_btn" v-on:click="go_to_reg_page()">
        Регистрация
      </button>
    </div>
  </div>
</div>
    
</template>

<script>
import login_funcs from '@/connect/login'
export default {
   data(){
    return{
      login_: "",
      psw: "",
      Flag: false,  // флаг для проверки, что все поля заполнены
      Flag2: false,  // флаг для проверки, что такой пользователь есть в системе
    }
  },
  name: 'dialogbox-login',
  props:{
    show:{
      type: Boolean,
      default: false
    }
  },
  methods:{
    hide_dialog(){
      this.$emit('update:show', [false, false])
    },
    enter_(){
      login_funcs.enter(this)
    },
    go_to_reg_page(){
      this.hide_dialog();
      this.$emit('update:show', [false, true])
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
  font-size: 20px;
  color: #26495c;
}
.dialog_main{
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;

  margin: auto;
  background: white;
  min-height: 30%;
  min-width: 40%;
  border: 2px solid #234455;
  border-radius: 4px; 
  padding: 1%;
}
.dialog_content{
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: center;

  margin: auto;
  padding: 1%;

  width: 100%;
}
.content{
  display: flex;
  flex-direction: column;
  margin: 1%;
}
.dialog_inp{
  background-color: #e5e5dc; 
  border: 2px solid #435d6b;
  border-radius: 4px; 
  padding-left: 1%;
  padding-right: 1%;
  margin: 0.25%;
  width: 100%;
}
.dialog_buttons{
  display: flex;
  justify-content: center;
}
.dialog_btn{
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
</style>