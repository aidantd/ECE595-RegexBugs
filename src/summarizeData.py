import pandas as pd
import datetime

models = ['OPENAI', 'BERT']
input_file_prefix = 'data/master_outputs_'
output_file_prefix = 'data/master_results_'
repo_names = ['java','v8','python','pcre2','rust','re2','icu']


def convert_xlsx_to_df(input_file, name, model):
    # Read from xlsx file to Pandas DataFrame
    if model == 'OPENAI':
        df = pd.read_excel(
            input_file,
            sheet_name=name,
            usecols="A:D",
            names=["hash","date","message","Evolution?"])
    else:
        df = pd.read_excel(
            input_file,
            sheet_name=name,
            usecols="A:C",
            names=["message","date","Category"])
        category = df["Category"].to_list()
        for i in range(len(category)):
            if category[i].lower() == 'maintenance':
                category[i] = "N"
            elif category[i].lower() == 'evolution':
                category[i] = "Y"
            else:
                category[i] = "?"
        df["Evolution?"] = category

    return df

def convert_date_column_to_datetime_list(df: pd.DataFrame):
    dates = df['date'].to_list()
    def str2date(s):
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S%z')
    dates = [str2date(d) for d in dates]
    df['date'] = dates
    return df

def get_counts_by_year(df: pd.DataFrame):
    dates = df["date"].to_list()
    evo = df["Evolution?"].to_list()

    years = [d.year for d in dates]
    all_years = list(set(years))
    all_years.sort()
    n_years = len(all_years)

    total_all = [0]*n_years
    total_maintenance = [0]*n_years
    total_evolution = [0]*n_years
    total_unlabeled = [0]*n_years
    for y,e in zip(years, evo):
        ind = all_years.index(y)
        total_all[ind] += 1
        if e == 'Y':
            total_evolution[ind] += 1
        elif e == "N":
            total_maintenance[ind] += 1
        else:
            total_unlabeled[ind] += 1
        

    result = {'years': all_years, 
              'total changes': total_all,
              'total maintenance':total_maintenance,
              'total evolution':total_evolution,
              'total unlabeled':total_unlabeled}      
    return result

def write_to_xlsx(file, results, repo_names):
    with pd.ExcelWriter(file) as writer:
        print(f'\nSaving results to Excel file: {file}')
        for name in repo_names:
            pd.DataFrame(results[name]).to_excel(writer, sheet_name=name)
            print(f'  Saved {len(results[name]['years'])} rows to sheet "{name}"')


def main(model, repo_names):
    input_file = input_file_prefix + model + '.xlsx'
    output_file = output_file_prefix + model + '.xlsx'
    print(f'\nReading label data from file: {input_file}')
    results = dict()
    for name in repo_names:
        df = convert_xlsx_to_df(input_file, name, model)
        print(f'  Read {len(df)} rows from sheet: "{name}"')
        print('  Converting dates and summarizing data by years...',end='')
        df = convert_date_column_to_datetime_list(df)
        data = get_counts_by_year(df)
        results[name] = data
        print('Complete!')

    write_to_xlsx(output_file, results, repo_names)
    print('Script completed!\n\n')

for model in models:
    main(model, repo_names)