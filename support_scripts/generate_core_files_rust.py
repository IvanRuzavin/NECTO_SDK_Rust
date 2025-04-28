import os, re, subprocess, json

def clean_define_value(value):
    return value.replace('(', '').replace(')', '').replace('UL', '').replace('U', '').replace('~', '!').replace('uint16_t', '')

def extract_defines(lines):
    defines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("#define"):
            # Handle multi-line defines
            while line.endswith("\\"):
                next_line = lines[i + 1].strip()
                line = line[:-1].rstrip() + " " + next_line
                i += 1

            # Now remove comment if any
            line_no_comment = line.split('/', 1)[0].strip()

            tokens = line_no_comment.split(maxsplit=2)
            if len(tokens) >= 3 and '?' not in line_no_comment:
                name = tokens[1]
                value = tokens[2]

                # Remove parentheses and UL, U suffixes cleanly
                value = clean_define_value(value)

                defines.append((name, value))

        i += 1

    return defines

def extract_enum(lines, enum_name):
    enum_lines = []
    inside_enum = False

    for line in lines:
        if "typedef enum" in line:
            inside_enum = True
            continue
        if inside_enum:
            if "}" in line:
                inside_enum = False
                break
            line = line.strip()
            if not line:
                continue
            if line.endswith(','):
                line = line[:-1]
            if '=' in line and '===' not in line:
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip()
                if "/" in val:
                    val = val.split('/')[0].strip().replace(',', '')
                enum_lines.append((key, val))
    return enum_lines

def extract_structs(lines):
    structs = []
    inside_struct = False
    current_struct = []
    struct_name = ""

    i = 0
    while i < len(lines):
        line = lines[i]
        if 'typedef struct' in line:
            inside_struct = True
            current_struct = []
            i += 1
            continue

        if inside_struct:
            if '}' in line.strip():
                # Check if struct name is on the same line
                parts = line.strip().split('}')
                if len(parts) > 1 and parts[1].strip() != '':
                    struct_name = parts[1].replace(';', '').strip()
                else:
                    # Struct name is on the next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        struct_name = next_line.replace(';', '').strip()
                        i += 1  # Skip the name line
                    else:
                        struct_name = ""

                structs.append((struct_name, current_struct))
                inside_struct = False
            else:
                current_struct.append(line.rstrip())

        i += 1

    return structs

def parse_struct_field(line):
    line = line.strip()
    if not line or line.startswith('/*') or ('*/' in line and '/*' not in line):
        return None
    line = line.split('/')[0].strip()  # Remove inline comments
    tokens = line.split()
    if len(tokens) < 2:
        return None

    name_part = tokens[-1]
    if name_part == ';':
        name_part = tokens[-2]

    array_size = None
    if '[' in name_part:
        match = re.match(r'(\w+)\[(.+)\]', name_part)
        if match:
            name, array_size = match.groups()
            array_size = array_size.strip().replace(' ', '')  # Remove inner spaces if needed
        else:
            name = name_part.replace(';', '').replace('*', '')
            array_size = None
    else:
        name = name_part.replace(';', '').replace('*', '')

    rust_type = "u32"  # everything __IO uint32_t -> u32 for now

    return (name, rust_type, array_size)

def rust_struct(struct_name, fields):
    output = []
    output.append("#[repr(C)]")
    output.append(f"pub struct {struct_name} {{")
    for field in fields:
        parsed = parse_struct_field(field)
        if parsed:
            name, rust_type, array_size = parsed
            if array_size:
                output.append(f"    pub {name}: [{rust_type}; {array_size}],")
            else:
                output.append(f"    pub {name}: {rust_type},")
    output.append("}\n")
    return "\n".join(output)

def format_with_rustfmt(file_path):
    try:
        subprocess.run(["rustfmt", file_path], check=True)
        print(f"Formatted {file_path} with rustfmt")
    except FileNotFoundError:
        print("Warning: rustfmt not found. Install it with `rustup component add rustfmt`")
    except subprocess.CalledProcessError:
        print(f"rustfmt failed formatting {file_path}")

