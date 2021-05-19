
# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
try:
	from nettoolkit import IO, STR, DB
except:
	raise Exception("Mandatory Module Import Failed: nettoolkit")
from os import path, remove
from shutil import copyfile
from random import randint

# ------------------------------------------------------------------------------
# VARS
# ------------------------------------------------------------------------------
COMPARATORS = ("%2==", "%2!=", " ==", " !=", ">=", "<=", "> ", "< ")
MATH_OPERATORS = ('+', '-', '*', '/')

# ------------------------------------------------------------------------------
# Definitions
# ------------------------------------------------------------------------------

def random_text_file(source_file, temporary_prefix):
	"""create a duplicate of source text file with random name using 
	given prefix.
	"""
	while True:
		random_number = randint(1, 1000000)
		random_file_name = temporary_prefix + str(random_number) + '.txt'
		temporary_template = random_file_name
		try:
			with open(temporary_template) as f: pass
		except:
			break
	try:
		copyfile(source_file, temporary_template)
	except FileNotFoundError as e:
		return None
	return temporary_template

def section_type(line, section_starter):
	"""checks section type in line and returns tuple with details 
	if section is conditional/repeatative
	"""
	if line[:section_starter['no_repeat_len']] == section_starter['no_repeat']:
		repeat = 0
		line = line[section_starter['no_repeat_len']:].lstrip()
	elif line[:section_starter['repeat_len']] == section_starter['repeat']:
		repeat = 1
		line = line[section_starter['repeat_len']:].lstrip()
	else:
		return (line, -1)
	return (line, repeat)

def replace_var_candidates(temporary_template, var_db_df, var_db_columns):
	"""update find/replace pairs in temporary template file """
	for x in var_db_df.iterrows():
		_find = x[1][var_db_columns['find']]
		_replace = x[1][var_db_columns['replace']]
		if _find.strip() != '':
			IO.update(temporary_template, _find, _replace)

