from heredity import joint_probability
people = {'Arthur': {"mother": None, "father": None},
          'Charlie': {"mother": "Molly", "father": "Arthur"},
          'Fred': {"mother": "Molly", "father": "Arthur"},
		  'Ginny': {"mother": "Molly", "father": "Arthur"},
		  'Molly': {"mother": None, "father": None},
		  'Ron': {"mother": "Molly", "father": "Arthur"}}
one_gene = {'Arthur'}
two_genes = {'Charlie'}
have_trait = {'Charlie'}
p = joint_probability(people, one_gene, two_genes, have_trait)
print(p)
# Result should be = 0.0026643247488