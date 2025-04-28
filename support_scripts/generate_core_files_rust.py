import os, shutil, json

for root, _, files in os.walk('d:/work_mikroe/GIT/core_packages/ARM/gcc_clang/def'):
    for file in files:
        dest_json = {}
        if '.json' in file and 'STM32' in file:
            if not os.path.exists(os.path.join('gui/core_packages/def', file)):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as source_json_file:
                    source_json = json.load(source_json_file)
                if 'config_registers' in source_json:
                    if source_json['config_registers'] != []:
                        dest_json['config_registers'] = source_json['config_registers']
                        dest_json['core'] = source_json['core'].replace('M0EF', 'M0')
                        dest_json['delay_src_path'] = source_json['delay_src_path'].replace('m0ef', 'm0')
                        dest_json['clock'] = str(source_json['clock'])
                        with open(os.path.join('gui/core_packages/def', file), 'w') as dest_json_file:
                            json.dump(dest_json, dest_json_file, indent=4)
                        print(f'Created {os.path.join("gui/core_packages/def", file)}')

        if '.h' in file and 'STM32' in root:
            start_writing = False
            mcu_name = root.split(os.sep)[-1]
            source_header_lines = []
            rust_lines = []
            if not os.path.exists(os.path.join('gui/core_packages/def/stm', mcu_name, file)):
                with open(os.path.join(root, file), 'r') as source_header_file:
                    source_header_lines = source_header_file.readlines()
                os.makedirs(os.path.join('gui/core_packages/def/stm', mcu_name), exist_ok=True)

                temp_lines = []
                for line in source_header_lines:
                    if '_BASE' in line:
                        start_writing = True
                    if 'Exported_macros' in line:
                        start_writing = False

                    if start_writing:
                        if '#define' in line and 'TypeDef' not in line and 'uint' not in line and 'Kept for legacy' not in line:
                            line = line.strip()
                            if '/*' in line:
                                main_part, comment_part = line.split('/*', 1)
                                comment = '// ' + comment_part.replace('*/', '').strip()
                            else:
                                main_part = line
                                comment = ''

                            tokens = main_part.replace('#define', '').strip().split()
                            if len(tokens) >= 2:
                                key = tokens[0]
                                value = tokens[1]
                                value = value.replace('(', '').replace(')', '').replace('UL', '').replace('U', '')
                                temp_lines.append((key, value, comment))

                # Calculate max length for alignment
                if temp_lines:
                    max_key_length = max(len(key) for key, _, _ in temp_lines)
                    for key, value, comment in temp_lines:
                        spacing = ' ' * (max_key_length - len(key) + 1)
                        rust_line = f'pub const {key}{spacing}:u32 = {value};'
                        if comment:
                            rust_line += f' {comment}'
                        rust_line += '\n'
                        rust_lines.append(rust_line)

                with open(os.path.join('gui/core_packages/def/stm', mcu_name, 'lib.rs'), 'w', encoding='utf-8') as dest_header_file:
                    dest_header_file.writelines(rust_lines)
                    print(f'Created {os.path.join("gui/core_packages/def/stm", mcu_name, "lib.rs")}')
