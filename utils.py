def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def split_sample(sample_text: str, model='llama3-instruct'):
    """Separate text sample to prompt and generation"""
    if model == 'llama3-instruct':
        sep = '<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n'
        prompt, generation = sample_text.split(sep)
        prompt += sep
        return prompt, generation
    else:
        raise ValueError(f'Sample splitting into prompt and generation is not implemented for this model: {model}')
