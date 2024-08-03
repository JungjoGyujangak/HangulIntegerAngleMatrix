import re

def parse_srt(file):
    srt_blocks = []
    block = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if re.match(r'^\d+$', line.strip()):
                if block:
                    srt_blocks.append(block)
                block = [line.strip()]
            else:
                block.append(line.strip())
        if block:
            srt_blocks.append(block)
    return srt_blocks

def format_time(seconds):

    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def split_and_emphasize(input_file, output_file):
    srt_blocks = parse_srt(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        counter = 1
        for block in srt_blocks:
            try:
                start_time, end_time = block[1].split(" --> ")
                start_time_sec = sum(x * float(t) for x, t in zip([3600, 60, 1], start_time.replace(",", ".").split(":")))
                end_time_sec = sum(x * float(t) for x, t in zip([3600, 60, 1], end_time.replace(",", ".").split(":")))
                duration = end_time_sec - start_time_sec
                has_degree_symbol = any("°" in line for line in block)
                if has_degree_symbol:
                    if len(block) > 6:
                        sixth_line = block[6]
                    else:
                        sixth_line = ""
                    
                    length_sixth_line = len(sixth_line)
                    divisions = length_sixth_line if length_sixth_line > 0 else 1
                    interval = duration / divisions

                    
                    for i in range(divisions):
                        start = start_time_sec + i * interval
                        end = start + interval
                        
                        file.write(f"{counter}\n")
                        file.write(f"{format_time(start)} --> {format_time(end)}\n")
                        char = sixth_line[i] if i < length_sixth_line else ""
                        for j, line in enumerate(block[2:]):
                            if j < 4 and char:
                                unicode_value = ord(char) - ord('가')
                                leading_consonant_index = unicode_value // 588
                                consonants = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
                                leading_consonant = consonants[leading_consonant_index]
                                double_to_single = {
                                    "ㄲ": "ㄱ", "ㄸ": "ㄷ", "ㅃ": "ㅂ", "ㅆ": "ㅅ", "ㅉ": "ㅈ",
                                    "ㄱ": "ㄱ", "ㄴ": "ㄴ", "ㄷ": "ㄷ", "ㄹ": "ㄹ", "ㅁ": "ㅁ", 
                                    "ㅂ": "ㅂ", "ㅅ": "ㅅ", "ㅇ": "ㅇ", "ㅈ": "ㅈ", "ㅊ": "ㅊ", 
                                    "ㅋ": "ㅋ", "ㅌ": "ㅌ", "ㅍ": "ㅍ", "ㅎ": "ㅎ"
                                }
                                q = double_to_single.get(leading_consonant, leading_consonant)

                                new_line = ""
                                for p in line:
                                    if p == q:
                                        new_line += char
                                    else:
                                        new_line += p
                                modified_line = new_line
                            else:
                                modified_line = line
                            file.write(f"{modified_line}\n")
                        
                        file.write("\n")
                        counter += 1
                else:
                    file.write(f"{counter}\n")
                    file.write(f"{start_time} --> {end_time}\n")
                    for line in block[2:]:
                        file.write(f"{line}\n")
                    file.write("\n")
                    counter += 1
            except Exception as e:
                print(f"Error processing block: {block} - {e}")

# Example usage with the provided file paths
input_file = '미륵.srt'
output_file = '미륵저그.srt'

# Execute the function to process the input file and generate the output file
split_and_emphasize(input_file, output_file)
