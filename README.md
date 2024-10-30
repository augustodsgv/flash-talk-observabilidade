# Flash talk observabilidade
## Como rodar
Primeiro, tenha o Docker e o Docker compose instalados. Caso não o tenha:
```sh
curl https://get.docker.com/ | sudo sh
sudo usermod -aG docker $USER
newgrp docker
```
Após isto, clone o repositório
```sh
git clone https://github.com/augustodsgv/flash-talk-observabilidade.git
```
Por fim, rode o docker compose
```sh
cd flash-talk-observabilidade
docker compose up
```
A aplicação estará rodando em [localhost:8000](http://localhost:8000) e o prometheus em [localhost:9090](http://localhost:9090)
## Stress APP
Esta é uma api simples que aceita requisições REST para estressar o computador, tanto em memória quanto em CPU. Ela conta com dois endpoints:
### POST /cpu-stress
Estressa "core_n" cores da CPU durante "stress_time" segundos. Exemplo de payload

```json
{
    "stress_time":"5",
    "cores_n":"3"
}
```
Deixa a 3 cores em 100% durante 3 segundos
### POST /memory-stress
Aloca "n_bytes" bytes de memória durante "stress_time" segundos. Exemplo de payload

```json
{
    "stress_time":"20",
    "bytes_n":"6000000000"
}
```
Aloca 6.000.000.000 bytes (~6GB) durante 20 segundos.
## Stack de monitoramento
O monitoramento é feito pelo Prometheus junto ao Node-Exporter e o FastAPI Exporter.
### Prometheus
O Prometheus é o coração da stack: Ele bate nos endpoints dos exporters em intervalos de tempo, coleta as métricas providas e armazena os dados em seu banco de dados de séries temporais. 
Cada métrica coletada tem labels, que indicam para o Prometheus como distinguir séries temporais diferetes. Por exemplo: suponha duas aplicações `foo` e `bar`. A métrica de disponibilidade `up` receberá uma label de `job`, de modo que temos duas séries temporais distintas.
```
up{job="foo"}
up{job="bar"}
```
Para recuperar os dados, usamos da linguagem de querys PromQL. Ela pode ser usada para coletar dados de maneira imediata, criar dashborads e até mesmo alertas. Por exemplo, supomos que queremos saber o número de requisições http que tivemos na API do Stress APP. O exporter de FastAPI provê a métrica `http_request_total`. Podemos recuperar o número total usando a query
```
http_request_total
```
Se quisermos agrupar pelo endpoint usado, podemos usar:
```
sum(http_request_total) by (handler)
```
Existe um mundo das queries de PromQL, que pode ser descoberdo de forma mais completa na [documentação oficial](https://prometheus.io/docs/prometheus/latest/querying/basics/).

Isso tudo, toda via, não seria possível sem os exporters

### Exporters
Os exporter são programas que vão coletar as métricas desejadas e disponibilizá-las através de um servidor http para que o prometheus possa raspar.
No geral, isso fica disponível no endpoint `/metrics`, e pode ser acessado usando um simples GET, que vai oferecer os dados no seguinte formato
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 3463.0
python_gc_objects_collected_total{generation="1"} 2351.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 48.0
python_gc_collections_total{generation="1"} 4.0
python_gc_collections_total{generation="2"} 0.0
...
```
No arquivos prometheus.yml, é possível configurar onde o Prometheus pode encontrar esses endpoints de métricas. Por exemplo, para obter métricas do node-exporter basta adicionar:
```diff
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

Existem inúmeros [exporter prontos](https://prometheus.io/docs/instrumenting/exporters/), como do [Postgres](https://github.com/prometheus-community/postgres_exporter), do [Redis](https://github.com/oliver006/redis_exporter), [Nginx](https://github.com/knyar/nginx-lua-prometheus), etc, que podem ser implantados via bibliotecas ou instalados durante o deploy da aplicação.

## Conclusões
A coleta de métricas é uma atividade importantíssima na atividade de DevOps e SRE, pois apresentam uma maneira de medir o desempenho e a saúde de aplicações que estão sendo deployadas, observar erros ocultos e obter insights sobre como recursos estão sendo utilizados.

O Prometheus é uma ferramenta OpenSource utilizada em grande parte da indústria e se apresenta como uma ótima opção para aqueles que querem implemntar observabilidade em seus ambiente de forma fácil e gratuita.

## Links úteis
[Deploy do Prometheus](https://prometheus.io/docs/prometheus/latest/installation/)

[Monitoramento da máquinas host do docker via node-exporter](https://grafana.com/docs/grafana-cloud/send-data/metrics/metrics-prometheus/prometheus-config-examples/docker-compose-linux/)

[Monitoramento de FastAPI](https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn)