# Data Collection

Há `data` (medida e factos por observação direta), `metadata` (data da data, como permissões e versões), e `information` (data processada, organizada e estruturada).

Informação são dados com contexto. O ciclo de vida da informação normalmente tem os seguintes passos:

- `Ocorrência`: descoberta, design, autor;
- `Transmissão`: através do acesso ou networking;
- `Processamento e manipulação`: coletar, validar, modificar, indexar, classificar, filtrar e armazenar;
- `Utilização`: monitorar, planear, para educar e aprender;

Aumentar o valor dos dados:

- Colocar os dados acessíveis;
- Combinar os dados, criar um documento coerente dentro do contexto sugerido;
- Eliminar os dados não estruturados ou nulos;
- Completar os atributos com informação de outras fontes;

## Data stages

- `Raw`: onde se dá a ingestion, understanding e criação de metadata;
- `Refined`: preparação dos dados para futura exploração. É o fruto final da pipeline de refinamento, constituída por substeps que ajudam a extrair a melhor parte da informação;
- `Production`: foco na integração dos dados refinados em processos finais e produtos;

Existem vários padrões de processamento de dados, como por exemplo:

### ETL

Extract, Transform, Load. É normalmente associada a operações de IT centralizadas.

### ELT

Evolução do ETL, onde há Extract, Load e Transform. Para uma melhor divisão das responsibilidades, pois data engineer e data analyst podem trabalhar em paralelo e de forma independente.

### OSEMN

- `Obtain`;
- `Scrub` - limpar, arranjar, preparar;
- `Explore` - observar, experimentar e visualizar;
- `Model` - criar um modelo estatístico;
- `Interpret` - retirar conclusões, avaliando e interligando os resultados;

Há iteração entre estas etapas e podem inclusive não ser feitas por esta ordem. O processo pode ser **centralizado** em departamentos e **descentralizado** em equipas especializadas.

Por um lado é bom ter o sistema centralizado (permite maior controlo e reutilização de modos de processamento), mas por outro pode demorar tempo por dependerem de um único departamento nas decisões.

Os Data Engineers desenham, implementam e mantêm os processamentos das pipelines de dados. 

## Open Data

O conceito de FAIR (findable, accessible, interoperable, reusable) é usado para Open Data. Esses dados podem ser estruturados e não estruturados. 

## Data Selection

É importante saber se o autor dos dados é confiável, se pode ser contactado, se os dados são regularmente atualizados, se os dados incluem informação da data da sua aquisição e se são plausíveis.

A serialização dos dados numa pipeline permite uma manipulação in-memory, mas ao mesmo tempo restringe o funcionamento a uma só linguagem de programação. Pode ser de dois formatos:
- `JSON and XML Serialization`: mais comuns, bastante suportados, mas tem ambiguidade em termos de números e dados binários (imagens);
- `Binary Serialization`: menos visual mas é mais compacta e rápida. 

Uma boa escolha de dados passa por estudá-los antes de processá-los:

- Missing data, inconsistent, duplicated, precision problems;
- Analisar a tendência, como a média, e a dispersão;
- Diagramas de frequência - histogramas, 

No entanto esta abordagem apenas apresenta um sumário, pois os dados possuem mais características. Os `outliers` e `missing data` são exemplos de partes que podem ser analisados de forma descritiva mas também de exploratória visualização.