# Codenames

Codenames implementation with interactive gameplay. This repository also includes experiments to test whether Sense2Vec and Word2Vec embedding models.

## Prerequisites
- **Sense2Vec**: Look through Sense2Vec Explosion Installation and Setup to download Sense2Vec https://github.com/explosion/sense2vec?tab=readme-ov-file#pretrained-vectors
- **Gensim**: Download Gensim library. https://pypi.org/project/gensim/
- **Model**: Make sure model paths are downloaded.
- **Config**: Make sure the configuration is correct in `config.yaml`.

### Default Configuration:
```yaml
parameters:
  embedding_model: word2vec  # Choose between word2vec, sense2vec

hyperparameters:
  vocab_size: 1500000 # Default 1000000
  cosine_sim_difference: 0.35 # Default 0.35
  topn: 2500 # Default 1000

model_paths:
  word2vec_model:
    file_path: model_paths\GoogleNews-vectors-negative300.bin
  sense2vec_model:
    file_path: model_paths\s2v_old
  codename_words:
    file_path: model_paths\wordlist.txt

experiment_params:
  num_of_games: 30

## Running Codenames
- **Running Experiments**: Simply run `python experiment.py`.
- **Playing the Game Yourself**: Run `python main.py`.
