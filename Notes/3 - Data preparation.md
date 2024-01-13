# Data Preparation

Os dados reais precisam de ser tratados e este é o passo mais demorado para a criação de um search system consistente.

## Data preparation tasks

- Data `cleaning` - identificação e reparação da qualidade do dataset;
- Data `transformation` - para melhorar a análise e manipulação;
- `Sintetizar` os dados - criação de atributos derivados;
- Data `integration` - combinar os dados de diferentes fontes;
- Data `reduction or selection` - eliminar dados para obter uma coleção mais consistente;

## Data Reduction or Selection

### 1 - Data filtering

São operações determinísticas segundo um atributo ou conjunto. Usada quando se verifica um padrão nos atributos incorrectos e podem ser por isso ser retirados sem comprometer os dados que restam.

### 2 - Data sampling

Processo não determinístico que visa retirar um subconjunto aleatório de dados. É importante analisar a distribuição dos dados antes e depois do sampling para garantir que a amostra é equilibrada e representativa do todo.

### 3 - Data aggregation

Agrupar os dados para eliminar um detalhe excessivo. Os operadores são por norma: média, mediana, mínimo, máximo, percentil.

### 4 -  Tools

- Data cleaning: OpenRefine;
- Data preparation: Beautiful Soup, NLTK;
- Data processing: R, Python Pandas;

##  Data pipelines

Conjunto de processos sequenciais que transformam os dados de diversas formas e de diversos destinos. Devem ser confiáveis, escaláveis e passíveis de manutenção. <br>
As principais ferramentas para automatizar as pipelines são: Makefiles, Apache Airflow, Apache Beam, Apache NiFi, Apache Kafka, Apache Flinks.

### Data Flow Diagrams (DFD)

Uma boa forma de documentar as pipelines:

- `Squares`: para representar entidades externas, sources or destinations;
- `Rounded rectangles`: os processos, devem ter como input os dados e output um refinamento desses mesmos dados;
- `Arrows`: o flow dos dados no sistema ou pipeline;
- `Storage`: acompanhado com o formato (SQL, CSV, JSON);