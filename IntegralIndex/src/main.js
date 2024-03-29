import { createApp } from 'vue';
import App from './App';
import components from '@/UI';
import '@/styles/color.css';
import '@/styles/style.css';




const app = createApp(App);

components.forEach(component => { 
    app.component(component.name,component);
})

app.mount('#app')
