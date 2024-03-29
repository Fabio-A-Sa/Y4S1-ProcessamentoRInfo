# Information Retrieval

Forma de encontrar e extrair informação relevante de grandes coleções de dados naturalmente não estruturados, como textos. A pesquisa é feita com base em documentos (resultado da reestruturação dos dados iniciais). Não confundir com bases de dados: aqui os resultados são ordenados por relevância, e esse é o principal desafio.

## NPL

O processamento de linguagem natural pode e deve ser usado para Information Retrieval, embora seja desafiante porque a linguagem é ambígua. Extrai informação estruturada para melhor compreensão, extrai também relações, entidades e sentimentos. Conceitos principais:

- `Tokenization`: partir o texto em palavras ou tokens com significado individual;
- `Part-of-Speach (POS) tagging`: dar assign aos tokens, com base em dados gramáticos (verbo, adjectivo);
- `Named Entity Recognition (NER)`: para identificação de entidades como nomes ou lugares; 
- `Syntatic Analysis`: dar parse das frases para entender partes semânticas;
- `Stemming and Lemmatization`: redução das palavras ao seu root (jumping, jump) e redução das palavras à sua base (better, good);
- `Semantic Analysis`: explora o contexto;
- `Sentiment Analysis`: explora os sentimentos com base nas palavras. Classifica-os como positivo, negativo ou neutro;
- `Information extraction`: identifica uma informação estruturada com relações entre tokens;

Pode também ser usada para vários fins:

- **Rule-Based**: usados para identificar entidades, como emails;
- **Statistical**: para prever a próxima palavra de um texto;
- **Machine Learning**: para análise de sentimentos;
- **Deep Learning**: para tradução de textos com base em transformers;

#### Representação textual

- Baseada pela frequência: Bag of Words (BOW), TF-IDF, N-grams (sequências de N tokens contínuos);
- Baseada pela representação semântica: Word Embeddings (king - man + woman = queen), Document Embeddings, Topic Models;
- Baseada pela estrutura: Syntax-Based Representations, Graph-Based Representations;

## Apache Solr

Plataforma de pesquisa de código aberto escrita em Java, escalável, que serve para retornar conteúdos ordenados por relevância. Interage-se com o sistema com base em REST API HTTP, com respostas em JSON ou XML.

### Lucene

Biblioteca escrita em Java que contém os blocos fundamentais para implementar capacidades de searching, indexing e ranking, através de um querying parsing.

### Solr

Uma search engine que usa Lucene e está preparado para um deploy em servidores de larga escala e com grandes volumes de dados. Possui uma interface e pesquisas com:
- faceting;
- highlighting;
- autocomplete

#### Solr Key Concepts

- A informação mais básica de Solr é o `document`;
- Cada document é coposto por `fields`, e cada um tem um tipo específico (date, currency, text, uuid...). Os tipos e definições são declarados em **schema file**;
- Os `textual fields` são tratados numa pipeline com três processos:
    1. `Analysers`: gera um token stream a partir do texto inicial. Contêm duas partes principais: os tokenizers e os filters;
    2. `Tokenizers`: recebe um character stream e retorna uma sequência de token objects;
    3. `Filters`: examina os tokens recebidos e transforma, descarta, deixa, cria novos;
- Pode ter vários `cors`/`indexes`, que guardam a informação dos documentos indexados;
- Suporta REST API para indexes e para queries;
- Os `query parsers` convertem uma string de pesquisa numa query em Lucene e encontra os documentos selecionados;

#### Setup and run

- Colocar o Apache Solr a correr usando o Docker:

```bash
$ docker run --name <PROJECT_NAME> -d -p 8983:8983 solr
```

- Criar um novo `core` para agrupar informação sobre os futuros documentos a indexar:

```bash
$ docker exec <PROJECT_NAME> solr create_core -c <CORE_NAME>
```

- Deste modo, os documentos a inserir no seguinte passo podem ser indexados sem definições extra (*schemaless mode*). A inserção é feita através de um pedido POST:

```bash
$ curl -X POST -H 'Content-type:application/json' \ --data-binary "@./<FILE>.json" \ http://localhost:8983/solr/<PROJECT_NAME>/update\?commit\=true
```

#### Queries

