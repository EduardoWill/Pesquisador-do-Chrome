from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

pesquisa = input("Digite a pesquisa: ")

# Configuração do Chrome
service = Service('C:/Users/eduar/Desktop/Aula2/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Acessa o Google
driver.get("https://www.google.com")

# Localiza a barra de pesquisa e envia o texto
campo = driver.find_element(By.CLASS_NAME, 'gLFyf')
campo.send_keys(pesquisa)
campo.send_keys(Keys.ENTER)

# Clica no botão "Ferramentas" e obtém o número de resultados
extras = driver.find_element(By.ID, 'hdtb-tls')
extras.click()

# Tenta capturar o número de resultados
resultado = driver.find_element(By.XPATH, "//div[@id='result-stats']")
texto_resultado = resultado.text
numero_resultado = texto_resultado.split("Aproximadamente ")[1].split(" resultados")[0]
numero_resultado = float(numero_resultado.replace('.', ''))
maximo_paginas = numero_resultado / 10
buscador_paginas = input("%s páginas encontradas, até qual página deseja ir? " % (maximo_paginas))

# Navega entre as páginas do Google
pagina_atual = 0
start = 10
lista_resultado=[]
while pagina_atual <= int(buscador_paginas): 
    # Coleta os resultados de cada página
    divs = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']")
    for div in divs:
        try:
            nome = div.find_element(By.TAG_NAME, "span")
            link = div.find_element(By.TAG_NAME, "a")
            resultado = "%s; %s" % (nome.text, link.get_attribute("href"))
            print(resultado)
            lista_resultado.append(resultado)

        except:
            continue  # Ignora elementos sem título ou link
        #troca de página
        next_button = driver.find_element(By.ID, "pnnext")
        next_button.click()
        time.sleep(2)  # Aguarda carregamento da página
        pagina_atual += 1
with open("resultado.txt","w") as arquivo:
    for resultado in lista_resultado:
        arquivo.write("%s\n"% resultado)
    arquivo.close()
print("%s resultados encontrados no Google e salvos no arquivo resultado.txt" % len(lista_resultado)) 
        

input("Pressione Enter para fechar o navegador...")
driver.quit()
