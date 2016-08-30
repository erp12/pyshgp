from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

# Set path of instruction files
instructions_dir = '../instructions/'

# Lines of the resulting doc file
doc_file_lines = []

# Some .rst lines to put in the top of the resulting doc file
doc_file_lines.append(".. sidebar:: Useful Links")
doc_file_lines.append("")
doc_file_lines.append("	* `Evolutionary Parameters <Evolutionary_Parameters.html>`_")
doc_file_lines.append("	* `Instruction Set <Instructions.html>`_")
doc_file_lines.append("	* `Examples <Examples.html>`_")
doc_file_lines.append("")
doc_file_lines.append("********************")
doc_file_lines.append("Pysh Instruction Set")
doc_file_lines.append("********************")

# For each .py file in the instructions file directory
for file_name in os.listdir(instructions_dir):
	# Only look at the .py files ...
    if file_name.endswith(".py"):
    	# ... but ignore these .py files
        if file_name == "__init__.py" or file_name == "registered_instructions.py" or file_name == "input_output.py":
        	continue

        # Open the file
        with open(instructions_dir+file_name) as file:
    		lines = file.readlines()
        	# Filter out the instruction doc string lines.
        	doc_lines = filter(lambda line: line[:8] == '#<instr_', lines)

        	in_instruction = False
        	# For each doc string line
        	for l in doc_lines:
        		# if the line is a <instr_open>
        		if l[8:12] == 'open':
        			if in_instruction:
        				raise Exception("Tried to start new instruction doc while already inside instruction doc.")
        			doc_file_lines.append('')
        			in_instruction = True
        		# if the line is a <instr_name>
        		elif l[8:12] == 'name':
        			if not in_instruction:
        				raise Exception("Tried to add instruction doc name while not already inside instruction doc block.")
        			doc_file_lines.append(l[13:-1])
        			doc_file_lines.append('"' * len(l[13:-1]))
        		# if the line is a <instr_desc>
        		elif l[8:12] == 'desc':
        			if not in_instruction:
        				raise Exception("Tried to add instruction doc desc while not already inside instruction doc block.")
        			doc_file_lines.append(l[13:-1])
        		# if the line is a <instr_name>
        		elif l[8:13] == 'close':
        			if not in_instruction:
        				raise Exception("Tried to close instruction doc block while not already inside instruction doc block.")
        			in_instruction = False
        			doc_file_lines.append("")
        		# if the line is a <instr_name>
        		else:
        			raise Exception("Unknown instruction doc tag in line: " + l)

instruction_file = open('auto_instructions.rst', 'w')
for line in doc_file_lines:
	instruction_file.write("%s\n" % line)