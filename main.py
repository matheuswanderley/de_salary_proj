import glassdor_scrapper as gs_basic
import pandas as pd

# Substitua o caminho abaixo pelo caminho real para o seu executável do ChromeDriver
path = '/home/matheus/science-projects/ds_salary_proj/chromedriver'

# Exemplo de uso
df = gs_basic.get_jobs('data scientist', 15, path)
print("DataFrame Shape:", df.shape)
print(df.head())