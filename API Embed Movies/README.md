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