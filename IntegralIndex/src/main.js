import { createApp } from 'vue';
import App from './App';
import components from '@/UI';
import '@/style.css';


const app = createApp(App);

components.forEach(component => { 
    app.component(component.name,component);
})

app.mount('#app')
