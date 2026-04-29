def process_data(data_list):
    """
    处理数据列表，去除空值并全部大写
    """
    cleaned_data = [str(item).upper() for item in data_list if item]
    return cleaned_data

def format_output(data):
    return " | ".join(data)

if __name__ == "__main__":
    sample = ["apple", "", "banana", None, "cherry"]
    result = process_data(sample)
    print(format_output(result))
