import os
import json

from tqdm.auto import tqdm
from datasets import load_dataset

from utils import convert_to_nltk_rep
from wrapping import format_sample


VAL_SAMPLES=50
model='llama3-instruct'
include_example=True

dataset = load_dataset('yale-nlp/FOLIO',split='train')
dataset_test = load_dataset('yale-nlp/FOLIO',split='validation')

unparsed_samples_xor = []
unparsed_samples_other = []
incorrect_samples = []
correct_samples = []
for sample in tqdm(dataset):
    premises = [convert_to_nltk_rep(premise) for premise in sample['premises-FOL'].strip().split('\n') if len(premise)]
    conclusion = convert_to_nltk_rep(sample['conclusion-FOL'])
    try:
        result = evaluate(premises, conclusion)
        if result != sample['label']:
            incorrect_samples.append(sample)
        else:
            correct_samples.append(sample)
    except:
        if (''.join(premises)+conclusion).count('⊕'):
            unparsed_samples_xor.append(sample)
        else:
            unparsed_samples_other.append(sample)
        continue


train_list = []
val_list = []
for sample in correct_samples[:-VAL_SAMPLES]:
    formatted_sample = format_sample(sample, model, include_example)
    sample['text'] = formatted_sample
    train_list.append(sample)

for sample in correct_samples[-VAL_SAMPLES:]:
    formatted_sample = format_sample(sample, model, include_example)
    sample['text'] = formatted_sample
    val_list.append(sample)


test_list = []
for sample in dataset_test:
    formatted_sample = format_sample(sample)
    sample['text'] = formatted_sample
    test_list.append(sample)

shot = 1 if include_example else 0

os.makedirs(os.path.join('data', 'sft'), exist_ok=True)

with open(os.path.join('data', 'sft', f'folio_filtered_train_{model}_{shot}shot.json'), 'w') as f:
    json.dump(train_list, f)

with open(os.path.join('data', 'sft', f'folio_filtered_val_{model}_{shot}shot.json'), 'w') as f:
    json.dump(val_list, f)

with open(os.path.join('data', 'sft', f'folio_filtered_test_{model}_{shot}shot.json'), 'w') as f:
    json.dump(test_list, f)

