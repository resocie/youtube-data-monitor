# Monitor de Dados do Youtube

![Travis_Build](https://travis-ci.org/unb-cic-esw/youtube-data-monitor.svg?branch=master)

Este repositório compõe projeto de pesquisa com foco empírico nas eleições brasileiras de 2018 do grupo de pesquisa [Resocie](http://resocie.org) do [Instituto de Ciência Política - IPOL](http://ipol.unb.br/) com o apoio técnico do [Departamento de Computação - CIC](http://www.cic.unb.br/) da [Universidade de Brasília - UnB](http://unb.br).

O projeto consiste na coleta sistemática de informações quantitativas da plataforma Youtube com o objetivo de subsidiar a análise do comportamento político de alguns atores da cena eleitoral durante o período de campanha. Além de seu objetivo finalístico para a coleta de dados, o projeto tem também por intuito servir de material de estudo dos alunos da disciplina Engenharia de Software do Departamento de Ciência da Computação da UnB no 1º semestre de 2018.

As instruções a seguir trazem orientações para aqueles que quiserem contribuir com a iniciativa. Para contribuir por favor leia o arquivo [CONTRIBUTING to resocie youtube-data-monitor](CONTRIBUTING.md) antes.

## Preparar ambiente

Um bom processo de trabalho em desenvolvimento de software começa com a preparação de um ambiente adequado de programação.


### Instalar pacotes básicos

* [python 3.6](https://www.python.org/)
* [pip](https://pypi.python.org/pypi/pip)
* [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/)

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

Todas as bibliotecas de que o projeto depende estão listadas no arquivo [requirements.txt](requirements.txt). Para instalá-las, execute:

```
$ cd youtube-data-monitor
$ source venv/bin/activate
$ (venv) pip install -r requirements.txt
```

### Acesso à API do youtube

Neste projeto, utilizamos [a Youtube Data API v3](https://developers.google.com/youtube/v3/). Para que o script funcione corretamente, é necessário que você registre seu projeto e crie as credenciais necessárias para acesso à API. As instruções estão disponíveis no [Create API Keys](https://developers.google.com/youtube/registering_an_application#Create_API_Keys).

Crie uma credencial do tipo API key e faça os seguintes procedimentos:

```
$ cd youtube-data-monitor
$ echo 'export YOUTUBE_KEY=SUA_API_KEY' >> venv/bin/activate
```

Adicione a seguinte linha dentro da função ```deactivate()``` dentro do arquivo ```venv/bin/activate```:

```
deactivate () {
    ...

    # Unset youtube api key variable
    unset YOUTUBE_KEY
}
```

Com isso toda vez que ativar seu ambiente virtual você terá uma variável de ambiente com sua API Key do Youtube, e
toda vez que desativar o ambiente virtual, esta variável será apagada. Para testar faça o seguinte:

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

Para testar a API o Youtube também disponibiza uma interface para testar as requisições nos endpoints > [Try this API](https://developers.google.com/youtube/v3/docs/search/list?hl=pt-br&apix=true).

### Executar os testes

Todos os testes foram desenvolvidos utilizando a biblioteca [unittest](https://docs.python.org/3/library/unittest.html) nativa do Python. Para executá-los, a partir da pasta raiz do projeto, execute:

```
$ python -m unittest discover tests
```


## TODO

Este é apenas um esqueleto de projeto para que o grupo comece a trabalhar. Resta ainda muito trabalho a ser feito. Algumas ideias:

* Expandir a variedade dos dados buscados
* Explorar novas possibilidades de coleta
* Criar interface CLI para execução do programa
* Implementar mecanismo para automatização da coleta recorrente dos dados
* Persistir dados coletados em base estruturada
* Viabilizar interface de integração da base de dados criada com canal para geração de informações visuais
