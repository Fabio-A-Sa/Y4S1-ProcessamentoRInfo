# Exam

## 0 - Topics

- [1. Introduction](#1---introduction)
- [2. Data colection](#2---data-colection)
- [3. Data preparation](#3---data-preparation)
- [4. Data processing](#4---data-processing)
- [5. Information Retrieval](#5---information-retrieval)
- [6. Query Processing](#6---query-processing)
- [7. Entity-Oriented Seach](#7---entity-oriented-search)
- [8. Search Interfaces](#8---search-interfaces)
- [9. Project](#9---project)

## 1 - Introduction

- Information retrieval é diferente de data retrieval porque não se rege com base em exact matching e os resultados são ordenados por relevância;
- Google search é um "ad hoc" search, busca independente para necessidade isolada. Depois também existem as searches: Vertical, Enterprise e Desktop;

## 2 - Data colection

- Data (factos por observação direta), metadata e information (data processada, organizada e estruturada);
- Life cycle: ocorrência, transmissão, processamento, manipulação, utilização;
- Extract-transform-load, ETL mais antiga, ELT melhor porque permite trabalho paralelo, muito usado com dados column-oriented;
- OSEMN: obtain, scrub, explore, model, interpret;
- Serialização em XML/JSON é mais usado mas carece de suporte para imagens (binários), Binary serialização é mais rápida, mas menos visual;

## 3 - Data preparation

- Cleaning, transformation, normalization, síntese, integration, reduction, selection;
- Binning ou Discretization: transforma um valor contínuo em categórico;
- Integration: combinar dados de diferentes fontes;
- Data filtering é determinística, sampling não-determinística;
- Data pipelines: reliable, scalable, maintenable;
- DFD (Data Flow Diagrams): squares para entidades externas, rounded rectangles para processos, arrows, open-ended rectanges for data-stores;

## 4 - Data processing

- Data models: relational, document, graph, triple store;
- Document para quando as relações entre entidades são raras, graph para mapear relações frequentes;

## 5 - Information Retrieval

- Tokenization, POS (Parts-of-speech), NER (Named entity recognization), syntatic analysis, Stemming (jumping -> jump), Lemmatization (better -> good);
- Rule based para identificar entidades, statistical para inferir novos tokens;
- Lucene (indexing, searching, ranking) e Solr usa Lucene com scalability, REST API, interface, faceting, hightlightling, autocomplete);
- Faceting, para arranjar os resultados em categorias e cores para store da informação dos documentos indexados;
- Analysers (texto inicial -> token streams), são para indexing e querying, são constituídos por um Tokenizer (character streams -> token objects) e vários Filters (modificam tokens);
- Standard, DisMax e eDisMax são Query Parsers. Os últimos permitem erros de sintaxe e complexidade nas queries;
- Eficácia (encontrar correcto), eficácia (encontrar rápido);
- Precision, Recall, F-measure (2PR/(P+R)), Precision-Recall Curves, P@K, MAP. Com P@K descobrimos AvP e com AvP descobrimos MAP;
- Full inverted indexes, { word: [document index, quantity, [indexes]] };
- Parametric indexes (por atributo, como nome, date, authors), e zone indexes (por zonas documento, como abstract, introduction);
- TF (term frequency in the document), DF (document frequency in all system documents), IDF = log(N / DF), TF-IDF = TF * IDF;
- Boolean Model, Vector Space Model (cada termo é um axis, os documentos e queries são vectores, cosseno exprime a similiaridade entre os documentos, ranking em função do ângulo que separa cada query e os documentos);
- Unigrams or Bigrams, documentos são ranqueados de acordo com a probabilidade de gerarem a query;
- Information needs: informational, navigational, transactional;
- Signals, como query-(in)dependent, document-based (HTML), colection-based (links), user-based (clicks). Há três tipos: content (semântica do HTML), structural (links), usage (clicks);
- Exclusões de crawlers: server-wide (diretórios), page-wide (metatags no html), cache (obriga a mostrar conteúdo sempre novo, não pode ir buscar da cache);
- Link-based signals: PageRank (probabilidade em random walk), HITS (Hyperlink Induced Topic Search, computação de authorities e hubs);
- Learn to Rank usa Signals (hand-crafted), enquanto Neural Information Retrieval usa a query e o documento como inputs;
- BERT (Bidirectional Encoder Representations from Transformers), word embeddings para capturar semântica em vectores condensados;
- Learn To Rank pode ser pointwise (relevância em cada documento), pairwise (relevância entre documentos, comparação), listwise (ranking de uma lista);

## 6 - Query Processing

- Algoritmos document-at-time e term-at-time;
- Otimizações: skip pointers (evita ver toda a inverted index list), conjunctive (faz skip a documentos que não possuam todos os termos da query), ignorar termos de alta frequência em term-at-time, ignorar documentos no fim das listas de relevância em document-at-time, caching;
- Rocchio algorithm: modifica a query de acordo com a query inicial e o feedback relevante/não relevante dos documentos (calcula o centróide);
- Relevance feedback: explicit, pseudo (afina a query com os primeiros K documentos), implicit (através de clicks e links);

## 7 - Entity-Oriented Search

- Entities com id, nome, tipo, atributos, relationships;
- Organizadas em semi-estruturada (wikipédia) ou estruturada (RDF - Resource Description Framework, KB - Knowledge Database);
- Tipos de necessidades de informação / queries: keyword (normal), structured (SQL), keyword++ (site:up.pt), natural, zero (proative search system);
- RDF Statement: (subject, predicate, object);
- Entity linking: para relacionar entidades a texto. Etapas: mention detection, candidate selection, disambiguation;

## 8 - Search Interfaces

- Interface: input, control, informational, personalization;
- Evaluation: IR Style (factos), Empirical (heuristics, IPC), Analytics (estima, low-cost);

## 9 - Project

- 4 datasets;
- Data preparation: empty/null values, uniform text, range normalization, date formats;
- Data normalization: remover reviews com menos de X palavras, remover hoteis com menos de X reviews;
- Data relational model: location - hotel - review;
- Document: hotel (name, location, average rate), review (date, text, rate);
- Information needs: best hotels near center of London, breakfast or room service, accessibility, vegetarian/vegan food;
- Indexing: ascii, lowercase, sinónimos, stopwords;
- 