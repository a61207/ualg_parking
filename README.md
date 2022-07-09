# Gestão de Parque de Estacionamento
  
Projecto de Laboratório de Engenharia de Software na Licenciatuara de Engenharia Informática com objectivo de desenvolver um sistema informático 
de média dimensão integrando os conhecimentos disciplinas da área científica de Sistemas de Informação e Bases de Dados e recorrendo a metodologias 
ágeis, o tema selecionado envolve um sistema que faz a gestão de um sistema de parque de estacionamento. Para desenvolver este sistema em formato web 
foi utilizada a framework Django.

## Instalação de Projeto Windows 
## ( !!! NO BASH !!! NÃO NO POWERSHELL !!! )

1. Fazer clone do projecto:

```git clone https://github.com/a61207/ualg_parking.git```

2. Entrar no ambiente de trabalho:

```cd ualg_parking```

3. Criar ambiente virtual: 

```python -m venv venv```

4. Ativar ambiente virtual:

```.\venv\Scripts\activate```

5. Enable Settings File by Decompressing "settings.zip":

```tar -xf ualgParking\settings.zip -C ualgParking```

6. Instalar Requirements:

```pip3 install -r requirements.txt```

6. Fazer migração:

```python manage.py migrate```

7. Popular base de dados:

```python manage.py loaddata inidb.json```

8. Run server

```python manage.py runserver```

9. Run Task Scheduler Server (Not Required)

```celery -A ualgParking worker --beat --scheduler django --loglevel=info```

