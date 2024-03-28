# import pandas as pd

# # 读取包含两列数据的文本文件
input_file_path = '/Users/taozui/Documents/proj/qt_interface/options/platfom.txt'
# # test_file_path = '/Users/taozui/Documents/test.txt'
output_file_path = '/Users/taozui/Documents/proj/qt_interface/options/arch_copy.py'

# with open(input_file_path, 'r') as file:
#     lines = file.readlines()

# # 使用列表推导式去除每行开头和结尾的空格
# stripped_lines = [line.strip() for line in lines]

# with open(input_file_path, 'w') as output_file:
#     output_file.write('\n'.join(stripped_lines))

# # input_file_path = '/Users/taozui/Documents/payloads_stripped.txt'

# # 以空格分隔读取文本文件
# df = pd.read_csv(input_file_path, delimiter=r'\s{2,}', header=None, names=['Column1', 'Column2','Column3'])
# # df = pd.read_csv(input_file_path, sep=r'\t', header=None, names=['Column1', 'Column2'])
# # df = pd.read_csv(test_file_path, sep='\t', header=None, names=['Column1', 'Column2'])

# # 选择其中一列数据并写入另一个文本文件
# selected_column = 'Column1'
# df[selected_column].to_csv(output_file_path, index=False, header=False, sep=' ')

# print(f"已将 {selected_column} 列数据写入 {output_file_path}")

# 读取文本文件并将数据存储到列表中
with open(input_file_path, "r") as file:
    data_list = file.read().splitlines()

# 将数据列表写入新的Python文件
# output_file_path = "output_data.py"
list_name = 'PLATFORM'
with open(output_file_path, "a") as output_file:
    output_file.write('\n' + list_name + '=' + str(data_list))

print(f"数据已成功写入到 {output_file_path} 文件中。")
