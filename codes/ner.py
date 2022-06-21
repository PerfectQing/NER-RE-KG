import os
import json
import numpy as np
from transformers import AutoTokenizer, AutoModelForTokenClassification, BertModel, TrainingArguments, Trainer
import transformers
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

tokenizer = AutoTokenizer.from_pretrained('/root/pgq/model_saved/StemCell')
model = AutoModelForTokenClassification.from_pretrained('/root/pgq/model_saved/StemCell')

label2id = {
    '[PAD]': 0,
    'B': 1,
    'I': 2,
    'O': 3,
    'X': 4,
    '[CLS]': 5,
    '[SEP]': 6,
}
id2label = {
    0: '[PAD]',
    1: 'B',
    2: 'I',
    3: 'O',
    4: 'X',
    5: '[CLS]',
    6: '[SEP]',
}



def predict(sent):
    tokenized_sent = tokenizer(sent)
    sent_tokens = tokenizer.convert_ids_to_tokens(tokenized_sent.input_ids)
    # print(sent_tokens)
    preds = model(torch.tensor(tokenized_sent.input_ids).unsqueeze(0)).logits.detach().numpy()
    # print(preds)
    valid_words = []
    valid_entities = []
    for idx, p in enumerate(preds[0]):
        # print(p)
        # npp = np.array(p)
        # p = list(p)
        # print(nnp)
        label = id2label[np.argmax(p)]
        # print(label)
        if label == 'B':
            valid_words.append(sent_tokens[idx])
        if label == 'I':
            if valid_words:
                if '##' in sent_tokens[idx]:
                    valid_words[-1] += sent_tokens[idx].replace('##', '')
                else:
                    valid_words.append(sent_tokens[idx])

        if '##' in sent_tokens[idx] and valid_words:
            valid_words[-1] += sent_tokens[idx].replace('##', '')
        if label == 'O':
            if valid_words:
                valid_entities.append(' '.join(valid_words))
            valid_words = []
    if valid_entities:
        valid_entities_line = ', '.join(valid_entities)
    else:
        valid_entities_line = 'No entities found.'

    return valid_entities_line
    # print(valid_entities)
    # # print(preds[0][0], len(preds[0][0]))
    
sent_sample = 'This is a very useful stem cell on our body.'
sent_sample = 'Histone deacetylase activity required for embryonic stem cell differentiation .'
predict(sent_sample)
# outputs = trainer.predict(test_dataset)



