# Contribuições

Para cada issue a ser resolvida, seguir o seguinte procedimento:

- Clone o repositório
- Prepare o ambiente como foi explicado acima
- Crie uma branch (local e remoto) sobre o problema a ser resolvido, e.g.:

```
$ git checkout -b dev-subscribers
$ git push -u origin dev-subscribers
```

- Após resolver a issue, rode os devidos testes (rode mesmo porque seu PR não será aceito se seus testes não estiverem passando!)
- Abra um ticket de pull request no github com o sentido (base <- head):

 ```
 unb-cic-esw/youtube-data-monitor/master <- unb-cic-esw/youtube-data-monitor/dev-subscribers
 ```

- Espere o Travis CI executar os testes de integração
- Se os testes passarem o adm disponível no momento irá aceitar seu PR :rocket:
