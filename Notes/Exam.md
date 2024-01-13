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
- 

## 6 - Query Processing



## 7 - Entity-Oriented Search



## 8 - Search Interfaces

