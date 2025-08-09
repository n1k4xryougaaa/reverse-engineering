# Tutorial : https://youtu.be/XqPqTkX01YA?si=ubGxlY7le9WIMO9m

# -*- coding: utf-8 -*-
# Requirements:
# uncompyle6==3.7.4
# xdis==5.0.5
# Pygments==2.5.2

"""
Sebuah disassembler untuk file bytecode Python (.pyc) yang dirancang untuk Python 2.
"""
import sys
import os
import types
import re
from cStringIO import StringIO

# Pastikan script dijalankan dengan Python 2
if sys.hexversion >= 0x3000000:
    sys.exit('Sorry, Python2.x required by this script :\'(')

# Coba import semua dependensi yang diperlukan
try:
    from uncompyle6.main import decompile
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters.terminal import TerminalFormatter
    from xdis.load import load_module
    from xdis.main import disco
except ImportError as e:
    sys.exit('[Error] {} :-\\'.format(e))

__version__ = '2.0.0'
__doc__ = """
    _ _
 __| (_)___ __ _ ______
/ _` | (_-</ _` (_-<_-<
\__,_|_/__/\__,_/__/__/ """

def disass(code_obj):
    """
    Mendisassamble bytecode dari objek kode yang diberikan.

    Args:
        code_obj: Objek kode dari file .pyc yang dimuat.

    Returns:
        String yang berisi hasil disassembling dan decompiling.
    """
    # Lambda untuk menghapus komentar dari output
    remove_comments = lambda text: re.sub(re.compile("#+.*?\n"), "", text)
    
    # Gunakan StringIO untuk menangkap output
    output = StringIO()
    
    # Iterasi melalui konstanta dalam objek kode
    for const in code_obj[3].co_consts:
        # Proses hanya jika konstanta adalah objek kode
        if isinstance(const, types.CodeType):
            output.write('\n%s\n%s:\n%s' % (
                "-" * 69, 
                const.co_name, 
                " ".join(["{:02x}".format(ord(x)) for x in const.co_code])
            ))
            
            # Mendisassamble bytecode
            disco(code_obj[0], const, code_obj[1], output, code_obj[4], code_obj[2], code_obj[5])
            
            # Coba dekompilasi bytecode
            try:
                decompile(code_obj[0], const, output)
            except:
                output.write('\nFailed to decompile')
    
    return remove_comments(output.getvalue())

def main():
    """
    Fungsi utama untuk menjalankan script.
    """
    if len(sys.argv) < 2:
        sys.exit('Usage: python2 disass.py file.pyc')
    
    os.system('clear')
    print(__doc__ + __version__ + "\n")
    print('Reading byte-code from %s... ' % sys.argv[1])
    
    # Muat file .pyc
    code_obj = load_module(sys.argv[1])
    
    # Disassamble, dekompilasi, dan cetak dengan syntax highlighting
    output_text = disass(code_obj)
    highlighted_output = highlight(output_text, PythonLexer(), TerminalFormatter())
    print(highlighted_output)

if __name__ == '__main__':
    main()
