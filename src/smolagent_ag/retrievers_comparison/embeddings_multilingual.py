import numpy as np
from sentence_transformers import SentenceTransformer

# Load multilingual model
model = SentenceTransformer("LaBSE")

# Get embeddings for texts in different languages
english_embedding = model.encode("This is an example text in English")
polish_embedding = model.encode("To jest przykładowy tekst po polsku")

# Calculate similarity
similarity = np.dot(english_embedding, polish_embedding) / (
    np.linalg.norm(english_embedding) * np.linalg.norm(polish_embedding)
)

print(f"Similarity score: {similarity}")
# If similarity > threshold (e.g., 0.75), consider texts similar
"""
In this example, the similarity score is 0.8792815, which is considered high.
Nevertheless, the texts are exactly the same, so the similarity score should be 1.
The lost of similary is due to the translation of the text from English to Polish.
"""
