# Data Collection

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