def main():
    input_path = 'd:/work_mikroe/GIT/core_packages/ARM/gcc_clang/def'
    output_dir = 'gui/core_packages/def/stm'
    input_path_linker = 'd:/work_mikroe/GIT/core_packages/ARM/gcc_clang/linker_scripts/stm'
    output_dir_linker = 'gui/core_packages/memory/stm'

    # for root, _, files in os.walk(input_path):
    #     for file in files:
    #         dest_json = {}
    #         if '.json' in file and 'STM32' in file:
    #             if not os.path.exists(os.path.join('gui/core_packages/def', file)):
    #                 with open(os.path.join(root, file), 'r', encoding='utf-8') as source_json_file:
    #                     source_json = json.load(source_json_file)
    #                 if 'config_registers' in source_json:
    #                     if source_json['config_registers'] != []:
    #                         dest_json['config_registers'] = source_json['config_registers']
    #                         dest_json['core'] = source_json['core'].replace('M0EF', 'M0')
    #                         dest_json['delay_src_path'] = source_json['delay_src_path'].replace('m0ef', 'm0')
    #                         dest_json['clock'] = str(source_json['clock'])
    #                         with open(os.path.join('gui/core_packages/def', file), 'w') as dest_json_file:
    #                             json.dump(dest_json, dest_json_file, indent=4)
    #                         print(f'Created {os.path.join("gui/core_packages/def", file)}')
    #         if file.endswith('.h') and 'STM32' in root:
    #             mcu_name = root.split(os.sep)[-1]
    #             dest_dir = os.path.join(output_dir, mcu_name)
    #             os.makedirs(dest_dir, exist_ok=True)

    #             with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
    #                 lines = f.readlines()
    #                 for idx, line in enumerate(lines):
    #                     if "Exported_macros" in line or 'INSTANCE' in line:
    #                         lines = lines[:idx]
    #                         break

    #             defines = extract_defines(lines)
    #             enum_items = extract_enum(lines, "IRQn_Type")
    #             structs = extract_structs(lines)

    #             rust_lines = []

    #             if enum_items:
    #                 rust_lines.append("#[repr(i32)]")
    #                 rust_lines.append("pub enum IRQn_Type {")
    #                 max_key_len = max(len(name) for name, _ in enum_items)
    #                 for name, val in enum_items:
    #                     spacing = ' ' * (max_key_len - len(name))
    #                     rust_lines.append(f"    {name}{spacing}= {val},")
    #                 rust_lines.append("}\n")

    #             for struct_name, fields in structs:
    #                 rust_lines.append(rust_struct(struct_name, fields))
                    
    #             if defines:
    #                 max_key_len = max(len(name) for name, _ in defines)
    #                 for name, value in defines:
    #                     spacing = ' ' * (max_key_len - len(name) + 1)
    #                     rust_lines.append(f"pub const {name}{spacing}:u32 = {value};")

    #                 rust_lines.append("")  # Blank line after defines

    #             output_path = os.path.join(dest_dir, 'lib.rs')
    #             with open(output_path, 'w', encoding='utf-8') as f:
    #                 f.write('\n'.join(rust_lines))

    #             print(f"Created {output_path}")
    #             format_with_rustfmt(output_path)

    os.makedirs(output_dir_linker, exist_ok=True)
    for file in os.listdir(input_path_linker):
        memory_lines = ""
        memory_found = False
        with open(os.path.join(input_path_linker, file), 'r') as source_linker:
            lines = source_linker.readlines()
            for line in lines:
                if 'MEMORY' in line:
                    memory_found = True
                if memory_found:
                    memory_lines += line
                    if '}' in line:
                        break
        if memory_lines != '':
            os.makedirs(os.path.join(output_dir_linker, file.replace('.ld', '').upper()), exist_ok=True)
            with open(os.path.join(output_dir_linker, file.replace('.ld', ''), 'memory.x'), 'w') as memory_file:
                memory_file.write(f'/* memory.x - Linker script for the {file.replace('.ld', '').upper()} */\n{memory_lines}')
            print(f'Created memory.x for {file.replace('.ld', '').upper()}')
        else:
            print(f'NO MEMORY FOUND FOR {file.replace('.ld', '').upper()}')

if __name__ == '__main__':
    main()