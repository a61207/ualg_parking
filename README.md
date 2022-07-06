# Gestão de Parque de Estacionamento
  
Projecto de Laboratório de Engenharia de Software na Licenciatuara de Engenharia Informática com objectivo de desenvolver um sistema informático 
de média dimensão integrando os conhecimentos disciplinas da área científica de Sistemas de Informação e Bases de Dados e recorrendo a metodologias 
ágeis, o tema selecionado envolve um sistema que faz a gestão de um sistema de parque de estacionamento. Para desenvolver este sistema em formato web 
foi utilizada a framework Django.

## Instalação de Projeto

1. Fazer clone do projecto:

```git clone https://github.com/a61207/ualg_parking.git```

2. Criar ambiente virtual: 

```python -m venv venv```

3. Ativar ambiente virtual:

```source venv/bin/activate```
```. venv/Scripts/activate```

4. Enable Settings File by Renaming from "__settings.py" to "settings.py":

5. Instalar Requirements:

```pip3 install -r requirements.txt```

6. Fazer migração:

```python manage.py migrate```

7. Popular base de dados:

```python manage.py loaddata inidb.json```

8. Run server

```python manage.py runserver```

