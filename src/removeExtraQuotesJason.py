def remove_quotes_after_message(line):
    message_index = line.find('"message": "')
    if message_index != -1:
        # Locate the first occurrence of quote after "message": "
        quote_index = line.find('"', message_index + len('"message": "'))
        # If a quote is found after "message": ", remove it
        if quote_index != -1:
            line = line[:quote_index] + line[quote_index + 1:]
    return line
def process_file(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            processed_line = remove_quotes_after_message(line)
            f_out.write(processed_line)

if __name__ == "__main__":
    input_file = "/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/uncategorizedData/re2_commits copy.jsonl"  # Replace with your input file name
    output_file = "/Users/aidan/Documents/School/Purdue/AdvancedSoftwareEngineering/Code/ECE595-RegexBugs/uncategorizedData/re2_commits copy_sorted.jsonl"  # Replace with your output file name
    process_file(input_file, output_file)
    print("Processing complete.")