# ---------------------------------------------------------------------------- #
# class : Config Generator
# ---------------------------------------------------------------------------- #
class ConfGen():
	"""create an object by providing necessary details to generate configuration
	Mandatory inputs are
	template_file, db
	"""

	def __init__(self, 
		db=None,
		template_file=None,
		output_file='output.txt',
		# below 4* depricated ones, next version to be removed
		xls_db=None,
		xls_db_sheet='tables',
		var_db=None,
		var_db_sheet='var',
		#
		confGen_minimal=False,
		#
		find_column_name='FIND',
		replace_column_name='REPLACE',
		repeat_starter="REPEAT EACH",
		repeat_stopper="REPEAT STOP",
		condition_starter="GOAHEAD FOR",
		condition_stopper="GOAHEAD END",
		nested_section_var_identifier="PARENT",
		):
		self.db = db
		self.template_file = template_file
		self.output_file = output_file
		self.xls_db = xls_db
		self.xls_db_sheet = xls_db_sheet
		self.var_db = var_db
		self.var_db_sheet = var_db_sheet
		self.confGen_minimal = confGen_minimal
		self.var_db_columns = { 'find': find_column_name,
			'replace': replace_column_name}
		self.section_starter = {
			"no_repeat": condition_starter,
			"no_repeat_len": len(condition_starter),
			"repeat": repeat_starter,
			"repeat_len": len(repeat_starter),
			}
		self.section_stopper = {
			"no_repeat": condition_stopper, 
			"no_repeat_len": len(condition_stopper),
			"repeat": repeat_stopper,
			"repeat_len": len(repeat_stopper),
			}
		self.nested_section_var_identifier = nested_section_var_identifier
		self.input_check()

	def input_check(self):
		"""check for mandatory inputs """
		if not self.template_file:
			raise Exception("Missing Mandatory argument 'template_file'")
		if not (self.db or (self.xls_db and self.var_db)):
			raise Exception("Missing Mandatory argument(s) database ex: 'db' ")

	def is_template_variried(self):
		"""sequence of checks to validate the conditions consistency in template.
		Errored Template can cause infinite loop in execution.
		raises exception if any error or returns True
		"""
		self.template_file_type_check()
		self.template_conditions_count_check()
		self.template_nesting_condition_check()
		return True

	def template_file_type_check(self):
		"""template check step 1. File type verification (.txt) """
		if self.template_file.endswith(".txt"): return True
		raise ValueError("Invalid Template Provided, should be a .txt file.")

	def template_conditions_count_check(self):
		"""template check step 2. count of conditions and condition closures
		matching
		"""
		s = ''
		goahead = {self.section_starter['no_repeat']: 0, 
				self.section_stopper['no_repeat']: 0,}
		repeatfor = {self.section_starter['repeat']: 0, 
					self.section_stopper['repeat']: 0,}
		with open(self.template_file, 'r') as f:
			rf = f.read()
			for k, v in goahead.items(): goahead[k] = rf.count(k)
			for k, v in repeatfor.items(): repeatfor[k] = rf.count(k)
		bg = goahead[self.section_starter['no_repeat']]
		eg = goahead[self.section_stopper['no_repeat']]
		br = repeatfor[self.section_starter['repeat']]
		er = repeatfor[self.section_stopper['repeat']]
		if bg != eg or br != er: s += f'Descrepencies found in template file: <{self.template_file}>\n'
		if bg != eg: s += f"\tGOAHEAD conditions : begins {bg} v/s ends {eg}\n"
		if br != er: s += f"\tREPEAT conditions : begins {br} v/s ends {er}\n\n"
		if s: raise ValueError(s)

	def template_nesting_condition_check(self):
		"""template check step 3. nested conditions closure check to avoid 
		infinite loop
		"""
		conditions = []
		with open(self.template_file, 'r') as f: rf = f.readlines()
		for i, line in enumerate(rf):
			if line.lstrip().startswith(self.section_starter['no_repeat']):
				conditions.append(self.section_starter['no_repeat'])
			elif line.lstrip().startswith(self.section_starter['repeat']):
				conditions.append(self.section_starter['repeat'])
			elif line.lstrip().startswith(self.section_stopper['no_repeat']):
				try:
					if conditions.pop() != self.section_starter['no_repeat']:
						raise ValueError(f"Conditions Nesting Error at line {i}")
				except IndexError:
					raise ValueError(f"Conditions Nesting Error at line {i}")
			elif line.lstrip().startswith(self.section_stopper['repeat']):
				try:
					if conditions.pop() != self.section_starter['repeat']:
						raise ValueError(f"Conditions Nesting Error at line {i}")
				except IndexError:
					raise ValueError(f"Conditions Nesting Error at line {i}")
			else: continue
		if len(conditions) > 0: raise ValueError(f"Conditions Nesting Error")
		return True


	# old depricated func/ to be delete in next version
	def deprication_warning(self):
		print("\n#### WARNING ####\nUsage of ",
			"xls_db, xls_db_sheet, var_db, var_db_sheet getting depricated\n",
			"Please use argument 'db' instead as",
			"a single excel file containing 'tables' and 'var' sheets.\n",
			"Next version will be removed with [separate excel sheet entries]\n"
			)
		try:
			self.tables_df = DB.read_excel(self.xls_db, sheet=self.xls_db_sheet)
			self.var_df = DB.read_excel(self.var_db, sheet=self.var_db_sheet)
			return {'var':self.var_df , 'tables': self.tables_df}
		except:
			raise Exception(f"One of Database argument error: ",
				f"{self.xls_db}/{self.xls_db_sheet}",
				f"{self.var_db}/{self.var_db_sheet}",
				)

	def generate(self):
		"""Check Template consistency and start execution to generate config
		"""
		# TEMPLATE VERIFICATION
		if not self.is_template_variried(): 
			raise Exception("Template Not Varified")
		print("Template Verified\nconfiguration generation is in progress, please wait...")

		# STEP 1. INITIALIZE OBJECT
		rd = Read(self.section_starter, self.section_stopper, self.var_db_columns)
		#####################################################
		if self.db:
			dataframes = rd.database(self.db)
		else:	
			# depricated way, to be remove in next version
			dataframes = self.deprication_warning()
			rd.dataframes_depricated(dataframes)
		#####################################################
		tmp_template = rd.template(self.template_file)
		print("Input Read.. OK")


		# STEP 2. START REPLICATING CONFIG 
		rpl = Replicate(rd.section_dict, dataframes, self.confGen_minimal)
		rpl.nested_section_var_identifier = self.nested_section_var_identifier
		rpl.start()

		print("ConfGen.. OK")
		# STEP 3. WRITE OUTPUT AND CLEANUP
		IO.to_file(self.output_file, '')
		IO.add_to_file(self.output_file, rpl.output)
		remove(tmp_template)
		print(f"Write Config to File.. {self.output_file} OK")


