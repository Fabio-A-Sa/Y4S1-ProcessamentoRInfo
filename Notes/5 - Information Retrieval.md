# Information Retrieval

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

