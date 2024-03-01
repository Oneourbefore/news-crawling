import tensorflow_hub as hub
import tensorflow_text

# Universal Sentence Encoder 모델 로드
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# 비교할 두 문장
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast brown fox leaps over a lazy hound."

# 문장을 임베딩하여 벡터로 변환
embeddings = embed([sentence1, sentence2])

# 두 벡터 간의 코사인 유사도 계산
similarity_score = np.inner(embeddings, embeddings)[0, 1]

print("문장 1:", sentence1)
print("문장 2:", sentence2)
print("유사도 점수:", similarity_score)
