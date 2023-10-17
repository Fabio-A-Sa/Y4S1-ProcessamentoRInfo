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

