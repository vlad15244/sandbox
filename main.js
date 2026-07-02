import { Table } from './database.js';
import { Column } from './database.js';
import mysql from 'mysql2/promise';
import http from 'http';
import express from 'express';
import path from 'path';

const PORT = 3000;

const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: '1234',
  database: 'test'
};

const pool = mysql.createPool(dbConfig);
const table = new Table('node_ex');
const app = express();

(async () => {
    const connection = await pool.getConnection();



    table.AddColumn(new Column('ID', 'BIGINT',"UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY "));
    table.AddColumn(new Column('NAME', 'VARCHAR(45)', "NOT NULL"));    

    try {
        await connection.execute(table.CreateTable());
        console.log('Table created or already exists'); 
    } catch(err){
        console.log(`Error ${err} while connect with database`); 
    } finally{
        connection.end();
    }

})();

const server = http.createServer(async (req, res) => {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    if (req.method === 'GET' && req.url === '/') {
        res.statusCode = 200;
        res.end(JSON.stringify({ message: 'Node.js сервер работает', stack: 'pure http' }));
        return;
    }
    
    if (req.method === 'GET' && req.url === '/database') {
        let connection;
        try{

        connection = await pool.getConnection();

        const [rows] = await connection.query(table.SelectAll());

        res.statusCode = 200;
        res.end(JSON.stringify({ message: 'Node.js сервер работает', row : rows}));


        return;
        }
        catch(err){

        }
        finally {


        }
    }    

});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});
