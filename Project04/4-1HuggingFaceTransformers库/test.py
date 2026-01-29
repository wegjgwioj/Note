from transformers import pipeline

# 第一次运行会自动下载模型和权重
# 演示情感分析管道使用

sentiment = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")  # type: ignore[arg-type]

texts = [
    "I love this library—it's so easy to use!",
    "The response time feels slow today."
]

results = sentiment(texts)#
# 输出结果
for text, res in zip(texts, results):
    print(f"{text} -> {res['label']} (score={res['score']:.3f})")
