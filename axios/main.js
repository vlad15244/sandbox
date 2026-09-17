import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = 3000;
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views')); // папка с шаблонами

app.get('/', async(req, res) =>{  
    
    try{
        res.render('index');
    }
    catch(err){
        console.log(`Ошибка сервера ${err}`)
    }

} )

app.get('/api/example', async(req, res) =>{  
    
    try{
        console.log("this is AXIOS request");
        res.json({answer : "This is Hi from NODEJS"});
    }
    catch(err){
        console.log(`Ошибка сервера ${err}`)
    }

} )

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});