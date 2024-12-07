import torch
import torch.nn as nn
from transformers import BertForMaskedLM

class TextEncoder(nn.Module):
    def __init__(self):
        super(TextEncoder, self).__init__()
        
        # BertForMaskedLM�� �ҷ��ɴϴ�.
        self.text_encoder = BertForMaskedLM.from_pretrained('path/to/bert_masked_lm')
        
        # ���� ����ġ ��������
        self.embedding_weights = self.text_encoder.bert.embeddings.word_embeddings.weight.data
        
        # ���ο� �Ӻ��� �ʱ�ȭ (vocab_size ������ �ʿ��� ���)
        new_vocab_size = 28996
        old_vocab_size, embedding_dim = self.embedding_weights.shape
        
        # ���ο� �Ӻ��� �ʱ�ȭ
        if new_vocab_size < old_vocab_size:
            print(f"Resizing embedding weights from {old_vocab_size} to {new_vocab_size}")
            self.embedding_weights = self.embedding_weights[:new_vocab_size, :]
        else:
            print(f"Initializing new embedding weights for extra {new_vocab_size - old_vocab_size} tokens")
            extra_weights = torch.randn(new_vocab_size - old_vocab_size, embedding_dim) * 0.02  # �ʱ�ȭ
            self.embedding_weights = torch.cat([self.embedding_weights, extra_weights], dim=0)
        
        # ���ο� �Ӻ����� �����մϴ�.
        self.text_encoder.bert.embeddings.word_embeddings = nn.Embedding.from_pretrained(self.embedding_weights, freeze=False)
        
    def forward(self, input_ids, attention_mask=None):
        # BertForMaskedLM�� forward �Լ� ���
        outputs = self.text_encoder.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        return outputs.last_hidden_state
