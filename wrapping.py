def format_sample(sample, model='llama3-instruct', include_example=True):
    if model=='llamacode':
        system_message = """The task is to translate each of the premises and conclusion into FOL expressions, so that the expressions can be evaluated by a theorem solver to determine whether the conclusion follows from the premises.\nExpressions should be adhere to the format of the Python NLTK package logic module."""
    elif model=='llama3-instruct':
        system_message = f"""The task is to translate each of the premises and conclusion into FOL expressions, so that the expressions can be evaluated by a theorem solver to determine whether the conclusion follows from the premises.
Expressions should be adhere to the format of the Python NLTK package logic module:
Conjunction (AND): A & B
Disjunction (OR): A | B
Implication: A -> B
Negation: -A
Universal Quantifier: all x. (proposition)
Existential Quantifier: exists x. (proposition)

Make sure that response is wrapped in EVALUATE tags."""
        if include_example:
            system_message += ''' Follow the format of the provided example. 
<EXAMPLE>
<EXAMPLE_INPUT>
<PREMISES>
Lawton Park is a neighborhood in Seattle. 
All citizens of Lawton Park use the zip code 98199. 
Tom is a citizen of Lawton Park.
Daniel uses the zip code 98199.
</PREMISES>
<CONCLUSION>
Tom is a citizen of Washington.
</CONCLUSION>
</EXAMPLE_INPUT>
<EXAMPLE_OUTPUT>
<EVALUATE>
TEXT: Lawton Park is a neighborhood in Seattle. 
FOL: NeighbourhoodIn(LawtonPark, Seattle)
TEXT: All citizens of Lawton Park use the zip code 98199. 
FOL: all x. (Residentof(x, LawtonPark) -> UseZipCode(x, NumNineEightOneNineNine))
TEXT: Tom is a citizen of Lawton Park.
FOL: ResidentOf(Tom, LawtonPark)
TEXT: Daniel uses the zip code 98199.
FOL: UseZipCode(Daniel, NumNineEightOneNineNine)
TEXT: Tom is a citizen of Washington.
FOL: ResidentOf(Tom, Washington)
</EVALUATE>
</EXAMPLE_OUTPUT>
</EXAMPLE>'''
    prompt = ("<PREMISES>\n"+sample['premises'].strip()+"\n</PREMISES>\n<CONCLUSION>\n"+sample['conclusion'].strip()+"\n</CONCLUSION>")
    premises_text = sample['premises'].strip().split('\n')
    premises_fol = [convert_to_nltk_rep(premise) for premise in sample['premises-FOL'].strip().split('\n') if len(premise)]
    conclusion_text = sample['conclusion']
    conclusion_fol = convert_to_nltk_rep(sample['conclusion-FOL'])
    parsing_output = ('\n'.join([f"TEXT: {x}\nFOL: {y}" for (x,y) in zip(premises_text, premises_fol)])
    +f'\nTEXT: {conclusion_text}\nFOL: {conclusion_fol}')
    if model=='llamacode':
        formatted_sample=f"""Source: system
{system_message}<step> Source: user

{prompt} <step> Source: assistant
Destination: user

<EVALUATE>
{parsing_output}
</EVALUATE>
"""
    elif model=='llama3-instruct':
        formatted_sample = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{{{{ {system_message} }}}}<|eot_id|><|start_header_id|>user<|end_header_id|>

{{{{ {prompt} }}}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{{{{ <EVALUATE>\n{parsing_output}\n</EVALUATE> }}}}<|eot_id|><|end_of_text|>"""
    else:
        raise RuntimeError('Prompt wrapping is not implemented for this kind of model')
    
    return formatted_sample
