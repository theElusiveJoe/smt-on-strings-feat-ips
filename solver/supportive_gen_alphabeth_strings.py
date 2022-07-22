import random

strlen = 400
alpha_2 = ''.join(random.choices(['A', 'B'], weights=[1,1], k = strlen))
alpha_3 = ''.join(random.choices(['A', 'B', 'C'], weights=[1,1,0.2], k=strlen))
alpha_6 = ''.join(random.choices(['A', 'B', 'C', 'D', 'E', 'F'], weights=[1,1,1,1,1,1], k=strlen))
print(alpha_2, alpha_3, alpha_6)

with open('formula_generator/alphabet_strings.py', 'w+') as dst:
    dst.write(f'alpha_2="{alpha_2}"\n')
    dst.write(f'alpha_3="{alpha_3}"\n')
    dst.write(f'alpha_6="{alpha_6}"\n')