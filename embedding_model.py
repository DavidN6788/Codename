from sense2vec import Sense2Vec
import yaml
import gensim
import re

def load_config(config_file):
    """Load and parse the config yaml file.

    config_file: The path to the config file
    RETURNS (Dict): The config as key value pairs
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

class EmbeddingModel():
    def __init__(self):
        self._config = load_config('config.yaml')
        self._vocab_size = self._config['hyperparameters']['vocab_size']
        # Check which embedding model to use
        if self._config['parameters']['embedding_model'] == 'word2vec':
            file_path = self._config['model_paths']['word2vec_model']['file_path']
            self._embedding_model = Word2VecModel(file_path, self._vocab_size)
        elif self._config['parameters']['embedding_model'] == 'sense2vec':
            file_path = self._config['model_paths']['sense2vec_model']['file_path']
            self._embedding_model = Sense2VecModel(file_path)

    def get_model(self):
        """Retrieves the model for a given word embedding

        RETURNS((Word2Vec/Sense2Vec)Model): the embedding model
        """
        return self._embedding_model.get_model()

    def get_vocab(self):
        """Retrieves a list of singular words of size vocab_size

        RETURNS(list): list of words
        """
        return self._embedding_model.get_vocab(self._vocab_size)

    def similarity(self, word1, word2):
        """
        Calculates semantic similarity between two words using cosine similarity.

        word1, word2(str): The two words to compute the semantic score
        RETURNS(float): The similarity score
        """
        return self._embedding_model.calc_similarity(word1, word2)

    def most_similar_words(self, word, topn):
        """
        Retrieves the top n most similar words for a given word

        word(str): The word to find the most other similar words
        topn(int): the number of top similar words to retrieve

        RETURNS(list): most similar words
        """
        return self._embedding_model.most_similar_words(word, topn)

class Word2VecModel():
    def __init__(self, file_path, vocab_size):
        """
        Initialize the pretrained Word2Vec embedding model Object

        file_path(str): the corpus to train the Word2Vec model

        RETURNS(Word2VecModel): The newly constructed object
        """
        self._vocab_size = vocab_size
        self._word_2_vec_model = gensim.models.KeyedVectors.load_word2vec_format(file_path, binary=True, limit=self._vocab_size)

    def get_model(self):
        return self._word_2_vec_model

    def get_vocab(self, vocab_size):
        vocab = []
        word_list = self._word_2_vec_model.index_to_key[:vocab_size]
        for term in word_list:
            # Convert to lower case
            curr_word = term.lower()
            # Check if word is a singular word and not already in vocab
            if re.match(r"^\w+$", curr_word) and curr_word not in vocab and "_" not in curr_word:
                vocab.append(curr_word)
        return vocab

    def calc_similarity(self, word1, word2):
        return self._word_2_vec_model.similarity(word1, word2)

    def most_similar_words(self, word, n):
        similar_word_tuple = self._word_2_vec_model.similar_by_word(word, topn=n)
        similar_word_list = [i[0] for i in similar_word_tuple]
        return similar_word_list

class Sense2VecModel():
    def __init__(self, file_path):
        """
        Initialize the pretrained Sense2Vec embedding model Object

        file_path(str): the corpus to train the Sense2Vec model

        RETURNS(Sense2VecModel): The newly constructed object
        """
        self._sense2vec_model = Sense2Vec().from_disk(file_path)

    def get_model(self):
        return self._sense2vec_model

    def get_vocab(self, vocab_size):
        vocab = []
        word_and_senses = []
        word_list = [word for word in self._sense2vec_model.keys()][:vocab_size]
        for term in word_list:
            # Split word and senses
            parts = term.split('|')
            curr_word = term.split('|')[0].lower()
            # Check if word is a singular word and not already in vocab
            if re.match(r"^\w+$", curr_word) and curr_word not in vocab and "_" not in curr_word:
                vocab.append(curr_word)
                word_and_senses.append(curr_word + '|' + parts[1])
        return vocab, word_and_senses

    def calc_similarity(self, word1, word2):
        return self._sense2vec_model.similarity(word1, word2)

    def most_similar_words(self, word, topn):
        most_similar = []
        word_and_senses = []
        similar_word_list = [i[0] for i in self._sense2vec_model.most_similar(word, n=topn)]
        for term in similar_word_list:
            if term is None:
                continue
            # Split word and senses
            parts = term.split('|')
            curr_word = term.split('|')[0]
            # Exclude words that include base forms
            if curr_word in word or word in curr_word:
                continue
            # Check if word is a singular word and not already in vocab
            if re.match(r"^\w+$", curr_word) and curr_word not in most_similar and "_" not in curr_word:
                most_similar.append(curr_word)
                word_and_senses.append(curr_word + '|' + parts[1])
        return most_similar, word_and_senses
