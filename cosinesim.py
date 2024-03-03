import tensorflow_hub as hub
import tensorflow_text

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast brown fox leaps over a lazy hound."

embeddings = embed([sentence1, sentence2])

# 두 벡터 간의 코사인 유사도 계산
similarity_score = np.inner(embeddings, embeddings)[0, 1]

print("문장 1:", sentence1)
print("문장 2:", sentence2)
print("유사도 점수:", similarity_score)
