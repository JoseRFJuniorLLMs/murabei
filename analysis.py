import pandas as pd


# Carregando os conjuntos de dados
# df_cat_school contém dados categóricos sobre as escolas
df_cat_school = pd.read_csv('cat_school_data.csv', delimiter=';')

# df_num_school contém dados numéricos sobre as escolas
df_num_school =  pd.read_csv('num_school_data.csv', delimiter=';')

# df_cat_student contém dados categóricos sobre os estudantes
df_cat_student = pd.read_csv('cat_student_data.csv', delimiter=';')

# df_num_student contém dados numéricos sobre os estudantes
df_num_student = pd.read_csv('num_student_data.csv', delimiter=';')

# Pivotando os dados categóricos das escolas para ter uma linha por escola
cat_schools = df_cat_school.pivot(index="school", columns='variable', values="value").reset_index()

# Pivotando os dados numéricos das escolas para ter uma linha por escola
num_schools = df_num_school.pivot(index="school", columns='variable', values="value").reset_index()

# Pivotando os dados categóricos dos estudantes para ter uma linha por estudante
cat_students = df_cat_student.pivot_table(index=["school","student"], columns='variable', values="value", aggfunc='first').reset_index()

# Pivotando os dados numéricos dos estudantes para ter uma linha por estudante
num_students = df_num_student.pivot_table(index=["school","student"], columns='variable', values="value", aggfunc='first').reset_index()

# Mesclando os dados categóricos e numéricos das escolas em um único DataFrame
schools = pd.merge(cat_schools, num_schools, on='school')

# Mesclando os dados categóricos e numéricos dos estudantes em um único DataFrame
students = pd.merge(cat_students, num_students, on=['school','student'])

# Mesclando os dados das escolas e dos estudantes em um único DataFrame
data = pd.merge(schools, students, on='school')

# Limpar dados do exame para evitar erros
# Substituindo vírgulas por pontos para permitir a conversão para numérico
data['normexam'] = pd.to_numeric(data['normexam'].str.replace(',', '.'), errors='coerce')

# Agrupando os dados por gênero da escola e tipo, e calculando a média do exame normalizado
resultados_por_tipo = data.groupby(['schgend', 'type'])['normexam'].mean().reset_index()

# Imprimindo os resultados
print(resultados_por_tipo)

# Salvando os resultados em um arquivo CSV
resultados_por_tipo.to_csv("resultado.csv", index=False)