Ou usando diretamente o `Solr Admin`, ou então através de requests:

```bash
$ curl http://localhost:8983/solr/<PROJECT_NAME>/query -d '{ "query": "content:portugal"}'
$ curl 'http://localhost:8983/solr/<PROJECT_NAME>/select?q=*&fl=id,title' # retorna apenas o ID e o TITLE
```

Uma das limitações de `schemaless` é que os acentos importam.

#### Schemas

Há três tipos não-primitivos que podem ser definidos:
- `Fields`: título de um campo de texto e contexto desse campo;
- `dynamicFields`: para indexar campos que não estão explícitos no schema, mas que podem ser pesquisados com base em patterns. Por exemplo, definir um novo field para todos os fields que acabem em "_txt";
- `copyFields`: copiam automaticamente o conteúdo de um field para outro. Usados para remover pontuação nas queries mas deixar o field original para visualização;

A estrutura do schema pode ser loaded usando o comando:

```bash
$ curl -X POST -H 'Content-type:application/json' \ --data-binary "@./<FILE>.json" \ http://localhost:8983/solr/<PROJECT_NAME>/schema
```

Para definir um novo schema, o anterior deve ser eliminado. E só depois há o load dos documentos a consultar. Um exemplo de ficheiro de configuração do schema:

```json
{
    "add-field-type": [
        {
        "name":"newsContent",
        "class":"solr.TextField"
        }
    ],

    "add-field": [
        {
        "name": "content",
        "type": "newsContent",
        "indexed": true
        }
    ] 
}
```

Para cada field, há possibilidade de adicionar informações sobre o `indexAnalyser` e o `queryAnalyser`. Cada analyser pode conter um só `tokenizer` e vários `filters`.

```json
{
    "add-field-type": [
        {
            "name":"newsContent",
            "class":"solr.TextField",
            "indexAnalyzer": {
                "tokenizer": {
                    "class":"solr.StandardTokenizerFactory"
                },
                "filters": [
                    {"class":"solr.ASCIIFoldingFilterFactory", "preserveOriginal":true},
                    {"class":"solr.LowerCaseFilterFactory"},
                ],
            },
            "queryAnalyzer": {
                "tokenizer": {
                    "class":"solr.StandardTokenizerFactory"
                },
                "filters":[
                    {"class":"solr.ASCIIFoldingFilterFactory", "preserveOriginal":true},
                    {"class":"solr.LowerCaseFilterFactory"}
                ],
            }
        }
    ]
}
```

