import re
from keywords import fraud, terror, pep


def tag_double(paragraph, dct):
    global user_input

    original = re.findall(r'[^\s]+', paragraph)
    tokens = re.findall(r'[^\s]+\s[^\s]+', paragraph)


    for index, token in enumerate(tokens):
        subj = re.sub(r'[^a-z\s]', '', token.lower().rstrip('\n'))

        if subj in fraud:
            original[index*2] = f"<span style='border-radius: 5px;background-color: #fca;padding: 2px 5px;'>{original[index*2]}"
            original[index*2+1] = f"{original[index*2+1]}</span>"
            dct['fraud_count'] += 1

        if subj in pep:
            original[index*2] = f"<span style='border-radius: 5px;background-color: #fea;padding: 2px 5px;'>{original[index*2]}"
            original[index*2+1] = f"{original[index*2+1]}</span>"
            dct['pep_count'] += 1

        if subj in terror:
            original[index*2] = f"<span style='border-radius: 5px;background-color: #faa;padding: 2px 5px;'>{original[index*2]}"
            original[index*2+1] = f"{original[index*2+1]}</span>"
            dct['terror_count'] += 1


    return ' '.join(original), dct


def tag_double_offset(paragraph, dct):
    global user_input

    original = re.findall(r'[^\s]+', paragraph)
    tokens = re.findall(r'[^\s]+\s[^\s]+', ' '.join(original[1:]))

    for index, token in enumerate(tokens):
        subj = re.sub(r'[^a-z\s]', '', token.lower().rstrip('\n'))

        if subj in fraud:
            original[index*2+1] = f"<span style='border-radius: 5px;background-color: #fca;padding: 2px 5px;'>{original[index*2+1]}"
            original[index*2+2] = f"{original[index*2+2]}</span>"
            dct['fraud_count'] += 1

        if subj in pep:
            original[index*2+1] = f"<span style='border-radius: 5px;background-color: #fea;padding: 2px 5px;'>{original[index*2+1]}"
            original[index*2+2] = f"{original[index*2+2]}</span>"
            dct['pep_count'] += 1

        if subj in terror:
            original[index*2+1] = f"<span style='border-radius: 5px;background-color: #faa;padding: 2px 5px;'>{original[index*2+1]}"
            original[index*2+2] = f"{original[index*2+2]}</span>"
            dct['terror_count'] += 1

    return ' '.join(original), dct


def tag_single(paragraph, dct):
    global user_input

    original = re.findall(r'[^\s]+', paragraph)
    tokens = re.findall(r'[^\s]+', paragraph)

    for index, token in enumerate(tokens):
        subj = re.sub(r'[^a-z]', '', token.lower().rstrip('\n'))

        if subj in fraud:
            original[index] = f"<span style='border-radius: 5px;background-color: #fca;padding: 2px 5px;'>{original[index]}</span>"
            dct['fraud_count'] += 1

        if subj in pep:
            original[index] = f"<span style='border-radius: 5px;background-color: #fea;padding: 2px 5px;'>{original[index]}</span>"
            dct['pep_count'] += 1

        if subj in terror:
            original[index] = f"<span style='border-radius: 5px;background-color: #faa;padding: 2px 5px;'>{original[index]}</span>"
            dct['terror_count'] += 1

    return ' '.join(original), dct


def tag(paragraph, user_input, dct):
    text_1 = paragraph.replace(user_input, f"<span style='text-decoration:underline;font-weight:bold;'>{user_input}</span>")
    text_2, dct_2 = tag_double(text_1, dct)
    text_3, dct_3 = tag_double_offset(text_2, dct_2)
    final, dct_final = tag_single(text_3, dct_3)

    # text_3 = tag_single(text_2)

    return final, dct_final
