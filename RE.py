# -*- coding: utf-8 -*-

# Import standard library modules first
import sys
from io import StringIO
import itertools
import re
from time import sleep
from string import ascii_lowercase, ascii_uppercase
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Check Python version
PY3X = sys.hexversion >= 0x3070000

__version__ = '2021.06'
__doc__ = """
*********************************************
* RE 2021.06: CZ I AM LAZY ^_^       *
* <https://youtube.com/marnocell>      *
* Type CTRL+C to stop and quit.       *
*********************************************
\x1b[?25l"""

# ---
# Helper Functions
# ---

def make_name(n):
    """
    Generate a unique name from letters.
    """
    letters = ascii_lowercase + ascii_uppercase
    letters_len = len(letters)
    name = ''
    n += 1
    while n:
        n -= 1
        name = letters[n % letters_len] + name
        n //= letters_len
    return name

def anim_text(x):
    """
    Write animated text (spinner) to the console.
    """
    sys.stdout.write(x)
    sys.stdout.flush()
    sys.stdout.write('\r')


# ---
# Main Script Logic
# ---

if __name__ == '__main__':
    # Check for correct usage
    if len(sys.argv) < 2:
        py_version = '2' if not PY3X else '3'
        sys.exit(f'Usage: python{py_version} RE.py file')

    # Display welcome message
    print(__doc__ + f'[!] Reverse {sys.argv[1]} will begin. Please wait...')

    # Check for external decompiler modules
    try:
        if PY3X:
            from decompyle3.main import decompile
        else:
            from uncompyle6.main import decompile
    except ImportError as e:
        sys.exit(f'[Error] {e} :-(')

    sleep(0.001)

    # Read the target file into a memory buffer
    file_content = open(sys.argv[1]).read()
    f = StringIO()
    f.write(file_content)
    sleep(0.001)

    # Check if the file contains 'exec' or 'eval'
    if not re.search('(exec|eval)', f.getvalue()):
        sys.exit('Sorry, exec keyword or eval function not found :(')
    
    # Prepare for the decompiler loop
    temp_var = make_name(8)
    replacements = {'exec': f'{temp_var}=', 'eval': f'{temp_var}='}
    
    # Spinner setup
    spinner_text = "Decompiling code objects.... "
    spinner_chars = "-\|/" * 11
    spinner_frames = [
        spinner_text[:i] + spinner_text[i].upper() + spinner_text[i+1:] + spinner_chars[i]
        for i in range(len(spinner_text))
    ]
    spinner_cycle = itertools.cycle(spinner_frames)
    
    # Lambda for pattern replacement
    replace_patterns = lambda patterns, text: re.compile(
        f"({'|'.join(map(re.escape, patterns.keys()))})"
    ).sub(lambda m: patterns[m.group(1)], text, count=1)

    output_filename = sys.argv[1][:-3] + '.py_dis'
    
    # Set up global and local namespaces for `exec`
    namespace = dict(locals(), **globals())
    if 'PY3X' in namespace:
        del namespace['PY3X']

    # Main loop to decompile the obfuscated layers
    while True:
        try:
            # Replace 'exec'/'eval' and execute the modified code
            current_code = replace_patterns(replacements, f.getvalue()).replace('\0', '')
            if not current_code:
                break
            
            f.truncate(0)
            
            exec(current_code, namespace, namespace)
            
            # Retrieve the decompiled code object from the temporary variable
            decompiled_obj = namespace[temp_var]
            
            anim_text(f'[!] {next(spinner_cycle)}')
            
            # Attempt to decompile, fall back to writing the object directly if it fails
            try:
                decompile(None, decompiled_obj, f)
            except Exception:
                f.write(str(decompiled_obj))

            # Stop the loop if no more obfuscation keywords are found
            if not re.search(r'(^exec|eval|module$)', f.getvalue(), flags=re.M):
                break
                
        except KeyboardInterrupt:
            sys.exit('\x1b[?25h\n')
        except Exception as e:
            sys.exit(f'\x1b[?25h{str(e)}\n')

        sleep(0.001)

    # Finalize and write the output
    final_code = f.getvalue().replace('\0', '').strip().rstrip()
    f.close()
    
    sys.stdout.write('[!] Decompiling code objects... done\n')
    anim_text(f'[!] Writing code to {output_filename}...')
    
    with open(output_filename, 'w') as out_file:
        out_file.write(final_code)
    
    sleep(0.8)
    sys.stdout.write(f'[!] Writing code to {output_filename}... done\n')
    sleep(0.3)
    
    print(f'\x1b[?25h\n{final_code}\n')
