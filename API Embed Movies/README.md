### Acessando os Serviços

- Subir o Elasticsearch e o Kibana: 
  
  - Clone https://github.com/deviantony/docker-elk  e depois docker-compose up setup (coloca o setup!!!) e depois docker-compose up  (sem o setup!!!)

- Elasticsearch:
  
  - Você pode acessar o Elasticsearch em http://localhost:9200 ou http://<seu-ip>:9200 se estiver em um ambiente diferente.
  - Por exemplo, para verificar se o Elasticsearch está funcionando corretamente, você pode acessar http://localhost:9200/_cat/health?v.

- Kibana:

    - A interface do Kibana estará disponível em http://localhost:5601.
    - Após iniciar o Kibana, você pode configurá-lo para se conectar ao Elasticsearch e começar a explorar e visualizar seus dados.

- Create Index On Elasticsearch:
  
  - Use o notebook em python para criar o indice no ES

### Conda Info

active environment : p310
            shell level : 2
          conda version : 24.4.0
         python version : 3.12.3.final.0
                 solver : libmamba (default)
       virtual packages : __archspec=1=skylake
                          __conda=24.4.0=0
                          __win=0=0
               platform : win-64
             user-agent : conda/24.4.0 requests/2.31.0 CPython/3.12.3 Windows/11 Windows/10.0.22631 solver/libmamba conda-libmamba-solver/24.1.0 libmambapy/1.5.8 aau/0.4.4 c/. s/. e/.
          administrator : False
             netrc file : None
           offline mode : False

### Erro `current license is non-compliant for [security]`

Correção: 

```bash
curl -X POST 'http://localhost:9200/_license/start_basic?acknowledge=true' -u elastic:changeme -H "Content-Type: application/json"
```