# -----------------------------------------------------------------------------
# class: READ [ READ DATA / TEMPLATE ]
# -----------------------------------------------------------------------------

class Read():

	def __init__(self,
		section_starter, 
		section_stopper,
		var_db_columns,
		):
		self.section_starter = section_starter
		self.section_stopper = section_stopper
		self.var_db_columns = var_db_columns
		self.section_list = []
		self.section_dict = {
			'logic_line': None,
			'repeat': None,
			'filtered_df' : None,
			'section_list' : self.section_list,
			}

	# ----------------------
	# PART 1 : READ DATABASE
	# ----------------------
	def database(self, xls_db):
		return self.dataframes(xls_db)

	def dataframes(self, xls_db):
		"""read Excel sheets and store it in Dictionary """
		self.tables_df = DB.read_excel(file=xls_db, sheet='tables')
		self.var_df = DB.read_excel(file=xls_db, sheet='var')
		return {'var':self.var_df , 'tables': self.tables_df}

	def dataframes_depricated(self, dataframes):
		"""Depricated way of reading sheets. To be Remove in next version
		"""
		self.tables_df = dataframes['tables']
		self.var_df = dataframes['var']

	#-----------------------
	# PART 2 : READ TEMPLATE
	#-----------------------

	def template(self, template_file):
		text_config = random_text_file(template_file, "temp_template_")
		replace_var_candidates(text_config, self.var_df, self.var_db_columns)
		self.read_temporary_template(text_config)
		return text_config

	def read_temporary_template(self, template_file):
		"""Reads provided template file, generate sections in the template """
		# ~~~~~~~~~` Start Reading Template ~~~~~~~~~~
		self.template_file = template_file
		with open(self.template_file, 'r') as f:
			while True:
				line = f.readline()
				# eof & blank
				if not line: break
				if line.strip() == '': continue

				# --------------- FULL TEMPLATE REPLACE IF REQUESTED ---------------- #
				if section_type(line, self.section_starter)[1] != -1:				#-1 : Normal Line
					_section = Section(self.template_file,
						self.section_starter,
						self.section_stopper,
						)
					_section.get(f, line)
					self.section_list.append(_section.section_dict)

				else:
					self.section_list.append(line)


# -----------------------------------------------------------------------------
# class: Section Selector  [ DATA SECTION LOGIC ]
# -----------------------------------------------------------------------------

class Section:

	def __init__(self, 
		template_name,
		section_starter, 
		section_stopper,
		):
		self.template_name = template_name
		self.section_starter = section_starter
		self.section_stopper = section_stopper
		self.section_list = []
		self.section_dict = {
			'logic_line': '',
			'repeat': None,
			'filtered_df' : None,
			'section_list' : self.section_list,
			}

	def get(self, f, logic_line):
		"""initiates the of section"""
		self.logic_line, self.repeat = section_type(logic_line.lstrip(), self.section_starter)
		self.section_dict['logic_line'] = self.logic_line
		self.section_dict['repeat'] = self.repeat
		self.read_lines(f)

	def read_lines(self, f):
		"""lines inside of a section """
		self.read_line = True
		while self.read_line:
			line = f.readline()
			section_starters = (self.section_starter['no_repeat'],  self.section_stopper['repeat'], )
			section_stoppers = (self.section_stopper['no_repeat'],  self.section_stopper['repeat'], )
			if line.strip() == '': continue
			if (line.strip()[:self.section_stopper['no_repeat_len']] == self.section_stopper['no_repeat'] or 
				line.strip()[:self.section_stopper['repeat_len']] == self.section_stopper['repeat'] 
				):
				self.read_line = False
			elif (line.strip()[:self.section_starter['no_repeat_len']] == self.section_starter['no_repeat'] or 
				line.strip()[:self.section_starter['repeat_len']] == self.section_starter['repeat'] 
				):
				_section = Section(self.template_name,
						self.section_starter,
						self.section_stopper,
						)
				_section.get(f, line)
				self.section_list.append(_section.section_dict)
			else:
				self.section_list.append(line)


