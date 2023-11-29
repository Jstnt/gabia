import sqlite3

conecao = sqlite3.connect('somatoriokcal.db')

conecao.execute ("""  
CREATE TABLE IF NOT EXISTS usuario (
 
                
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome varchar (50) NOT NULL, 
  idade INTEGER,
  email TEXT NOT NULL, 
  genero varchar (15),
  peso REAL,
  altura REAL);
  
""")

conecao.execute ("""
    
 CREATE TABLE IF NOT EXISTS lancamento (

id INTEGER PRIMARY KEY AUTOINCREMENT,
  Data date,
  Refeicao VACHAR (30) NOT NULL, 
  calorias FLOAT,
  totalcaloria FLOAT,
  id_usuario integer,
  FOREIGN KEY(id_usuario) REFERENCES usuario(id))

""")

conecao.close()

