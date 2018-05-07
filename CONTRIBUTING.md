# Contribuições

## Ferramentas utilizadas

* [python 3.6](https://www.python.org/)
* [pip](https://pypi.python.org/pypi/pip)
* [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/)

## Preparar o ambiente

### Clonar repositório

```
$ git clone git@github.com:unb-cic-esw/youtube-data-monitor.git
```

### Criar virtualenv

```
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

### Instalar dependências

Todas as bibliotecas de que o projeto depende estão listadas no arquivo
[requirements.txt](requirements.txt). Para instalá-las, execute:

```
$ cd youtube-data-monitor
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Acesso à API do Youtube

Neste projeto, utilizamos
[a Youtube Data API v3](https://developers.google.com/youtube/v3/). Para que o
script funcione corretamente, é necessário que você registre seu projeto e
crie as credenciais necessárias para acesso à API. As instruções estão
disponíveis no [Create API Keys](https://developers.google.com/youtube/registering_an_application#Create_API_Keys).

Crie uma credencial do tipo API key e faça os seguintes procedimentos:

```
$ cd youtube-data-monitor
$ echo 'export YOUTUBE_KEY=SUA_API_KEY' >> venv/bin/activate
```

Adicione a seguinte linha dentro da função ```deactivate()``` dentro do
arquivo ```venv/bin/activate```:

```
deactivate () {
    ...

    # Unset youtube api key variable
    unset YOUTUBE_KEY
}
```



Com isso toda vez que ativar seu ambiente virtual você terá uma variável de
ambiente com sua API Key do Youtube, e
toda vez que desativar o ambiente virtual, esta variável será apagada. Para
testar faça o seguinte:

```
$ source venv/bin/activate
$ echo $YOUTUBE_KEY
```

Após estes comandos sua API deverá mostrar no terminal.

```
$ deactivate
$ echo $YOUTUBE_KEY
```

Após estes comandos sua API não aparecerá no terminal.

Para testar a API o Youtube também disponibiza uma interface para testar as
requisições nos endpoints >
[Try this API](https://developers.google.com/youtube/v3/docs/search/list?hl=pt-br&apix=true).

## Adicionar funcionalidades

Para cada estória a ser resolvida, seguir o seguinte procedimento:

- Clone o repositório
- Prepare o ambiente como foi explicado acima
- Crie uma branch (local e remoto) sobre o problema a ser resolvido, e.g.:

```
$ git checkout -b dev-subscribers
$ git push origin dev-subscribers
```

- Após resolver a issue, rode os devidos testes (rode mesmo porque seu PR não
  será aceito se seus testes não estiverem passando!)
- Abra um ticket de pull request no github com o sentido (base <- head):

 ```
 unb-cic-esw/youtube-data-monitor/master <- unb-cic-esw/youtube-data-monitor/dev-subscribers
 ```

- Espere o Travis CI executar os testes de integração
- Se os testes passarem o adm disponível no momento irá aceitar seu PR :rocket:



## Executar os testes

Todos os testes foram desenvolvidos utilizando a biblioteca
[unittest](https://docs.python.org/3/library/unittest.html) nativa do Python.
Para executá-los, a partir da pasta raiz do projeto, execute:

```
$ python -m unittest discover tests
```

## Checar estilo de código

Para seguir os padrões PEP8 de código python estamos usando a biblioteca
[pycodestyle](http://pycodestyle.pycqa.org/en/latest/).
Para cada novo módulo adicionado ao projeto é necessário criar um teste para
checar seu estilo de código (ver exemplos em [test_pep8](tests/test_pep8.py)).
Para executar a ferramenta e checar algum código, basta executar:

```
$ pip install pycodestyle
$ pycodestyle youtube/youtube.py
```

## Periodicidade e automatização da coleta dos dados

Para automatizar a execução do programa, utilizamos a ferramenta **crontab**.
Um script foi escrito para adicionar a rotina de coletar os dados da api do
Youtube à meia-noite como é possível ver no arquivo
[scheduler.sh](scheduler.sh). Para ativar a rotina basta escrever o seguinte
comando no terminal:
```
$ bash scheduler.sh
```
Para editar os crontabs:
```
$ crontab -e
```
Para listar os crontabs:
```
$ crontab -l
```

Em sistemas Linux, adicione a seguinte linha no arquivo aberto pelo comando
de editar crontab:
```
$ 0 0 * * * comando_a_ser_executado
```
O primeiro '0' diz respeito ao minuto, já o segundo '0' às horas. É usado o
sistema de 24 horas. Com o comando abaixo, o programa será executado todos os
dias à meia-noite.
```
$ 0 0 * * * cd $HOME/youtube/youtube-data-monitor && . venv/bin/activate && python -m youtube.update
```
