import affect_ai
import pytest, random
import pandas, string
from collections import Counter
# words: foo, bar, baz, goo, car, caz, hoo, dar, daz, ioo, ear, eaz, loo, far, faz; corpora: happiness 1, satisfaction 2, elation 2, 3
lotsa_words = []
for word in range(1000):
    new_word = ''
    for j in range(3):
        new_word += random.choice(string.letters)
    if new_word in lotsa_words:
        not_good = True
        while not_good:
            new_word = ''
            for j in range(3):
                new_word += random.choice(string.letters)
            if new_word not in lotsa_words:
                not_good = False
    lotsa_words.append(new_word)
words = ['foo', 'bar', 'baz', 'goo', 'car', 'caz', 'hoo', 'dar', 'daz', 'ioo', 'ear', 'eaz', 'loo', 'far', 'faz']
corpora = ['happiness 1', 'satisfaction 2', 'elation 2', 'elation 3']
vocab_dict = {}
weights = {}
for word in lotsa_words:
    vocab_dict[word] = random.choice(corpora)
for corpus in corpora:
    weights[corpus] = random.random()
input_frame = pandas.DataFrame.from_dict(vocab_dict.items())
# print input_frame
sample = str()
for word in range(len(corpora)):
    sample += random.choice(lotsa_words)
    if word < len(corpora)-1:
        sample += ' '

ai = affect_ai.affect_AI()

# Test that an affect_AI object gets created correctly
def test_creation():
    # We create an affect_ai object with some parameters
    # We make sure those parameters do what they should within the object
    # assert ai.vocab_size == 15
    # assert ai.primary_size == 3
    assert ai.vocab == {}
    assert ai.corpora == {}
    pass
# Test that an affect_AI object can be trained, and builds vocabulary correctly
def test_training():
    # We try to pass in corpora to the affect_ai object we created earlier
    # We make sure its internal objects change as they should
    ai.train(input_frame, weights)
    assert len(ai.vocab) == len(lotsa_words)
    assert len(ai.weights) == len(weights)
    pass
# Test that an affect_AI object correctly scores samples
def test_scoring():
    # We have the affect_ai score a sample of words containing some of its trained words
    # We compare the scored result to what we know it should be
    ai.train(input_frame, weights)
    scored_corpora = Counter()
    final_scores = {}
    print 'sample.split:',sample.split(' ')
    for word in sample.split(' '):
        # print 'this is word: ', word, 'this is the corpus we add:', vocab_dict[word]
        scored_corpora.update([vocab_dict[word]])
    for corpus in scored_corpora:
        # print 'this is corpus: ', corpus
        final_scores[corpus] = scored_corpora[corpus] * weights[corpus]

    test_scores = ai.score(sample)
    print 'this is test_scores:',test_scores
    for corpus in test_scores:
        # corpus_parts = corpus.split(' ')
        # corpus_symbol = corpus_parts[0][0] + '-' + corpus_parts[1]
        print 'corpus in test_scores'
        score_key = ai.corpora.keys()[ai.corpora.values().index(corpus)]
        print final_scores[score_key]
        print test_scores[corpus]
        assert final_scores[score_key] == test_scores[corpus]
    pass