# ------------------------------------------------------------------------------
# class: Replicate config [ CONFIGURATION REPLICATOR ]
# ------------------------------------------------------------------------------

class Replicate:
	"""Replicate section configs using database provided in dataframes.
	"""

	nested_section_var_identifier = "PARENT."	# only exact match is valid.

	def __init__(self, 
		section_dict,
		dataframes,
		confGen_minimal=False,
		# nested_section_var_identifier="PARENT",
		):
		self.section_dict = section_dict
		self.dataframes = dataframes
		self.confGen_minimal=confGen_minimal
		# self.nested_section_var_identifier = nested_section_var_identifier			# only exact match is valid.
		self._output = []

	@property
	def output(self): return self._output

	def start(self):
		"""Executes the replication
		"""
		if self.section_dict['logic_line']:
			logic_line = self.section_dict['logic_line']
			logic_line = self.update_condition_for_cf_var(logic_line)
			df_condition = self.logic_line_to_df_condition(logic_line)
			filtered_dataframe = self.get_section_dataframe(df_condition)
		else:
			self.section_dict['condition'] = True
		self.go_thru_section_list()

	def update_condition_for_cf_var(self, logic_line):
		"""update condition line with carried forwarded Nested Section 
		Variable value.
		-->updated condition (str)
		"""
		if not self.section_dict.get('tables_line_vars'):
			return logic_line
		for k, v in self.section_dict['tables_line_vars'].items():
			logic_line = logic_line.replace(
				'== ' + self.nested_section_var_identifier + "." +  k, 
				'== "' + v + '"')
		return logic_line

	def logic_line_to_df_condition(self, logic_line):
		"""convert condition to pandas dataframe condition
		"""
		while logic_line.find("( ") > -1:
			logic_line = logic_line.replace("( ", "(")
		while logic_line.find(" )") > -1:
			logic_line = logic_line.replace(" )", ")")
		if logic_line.find("((") > -1:
			logic_line = logic_line.replace("((", "((df['")
			i = -1
			for x in range(10):
				doubleBR_idx = logic_line.find("((")
				i = logic_line.find("(", i+1)
				if i == -1: break
				if i == doubleBR_idx: continue
				if i == doubleBR_idx+1: continue
				logic_line = logic_line[:i] + "(df['" + logic_line[i+1:]
		else:
			logic_line = logic_line.replace("(", "(df['")
		for _c in COMPARATORS:
			while logic_line.find(" " + _c) > -1:
				logic_line = logic_line.replace(" " + _c, _c)
			if logic_line.find(_c) > -1:
				logic_line = logic_line.replace(_c, "'] " + _c)
		logic_line = "df[ " + logic_line.strip() + " ]"
		logic_line = logic_line.replace(' != ""', '.notnull()')
		logic_line = logic_line.replace(' == ""', '.isnull()')
		logic_line = logic_line.replace('%2!= ""', '%2.notnull()')
		logic_line = logic_line.replace('%2== ""', '%2.isnull()')
		return logic_line

	def get_section_dataframe(self, df_condition):
		"""returns filtered dataframe for given condition"""
		try:
			df = self.dataframes['tables']
			self.section_dict['filtered_df'] = eval(df_condition)
			self.section_dict['condition'] = not self.section_dict['filtered_df'].empty
			return self.section_dict['filtered_df']
		except:
			print(f"Error in Template condition\n{df_condition}")
			raise Exception()

	def go_thru_section_list(self):
		"""Entry point for sections """
		if self.section_dict['logic_line'] is None:
			self.initial_Go()
		else:
			self.replicate_for_data()

	def initial_Go(self):
		"""start parent section/i.e. file """
		tmpList = list(self.section_dict['section_list'])         # Template commands in a list
		for i, line in enumerate(tmpList):          # Go thru lines
			if isinstance(line, str):
				tmpList[i] = line

			# new section
			elif isinstance(line, dict):
				rpl = Replicate(line, self.dataframes, self.confGen_minimal)
				rpl.nested_section_var_identifier = self.nested_section_var_identifier
				rpl.start()
				tmpList[i] = rpl.output
		self._output.extend(tmpList)
		tmpList.clear()                    # clear list for next iteration

	def replicate_for_data(self):
		"""Go thru each line of data (data frame), and update configs in that 
		section
		"""
		rows = max(self.section_dict['filtered_df'].count())
		for row in range(rows):
			self.update_config_section(row)
			if not self.section_dict['repeat']: break
			if self.confGen_minimal: break

	def get_table_line_vars(self, RowData):
		"""data dictionary for a single row """
		tables_line_vars = {}
		for header in RowData.keys():           # Go thru columns
			try:
				if RowData[header] == 'nan': continue
				if RowData[header] == False: continue
				if int(RowData[header]) == RowData[header]:
					cell_value = str(int(RowData[header]))
				else:
					cell_value = str(RowData[header])
			except:
				cell_value = str(RowData[header])
			tables_line_vars[header] = cell_value
		return tables_line_vars

	def update_config_section(self, row):
		"""Add config with updates for given one row"""
		tmpList = list(self.section_dict['section_list'])         # Template commands in a list
		RowData = self.section_dict['filtered_df'].iloc[row]
		tables_line_vars = self.get_table_line_vars(RowData)

		for i, line in enumerate(tmpList):          # Go thru lines
			if isinstance(line, str):
				if not self.confGen_minimal: 
					for header in RowData.keys():           # Go thru columns						

						if not STR.found(line, header): continue
						if RowData[header] == 'nan': RowData[header] = ''
						if RowData[header] == False: RowData[header] = ''
						line = self.updated_line(line, RowData, header)
				tmpList[i] = line
			elif isinstance(line, dict):
				line['tables_line_vars'] = tables_line_vars
				rpl = Replicate(line, self.dataframes, self.confGen_minimal)
				rpl.nested_section_var_identifier = self.nested_section_var_identifier
				rpl.start()
				tmpList[i] = rpl.output

		# append updated line|tmpList to _output
		self._output.extend(tmpList)
		tmpList.clear()                    # clear list for next iteration

	def updated_line(self, line, RowData, header):
		try:
			if int(RowData[header]) == RowData[header]:
				line = line.replace(header, str(int(RowData[header])))
			else:
				line = line.replace(header, str(RowData[header]))
		except:
			line = line.replace(header, str(RowData[header]))
		return line

# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
	pass
# ---------------------------------------------------------------------------- #
	# # -------- provide inputs
	# db = "data.xlsx"
	# template = "template.txt"
	# output = "output.txt"

	# # -------- ConfGen 
	# cfg = ConfGen(
	# 		template_file=template,	# template
	# 		output_file=output,		# output filename ( default: output.txt)

	# 		db=db,					# database

	# 		# # depricated way of providing database details
	# 		# xls_db=db,
	# 		# xls_db_sheet='tables',
	# 		# var_db=db,
	# 		# var_db_sheet='var',

	# 		#
	# 		# confGen_minimal=True,	# execution of var sheet replacement only.( default: False)
	# 		#
	# 		find_column_name="FIND",
	# 		replace_column_name="REPLACE",
	# 		#
	# 		condition_starter="GOAHEAD FOR",
	# 		condition_stopper="GOAHEAD END",
	# 		repeat_starter   ="REPEAT EACH",
	# 		repeat_stopper   ="REPEAT STOP",
	# 		#
	# 		nested_section_var_identifier= "PARENT"

	# 	)
	# cfg.generate()
# ---------------------------------------------------------------------------- #

