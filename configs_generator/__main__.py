from pprint import pprint
from .confGen import ConfGen

# -----------------------------------------------------------------------------
# input parser
# -----------------------------------------------------------------------------
import argparse

parser = argparse.ArgumentParser(prog='configs_generator', 
	description='Made for Networking Geeks',
	epilog="And that's how you'd use the tool",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	prefix_chars='-+/'
	)
parser.add_argument('-i', '-interactive', action='store_true', help='run command interactive mode', dest='interactive')
parser.add_argument('-t', '-template', help='Template File (text file)', dest='template_file')
parser.add_argument('-d', '-database', help='Database File (Excel file)', dest='db')
parser.add_argument('-o', '-output', help='output File (text file)', dest='output_file')
parser.add_argument('-m', '-minimal', action='store_true', help='execution of var sheet replacement only.( default: False)', dest='confGen_minimal')
parser.add_argument('-f', '-find', help='FIND column headers from "var" tab: ', default='FIND', dest='find_column_name')
parser.add_argument('-r', '-replace', help='REPLACe column headers from "var" tab: ', default='REPLACE', dest='replace_column_name')
parser.add_argument('-cs', '-condition_start', help='conditional block start identifier', default='GOAHEAD FOR', dest='condition_starter')
parser.add_argument('-ce', '-condition_end', help='conditional block end identifier', default='GOAHEAD END', dest='condition_stopper')
parser.add_argument('-rs', '-repeat_start', help='repeat block start identifier', default='REPEAT EACH', dest='repeat_starter')
parser.add_argument('-re', '-repeat_end', help='repeat block end identifier', default='REPEAT STOP',  dest='repeat_stopper')
parser.add_argument('-nv', '-nested_var', help='nested section variable identifier string', default='PARENT',  dest='nested_section_var_identifier')
args = parser.parse_args()
va = vars(args)


def optional_interactive_args(arg, arg_desc):
	_i = input(arg_desc)
	va[arg] = _i if _i else None

if va.get('interactive'):
	va['template_file'] = input("Enter Template File (text file): ")
	va['db'] = input("Enter Database File (Excel file): ")
	va['output_file'] = input("Enter output File (text file): ")

	confGen_minimal = None
	while confGen_minimal not in ("yes", "no", ""):
		confGen_minimal = input("Do you want to execution of var sheet replacement only [yes/no] .(default: no)").lower()
	va['confGen_minimal'] = True if confGen_minimal == 'yes' else False

	optional_interactive_args('find_column_name', 'change FIND column headers on database "var" tab [default: FIND]: ')
	optional_interactive_args('replace_column_name', 'change REPLACE column headers on database "var" tab [default: REPLACE]: ')
	optional_interactive_args('condition_starter', 'change conditional block start identifier in tempalte [default: GOAHEAD FOR]: ')
	optional_interactive_args('condition_stopper', 'change conditional block end identifier in tempalte [default: GOAHEAD END]: ')
	optional_interactive_args('repeat_starter', 'change repeat block start identifier in tempalte [default: REPEAT EACH]: ')
	optional_interactive_args('repeat_stopper', 'change repeat block end identifier in tempalte [default: REPEAT STOP]: ')
	optional_interactive_args('nested_section_var_identifier', 'change nested section variable identifier string  in tempalte [default: PARENT]: ')


if va.get('template_file') and va.get('db') and va.get('output_file'):
	del(va['interactive'])
	va = {k:v for k,v in va.items() if v!=None}
	print("Executing, please wait...")
	pprint(va)
	cfg = ConfGen(**va)
	cfg.generate()
else:
	print('ERROR: missing a mandatory input: ',)
	pprint(va)