Os `tokenizers` vão quebrar o texto numa stream de tokens de acordo com uma regra. Há uma grande lista de possíveis a usar no projecto, ver [aqui](https://solr.apache.org/guide/solr/latest/indexing-guide/tokenizers.html). Alguns exemplos:
- Standard, usa white spaces e pontuação;
- Lower case, limita non-letters e coverte todas depois para lowercase. White spaces e non-letters são descartados;
- N-Gram, gera streams com N tokens. Bom para pesquisa contextual;

Os `filters` processam a stream de tokens e gera um conjunto diferente de tokens, com base em transformações, eliminações e afins. Há [uma grande lista](https://solr.apache.org/guide/solr/latest/indexing-guide/filters.html) de filtros disponívels para Solr. Exemplos:
- ASCII Folding: converte tudo no seu equivalente ASCII code;
- Lowercase: converte qualquer caracter não-lowercase em lowercase;
- Stop: descarta qualquer token que possua palavras de stop. Podem ser indicadas num ficheiro;
- Snowball Porter Stemmer: aplica patterns com base numa linguagem específica;

#### Parsers

- `Standard`, é o mais simples mas também intolerante em erros de sintaxe;
- `DisMax`, permite cometer alguns erros, apropriado para aplicações gerais;
- `eDisMax`, ou extended DisMax, pois também permite queries mais complexas;

Com **eDisMax** podemos simplesmente:

```note
defType=edismax&qf=title+content+summary&q=flower
```

em vez de 

```note
q=title:flower+AND+content:flower+AND+summary:flower
```

#### Pesos

Também dá para atribuir pesos aos atributos a pesquisar:

```note
qf=title^5+content+summary^3
```

## Evaluation

A avaliação é o coração da **Information Retrieval** e depende da tarefa, da coleção (news articles, web pages, scientific articles) e do tipo de informação necessária. É importante para entender o uso do sistema por parte dos utilizadores e definir novos designs e implementações com base no feedback recebido. 

### Not Ranked

É importante distinguir duas coisas da satisfação dos utilizadores:

- `Eficácia`: medida da habilidade do sistema encontrar a informação certa;
- `Eficiência`: medida da habilidade do sistema encontrar informação rapidamente;

Em termos de eficácia, a avaliação passa por identificar um conjunto de documentos, classificá-los em relevantes ou não e depois recorrer à percentagem retornada pelo sistema de busca.

#### Paradigma de Cranfield

Proporcionou o fundamento para as avaliações atuais de sistemas de informação e culmina no cálculo de valores de Precision e Recal, que são baseados em conjuntos:

- `Precision`: Número de documentos relevantes retirados / Número total de documentos retirados;
- `Recall`: Número de documentos relevantes retirados / Número de documentos relevantes do sistema;
- `Accuracy`: true (positives | negatives) / total;
- `F Measure`: calculado com base em valores de recall e de precision;

### Ranked

#### Precision Recall Curves

Para cada subconjunto de documentos rankeados retornados, e para cada sequência de documentos nesse subconjunto, calcular valores de (recall, precision) para desenhar a curva.

#### Precision at K (P@K)

No caso da WEB, a maioria dos utilizadores não precisa de grande recall, ou seja, não interessa a percentagem de resultados relevantes dado todos os documentos importantes, mas sim a quantidade de documentos relevantes naquele conjunto retornado. Assim, a precisão toma uma importante função e é necessário escolher a quantidade K adequada para que a precisão seja máxima.

#### Mean Average Precision (MAP)

É uma das mais comuns medidas usadas em IR. Trata-se da média de Average Precision dos vários conjuntos retornados, calculados para K documentos rankeados e úteis.

![MAP](../Images/MAP.png)

### Eficiência

A eficiência pode ser medida através de:

- Tempo de indexação;
- Latência de pesquisas;
- Tamanho do índex criado;

## IR Overview

### Boolean Model

Uma matriz de incidência é simplesmente um modo de representação que indica se o termo da linha X está presente no documento da coluna Y. Este `Boolean Retrieval Model`:

- vê documentos como um conjunto de palavras;
- tem a facilidade de poder fazer operações bitwise;
- pode ser considerado um BoW (*Bag of Words*) se for considerado também o número de ocorrências;

### Inverted Index

Cada palavra é ligada a uma lista de listas, cada uma podendo conter até 3 argumentos:

- `A`: O index do documento onde a palavra está presente;
- `B`: A quantidade de vezes onde essa palavra está presente naquele documento;
- `C`: Os indexes, naquele documento, da posição de cada match encontrado;

### Parametric and Zone indexes

Há documentos constituídos por mais parâmetros (como data, autores, título) e por isso houve necessidade de criar:

- `parametric indexes`: inverted indexes criados por cada parâmetro. assim conseguimos obter queries mais complexas, como por exemplo "todos os documentos do autor Z que contêm a palavra Y";
- `zone indexes`: é o mesmo conceito, mas aplicado a uma porção arbitrária do documento, como por exemplo ao abstract ou à conclusão de um paper;

## Ranking Retrieval

Num sistema grande o modelo booleano não é a melhor opção e houve necessidade de ordenar os documentos por ordem de relevância. Essa relevância pode, por exemplo, ser o resultado da média ponderada de matches em cada zona ou field.

O próximo passo da evolução do sistema é não considerar apenas a presença do token mas sim a sua frequência:

- `Term Frequency` (TF) - analisa a frequência num determinado documento. Só isto não é suficiente pois, por exemplo, num conjunto de documentos que são dissertações, a palavra "dissertação" não vai ter relevância para a pesquisa mas vai aparecer muitas vezes;

- `Document Frequency` (DF) - o número de documentos que contêm o termo;

- `Inverse Document Frequency` (IDF) - calculado com log(N / document frequency), sendo N o número total de documentos. Assim, quanto mais raro é o termo nos documentos em geral, maior será este índice;

### TF-IDF

Resulta da multiplicação de TF (a frequência de um dado termo num documento) com IDF (o inverso da frequência desse termo nos documentos em geral). Assim é de prever que:

- o valor será grande para um termo T que apareça muitas vezes num documento e num pequeno número de documentos;
- o valor será pequeno para um termo T que apareça poucas vezes num documento ou que apareça em muitos documentos;
- praticamente nulo se o termo T aparecer em todos os documentos;

## IR Models

Os modelos têm o objectivo de produzir uma **função de ranking**, ou seja, dar score a cada documento dado uma query. Assim, é necessário:

- Representar os documentos, Di;
- Representar as queries, Qi;
- Representar a função de ranking, R(Di, Qi);

### Vector Space Model

É uma representação de um conjunto de documentos, onde cada eixo é na realidade um termo. A similiaridade entre dois documentos é baseada no cosseno do ângulo formado entre os dois vetores, desta forma compensando os efeitos do comprimento do documento. <br>
As queries também são representadas num espaço de dimensão N, onde N é o número de termos na query. Assim, as queries são vistas como pequenos documentos. O resultado das queries são os X documentos mais próximos segundo a similiaridade do cosseno entre os respectivos vectores. 

### Language Models

Um documento é acertado para uma dada query se o Document Model for capaz de gerar essa query. Para uma dada query, os documentos são ordenados por relevância baseado na probabilidade do documento gerá-la, P(q | Md).

- A soma das probabilidades de uma sequência de termos é 1
- Se considerarmos os termos independentes (`unigram`), a probabilidade de uma sequência de termos é a multiplicação da probabilidade do aparecimento de cada termo;
- Se considerarmos `bigrams`, aí a probabilidade será computada aos pares, a cada termo associa-se a probabilidade do seu anterior;

Assim, podem ser usadas para reconhecer línguas, correções de escrita e traduções. Exemplo:

> D1: Portugal eyes political balance in presidential election <br>
> D2: After Portuguese elections, Spain braces for elections <br>
> Q: Portugal Election <br>
> P(Q|D1) = P(portugal|Md1) x P(election|Md1) = 1/7 x 1/7 = 0.0204 <br>
> P(Q|D2) = P(portugal|Md2) x P(election|Md2) = 1/7 x 2/7 = 0.0408 <br>

## Information Retrieval in Web

A Web lança desafios em termos de distribuição (pois não é centralizada), tamanho e qualidade dos dados, assim como a diversidade das necessidades e a sua relevância. Assim, os métodos de acesso a esta informação foi classificados em dois grupos:

- `Full-text index search engines`: usam keys e inverted indexes para o ranking dos documentos;
- `Directories/Taxonomies`: navegam a partir de uma hierarquia estabelecida, através de uma categorização manual, que não é escalável, tem um alto custo e é sensível a ambiguidades;

A Web pode ser modelada em termos de um grafo, onde páginas apontam para outras páginas. Há links para outras páginas (out-links, anchor texts) e links para recursos dentro da mesma página (in-links, o `in-degree`).

### Web Spam

As search engines devem ser resistentes a alta manipulação, para que não coloquem spam como documentos rankeados no topo das pesquisas. Para manipular os resultados:

- `Cloaking / Camuflagem`: se a searching engine é `crawler`, então apresenta um conteúdo qualquer, senão apresenta SPAM;

### User information needs

Podem ser agrupadas em três partes principais:

- `Information queries`: informação geral sobre um tópico, não há apenas um sítio único de fonte relevante de informação, pelo que os utilizadores aglutinam informações de vários sites;
- `Navigational queries`: procurar a home page de uma entidade singular, as expectativas dos utilizadores são encontrar um recurso específico;
- `Transactional queries`: como comprar um produto, download de um ficheiro, fazer uma reserva num hotel;

### Web Crawling

É o processo pelo qual as páginas web são coletadas da internet, tendo como objectivo encontrar de forma simples e rápida a maior quantidade de páginas web. Um crawler tem de providenciar robustez ao encontrar problemas, como conteúdo não esperado. Também deve executar numa perspectiva escalável e eficiente, encontrando páginas de qualidade e cujo reload depende da frequência de atualização da página. 

#### Politeness

- Deve utilizar os recursos disponíveis para obter a coleção de dados;
- Não pode fazer overload de pedidos HTTP, ou seja, o crawler deve esperar um delay entre duas requests sucessivas. Caso não o faça pode ser banido segundo as políticas dos hosting providers;
- Deve obedecer ao protocolo de exclusão de robots (*robots.txt*);

#### Robots Exclusion Protocol

- `Server-wide exclusion`: indica os diretórios que não devem ser explorados;
- `Page-wide exclusions`: através de meta-tags no HTML, como noindex, nofollow;
- `Cache exclusions`: para não mostrarem ao utilizador uma cópia da cache local da página;

#### Run

- O Crawler começa com um conjunto de `seed pages`, e estas apontam para vários outros documentos/páginas. O crawler acaba quando o critério de paragem é atingido ou quando quando o update/refresh policy foi atingido.
- A duplicação de páginas ou partes de páginas podem ser evitadas comparando partes de documentos;

### Web Ranking

É a parte mais complexa e importante de uma search engine. Além de avaliar a relevância dos documentos, há que identificar a qualidade dos conteúdos e coletá-los, assim como evitar spam. Para isso há `Ranking Signals` de três tipos principais:

- `Content signals`: relacionado ao texto e considera a semântica HTML (headings, sections, likes);
- `Structural signals`: relacionado à estrutura de links da web, pode ser textual (anchor text) ou relacionado aos links (números);
- `Usage signals`: relacionado ao feedback dado pelos utilizadores, como clicks, localização geográfica, stack de tecnologia, tempo... ;

Os `Ranking Signals` também podem ser distinguidos de acordo com outras dimensões:

- `User dependent`: dependem das características do utilizador;
- `Query dependent`: dependem das queries usadas;
- `Document dependent`: dependem de um único documento;
- `Collection dependent`: dependem da informação da coleção completa;

As características de cada signal vão impactar a sua computação. Essa computação muitas vezes é feita com Machine Learning, para medir os pesos de cada um dos componentes. 

#### Linked-based signals

Assume-se que quanto mais hyperlinks apontam para uma página, mais popular esta é. Existem dois tipos de algoritmos:

#### 1. `PageRank`:

O PageRank de um nó do grafo da WEB é um valor entre 0 e 1. É a probabilidades de, num surf aleatório e infinito, o crawler passar por aquele nó.

##### 2. `HITS`:

Conhecido como Hyperlink Induced Topic Search, que é um algoritmo `query dependent`. Começa com um conjunto de respostas (ou seja, páginas que contém keywords), e computa dois scores por página:

- páginas que têm várias a apontar para elas são `authorities`;
- páginas que apontam para várias outras são `hubs`;

## Leaning to Rank

Através de Machine Learning. O training set consiste num conjunto de queries, o conjunto de documentos e os julgamentos de relevância. A modelação dos processos podem ser feita através de:

- `Pointwise approach`, encontra a relevância de cada documento, tratando o problema como se fosse de regressão;
- `Pairwise approach`, encontra a relevância entre dois documentos, tratando o problema como se fosse de classificação;
- `Listwise approach`, encontra uma lista de relevâncias de documentos para cada query. É o contém melhor performance e mais próximo dos métodos tradicionais de Information Retrieval;

## Neural Information Retrieval

Aceitam texto de queries sem tratamento e documentos como input e representa-os como vectores. A sua performance é proporcional à quantidade de dados consumidos.

`BERT`, ou Bidirectional Encoder Representations from Transformers, são modelos de linguagem pré-treinados construídos num *transformer architecture*. As Neural Networks são usadas de dois modos distintos:

- A construir **ranking functions** usando **relevance signals**;
- A aprender representações abstratas de documentos e queries para capturar a sua relevância;

Palavras que ocorrem nos mesmos contextos têm tendência a ter significados semelhantes, pelo que usar `word embeddings` é uma opção válida que:

- tem um custo baixo a nível de dimensão;
- são normalmente vectores numerais e densos;
- a computação de semelhança pode ser feita com os métodos tradicionais;

`Transformers` são *neural networks* que são desenhadas para explicitamente terem em conta o contexto de uma arbitrária sequência de palavras num texto. Estes métodos usam um **soft match**, como assemelhar o singular do plural, sinónimos, query expansion, semelhança semântica, entre outras.