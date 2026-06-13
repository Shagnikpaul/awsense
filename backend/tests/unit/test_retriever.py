from unittest.mock import patch, MagicMock
import numpy as np

from src.retriever import Retriever


@patch("src.retriever.faiss.read_index")
@patch("src.retriever.pickle.load")
@patch("builtins.open", new_callable=MagicMock)
@patch("src.retriever.requests.post")
def test_get_embedding(
    mock_post,
    mock_open,
    mock_pickle,
    mock_faiss,
):
    # Mock vector store loading
    mock_pickle.return_value = {
        "documents": [],
        "sources": [],
    }

    # Mock HF API response
    mock_response = MagicMock()

    mock_response.json.return_value = [[0.1, 0.2, 0.3]]

    mock_post.return_value = mock_response

    retriever = Retriever()

    embedding = retriever.get_embedding("What is S3?")

    assert isinstance(embedding, np.ndarray)

    assert embedding.shape == (1, 3)

    mock_post.assert_called_once()
