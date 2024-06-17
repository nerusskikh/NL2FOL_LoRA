from collections import Counter
from utils import reformat_fol

def evaluate(premises, conclusion):
    premises = [reformat_fol(p) for p in premises]
    conclusion = reformat_fol(conclusion)

    c = read_expr(conclusion)
    p_list = []
    for p in premises:
        p_list.append(read_expr(p))
    truth_value = prover.prove(c, p_list)
    if truth_value:
        return "True"
    else:
        neg_c = read_expr("-(" + conclusion + ")")
        negation_true = prover.prove(neg_c, p_list)
        if negation_true:
            return "False"
        else:
            return "Uncertain"


def evaluate_generation(generation, return_error_message=False):
    try:
        all_propositions = [x.replace('FOL:','').strip()
                                for x in generation.split('\n')[2:-1:2]]
                                #for x in generation.split('<EVALUATE>')[9][:-12].strip().split('\n')[1::2]]
        premises, conclusion = all_propositions[:-1], all_propositions[-1]
        return evaluate(premises, conclusion)
    except Exception as e:
        if return_error_message:
            return f"Error: {str(e)}"
        else:
            return "Error"

def metric(generations, references, error_token):
        correct = 0
        for gens, ref in zip(generations, references):
            gens = [gen for gen in gens if gen != error_token]
            if len(gens) > 0:
                majority = Counter(gens).most_common(1)[0][0]
                if majority == ref:
                    correct += 1
        return {f"accuracy (pass@1 majority)": correct / len(references)}
