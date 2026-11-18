from pathlib import Path
import json, subprocess, sys, tempfile
root = Path(__file__).resolve().parents[3]
replacements={
'cash': {'negative-reprompt':('while amount < 0:', 'while False:'), 'cents':('cents = round(amount * 100)', 'cents = int(amount * 100)'), 'minimum':('(25, 10, 5, 1)', '(10, 5, 1)'), 'remainder':('(25, 10, 5, 1)', '(25, 10, 5)'), 'final-line':('print(coins)', 'print(f"{coins} coins")')},
'readability': {'letters':("'a' <= char <= 'z' or 'A' <= char <= 'Z'", "'a' <= char <= 'z' or 'A' <= char <= 'Z' or '0' <= char <= '9'"), 'words':('words = len(text.split())', "words = len(text.replace(\"'\", ' ').split())"), 'sentences':("char in '.!?'", "char in '.'"), 'index':('grade = round(index)', 'grade = int(index)'), 'grade-labels':('print("Before Grade 1")', 'print(f"Grade {grade}")')},
'dna': {'arity':('if len(sys.argv) != 3:', 'if len(sys.argv) == 99:'), 'csv-fields':('fields = reader.fieldnames[1:]', "fields = [field for field in reader.fieldnames[1:] if field in ('AGAT', 'AATG', 'TATC')]"), 'longest-run':('return longest', 'return sequence.count(subsequence)'), 'exact-profile':('if all(int(person[field]) == counts[field] for field in fields):', 'if any(int(person[field]) == counts[field] for field in fields):'), 'no-match':("print('No match')", 'return')}}
cases={'cash':[('-1\n-0.25\n0.50\n','2\n'),('0.29\n','5\n'),('0.50\n','2\n'),('0.41\n','4\n'),('0.01\n','1\n')], 'readability': [('Green birds fly high above lakes 1234567890.\n','Grade 3\n'),("Don't stop looking around the garden.\n",'Grade 9\n'),('Bright stars! Silver moons? Lanterns shine.\n','Grade 4\n'),('Bright stars shine above the lake.\n','Grade 7\n'),('Small cats nap.\n','Before Grade 1\n')], 'dna': [('arity', 'usage'),('name,CG\nBea,1\nAda,2\n|CGCG','Ada\n'),('name,AC\nAda,3\nBea,4\n|ACACACGGAC','Ada\n'),('name,AC,GT\nBea,2,2\nAda,2,1\n|ACACGT','Ada\n'),('name,AC,GT\nAda,1,2\n|ACACGT','No match\n')]}
results={}
with tempfile.TemporaryDirectory() as temp:
 p=Path(temp); (p/'cs50.py').write_text('def get_float(prompt): return float(input())\ndef get_string(prompt): return input()\n')
 for name,mutants in replacements.items():
  source=(root/'data/assignments'/name/'reference.py').read_text()
  for mutant,(old,new) in [('reference',('',''))]+list(mutants.items()):
   code=source if mutant=='reference' else source.replace(old,new)
   if mutant!='reference': assert source.count(old)==1
   path=p/(name+'.py'); path.write_text(code)
   results[name+'.'+mutant]=[]
   for data,expected in cases[name]:
    args=[]; inp=data
    if name=='dna':
     inp=''
     if data!='arity':
      db,seq=data.split('|'); (p/'db.csv').write_text(db); (p/'seq.txt').write_text(seq); args=[str(p/'db.csv'),str(p/'seq.txt')]
    try:
     proc=subprocess.run([sys.executable,str(path),*args],input=inp,text=True,capture_output=True,timeout=3,cwd=p)
     ok=proc.returncode==0 and (('Usage:' in proc.stdout) if expected=='usage' else proc.stdout==expected)
     observed={'pass':ok,'stdout':proc.stdout,'returncode':proc.returncode,'stderr':proc.stderr[-300:]}
    except subprocess.TimeoutExpired: observed={'pass':False,'timeout':True}
    results[name+'.'+mutant].append(observed)
 print(json.dumps(results,indent=2))
