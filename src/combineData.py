repo_names = ['net','perl','v8','rust','pcre2','java','ICU','re2','python_re','pcre2_chlog','pcre_chlog']

with open('data/all_train.jsonl','w') as f:
    for name in repo_names:
        filename = 'data/' + name + "_train.jsonl"
        with open(filename, 'r') as input_file:
            x = input_file.read()
            f.write(x)

with open('data/all_test.jsonl','w') as f:
    for name in repo_names:
        filename = 'data/' + name + "_test.jsonl"
        with open(filename, 'r') as input_file:
            x = input_file.read()
            f.write(x)
            
