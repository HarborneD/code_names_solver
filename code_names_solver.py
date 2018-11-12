import gensim
from gensim.models import Word2Vec
import os

model_path = "/Users/harborned/Documents/repos/molly_projects/crossword_solver/model"

model_path = os.path.join(model_path,"GoogleNews-vectors-negative300.bin")
# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)


similar_words=model.wv.most_similar(positive=['woman','king'], topn=100)  

print(similar_words)
print("")

if "castle" in model.vocab:
    print("Answer found")


#####

print(len(model.wv.vocab))

print(model.wv.vocab)

vocab_output_path = "google_dict.txt"

with open(vocab_output_path, "w") as f:
    f.write(",".join([word.encode('utf-8') for word in list(model.wv.vocab.keys())]))
