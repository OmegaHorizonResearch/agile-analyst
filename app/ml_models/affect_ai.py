import sys
from collections import Counter
import pandas as pd
import copy

# New direction: store vocab words in a single dictionary. Keep track of corpora. At the end, when all corpora have been tallied, generate a dictionary where each key is a corpus and each value is a number between 0 and the number of corpora. During scoring, the number value for each word is put into a counter, then converted into a dictionary for final reporting.

class affect_AI:
    def __init__(self):
        # This is where we set up whatever objects we need for the hash table and dictionaries.
        """
        Params
        ------
         vocab_size: int, the total size of the vocabulary to be stored.

         secondary_dict_size: int, the maximum number of words to be stored in the second-order dictionaries.

        """

        # vocab is all the words the ai has affective associations for.
        self.vocab = {}
        # corpora maps each corpus found during training to an integer symbol. The symbol is then used internally.
        self.corpora = {}
        # weights tells us how to scale a 'hit' for each corpus, to scale and normalize somewhat for varying corpus sizes and word frequencies across all corpora.
        self.weights = {}

    def train(self, vocab, weights):
        # This is where we actually 'learn' the vocabulary and its r-emotion scores.
        # Dilemma: Do we use 400 columnns (or num columns = num corpora) or do we just have words with lists of the corpora and tiers they're in? The first is larger, but we can use column labels to facilitate some training/scoring functions more easily. The second way saves some memory, but we'd have to build a list of all the unique corpora we've encountered as we take in vocabulary.
        """
        Uses nested dictionaries to keep lookup times to a minimum. Python dictionaries are implemented with hash tables, and their overhead stays relatively low up to hundreds or thousands of members, so we try to keep each dictionary close to this number of members. Future development directions might include self-adjusting or empirically self-determined dictionary sizes and ratios, where the sizes would all be chosen to maximize lookup time while keeping to minimum complexity.

        Inputs:
            --'vocab', DataFrame. 'vocab' is a pandas DataFrame object. Contains a row for each word in the original corpus. First column is the word. Subsequent columns are filled as needed to specify r-emotion corpus and tier each word belongs to.
            --'weights', python dictionary. 'weights' is a dictionary containing scaling coefficients for each tier of each corpus. These coefficients are meant to scale any word found in a tier based on its frequency. Tiers with more words will have smaller coefficients, and tiers with fewer words will have larger coefficients.

        Outputs: None. Stores as an internal object (an attribute on 'self') an ordered dictionary of ordered dictionaries containing our words as keys in the second order dictionaries and the corpora and tiers it's part of as values in the second order dictionaries.
        """

        word_col = vocab.axes[1][0]
        vocab.sort_values(by=word_col)


        corp_num = 0
        for row in range(vocab.shape[0]):
            self.vocab[vocab.iloc[row][0]] = vocab.iloc[row][1]
        for value in Counter(self.vocab.values()):
            self.corpora[value] = corp_num
            corp_num += 1
        self.weights = weights
        self.symbolify()


    def score(self, sample):
        # This is where we take a sample and return the 400 r-emotion scores.
        """
        Inputs: Str. A string composed of any number of words, sentences, or paragraphs.

        Outputs: Dictionary. A dictionary of r-emotion symbols and 1200 floats, each float corresponding to an r-emotion value score.
        """
        # For each word in the sample, we check if it's where it should be in our hash table. If it's there, we add its contribution to the total r-emotion scores for the sample.
        scores = Counter()
        r_scores = {}
        sample = self.wordify(sample)
        for word in sample:
            # If we find a word from the sample in the vocab, then we should actually look it up.
            # TODO: Use a list comprehension to lookup only those words in the vocab.
            if word in self.vocab:
                scores.update([self.vocab[word]])

        for symbol in scores:
            # We need to multiply the score for each symbol by its weight for the corpus.
            symbol_name = self.corpora.keys()[self.corpora.values().index(symbol)]
            r_scores[symbol_name] = scores[symbol] * self.weights[symbol]

        return r_scores


    def symbolify(self):
        # This method should only be called at the end of trianing. It reduces the corpora for each word in the affect_ai's dictionary to a symbol. These symbols are generated using the 'reduce_chars' method. Each symbol is the minimum number of characters required to differentiate it from another symbol, followed by a number for each corresponding tier within the corpus.
        for word in self.vocab:
            corp = self.vocab[word]
            # If we have a list of corpus names for a word's membership, we have multiple symbols to replace.
            if type(corp) == list():
                new_corpora = []
                for corpus in corp:
                    # do the symbol replacement
                    new_corpora.append(self.corpora[corpus])
                self.vocab[word] = new_corpora
            else:
                # Do just single symbol replacement.
                self.vocab[word] = self.corpora[corp]
        new_weights = {}
        # Now, we need to replace the corpus names in 'weights' with their matching symbol.
        for corpus in self.weights.keys():
            new_weights[self.corpora[corpus]] = self.weights[corpus]
        self.weights = new_weights


    def wordify(self, sentence):
        """ wordify method takes a sentence or paragraph, as a single string, and returns a list of words with letters and numbers only.

        Inputs
            sentence: string. The string to be transformed into a list of words.
        Outputs
            words: list. A list of alphanumeric words, found separated within 'sentence' by spaces.

        """
        words = sentence.split(" ")
        words = [str().join(filter(str.isalpha, word)) for word in words]
        words = [word for word in words if word]
        return words

    # def find_index(self, query):
    #     keys = self.primary_keys
    #     if query in keys:
    #         print 'dict keys:', keys
    #         print 'dict primary keys:', self.dict.keys()
    #         return query
    #     keys.append(query)
    #     keys.sort()
    #     location = keys.index(query)
    #     index_word = keys[location-1]
    #     # print index_word
    #     return index_word
