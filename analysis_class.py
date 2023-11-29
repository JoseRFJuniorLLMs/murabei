from pandas import read_csv, pivot_table, merge

def clean_data(df, var_name):
    """Substitui vírgulas por pontos e converte para numérico."""
    df[var_name] = df[var_name].str.replace(',', '.').astype(float)
    return df

def process_school_data():
    """Carrega, pivota e mescla dados de escolas."""
    school_df = read_csv('cat_school_data.csv', delimiter=';')
    cat_schools = school_df.pivot(index="school", columns='variable', values="value").reset_index()
    num_schools = school_df.pivot(index="school", columns='variable', values="value").reset_index()
    return merge(cat_schools, num_schools, on='school')

def process_student_data():
    """Carrega, pivota e mescla dados de estudantes."""
    student_df = read_csv('cat_student_data.csv', delimiter=';')
    cat_students = student_df.pivot_table(
        index=['school', 'student'], columns='variable', values="value", aggfunc='first').reset_index()
    num_students = student_df.pivot_table(
        index=['school', 'student'], columns='variable', values="value", aggfunc='first').reset_index()
    return merge(cat_students, num_students, on=['school', 'student'])

def main():
    schools_df = process_school_data()
    students_df = process_student_data()

    # Limpar dados do exame para evitar erros
    # Substituindo vírgulas por pontos para permitir a conversão para numérico
    schools_df['normexam'] = clean_data(schools_df, 'normexam')
    students_df['normexam'] = clean_data(students_df, 'normexam')

    # Agrupar os dados por gênero da escola e tipo, e calcular a média do exame normalizado
    resultados_por_tipo = merge(schools_df, students_df, on='school').groupby(['schgend', 'type'])[
        'normexam'].mean().reset_index()

    # Imprimindo os resultados
    print(resultados_por_tipo)

    # Salvando os resultados em um arquivo CSV
    resultados_por_tipo.to_csv("resultado.csv", index=False)

main()
