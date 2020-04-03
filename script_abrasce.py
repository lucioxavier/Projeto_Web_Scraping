#Importando as Bibliotecas importantes
from selenium import webdriver # Importar a classe WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait # Importar a classe que contém as funções e aplicar um alias
from selenium.webdriver.support import expected_conditions as EC # Importar classe para ajudar a localizar os elementos
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup as bs
from random import random

#Declarando as primeiras variáveis
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N', 
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 
            'V', 'X', 'Y', 'W', 'Z']
links = []
i = []
url = f'https://abrasce.com.br/guia-de-shoppings/?letter='
c = 1

#Criando arquivo para salvar os dados posteriormente
with open('shoppings.csv', 'w') as _file:
    _file.write('Nome_Shopping; Classe_A; Classe_B; Classe_C; Classe_D; Area_total; Area_Construida;'
                'Area_Bruta_Locavel; Telefone; Site; Endereco; Qtd_pisos; Qtd_lojas_ancora; '
                'Total_lojas; Sala_cinema; Estacionamento\n')

#Definindo funções
def carregar_url(url_):
    chrome.get(url_)
    print(f'A url foi carregada...')

def close_pop_up ():
    id_button_1 = 'onesignal-popover-cancel-button'
    close_1 = False
    c1 = 0
    while close_1 is False:
        try:
            wait.until(EC.element_to_be_clickable((By.ID, id_button_1)))
            print('Tentando fechar o Pop-Up (1)...')
        except:
            c1 += 3
            if c1 > 100:
                break
            print(f'Aguarde. Pop-Up (1) ainda não disponível... {c1}%')
        else:
            wait.until(EC.element_to_be_clickable((By.ID, id_button_1))).click()
            print('Pop-Up (1) fechado com sucesso.')
            sleep(1)
            break

def close_pop_up_2 ():
    id_button_2 = '//*[@id="modalCorona"]/div/div/button'
    close_2 = False
    c2 = 0
    while close_2 is False:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, id_button_2)))
            print('Tentando fechar o Pop-Up (2)...')
        except:
            c2 += 3
            if c2 > 100:
                break
            else:
                print(f'Aguarde. Pop-Up (2) ainda não disponível... {c2}%')
        else:
            wait.until(EC.visibility_of_element_located((By.XPATH, id_button_2))).click()
            print('Pop-Up (2) fechado com sucesso.')
            sleep(1)
            break

def carregar_mais ():
    id_button_3 = 'loadMoreShopping'
    close_3 = False
    c3 = 0
    while close_3 is False:
        try:
            wait.until(EC.text_to_be_present_in_element((By.ID, id_button_3), 'CARREGAR MAIS'))
            print('Verificando existência de nova página...')
        except:
            c3 += 1
            if c3 > 100:
                break
            else:
                print(f'Aguarde... {c3}%')
        else:
            wait.until(EC.element_to_be_clickable((By.ID, id_button_3))).click()
            print('Uma nova página foi encontrada e aberta. Aguarde carregamento...')
            c3 = 0

#Abrindo navegador
chrome = webdriver.Chrome(executable_path='C:\PYTHON\chromedriver')
wait = WebDriverWait(chrome, 1)

for letra in alphabet:
    carregar_url(f'{url}{letra}')
    close_pop_up()
    close_pop_up_2()
    carregar_mais()
    abrasce_page = bs(chrome.page_source, 'html.parser')
    boxes = abrasce_page.find_all('div', {'class': 'shopping'})
    for box in boxes:
        links.append(box.find('a').get('href'))
    for link in links:
        print(f'Carregando link {c}/{len(links)}')
        chrome.get(link)
        sleep(3)
        page = bs(chrome.page_source, 'html.parser')
        selection_1 = page.find('div', {'class': 'col-12 col-lg-7'})
        selection_2 = page.find('div', {'class': 'col-12 col-lg-5'})
        selection_3 = page.find('div', {'class': 'icons shoppings mt-4 mb-4'})
        name_shopping = selection_1.find('div', {'class': 'col-12'}).text.strip()
        classe_a = selection_1.find('span', {'id': 'mfs_perfil_a'}).text
        classe_b = selection_1.find('span', {'id': 'mfs_perfil_b'}).text
        classe_c = selection_1.find('span', {'id': 'mfs_perfil_c'}).text
        classe_d = selection_1.find('span', {'id': 'mfs_perfil_d'}).text
        area_total = selection_1.find('span', {'id': 'mfs_total'}).text
        area_construida = selection_1.find('span', {'id': 'mfs_contruida'}).text
        area_bruta_locavel = selection_1.find('span', {'id': 'mfs_bruta'}).text
        telefone = selection_2.find('span', {'id': 'mfs_fone'}).text
        site = selection_2.find('span', {'id': 'mfs_site'}).text
        endereco = selection_2.find('span', {'id': 'mfs_endereco'}).text
        qtd_pisos = selection_3.find('p', {'id': 'mfs_piso_loja'}).text
        qtd_lojas_ancora = selection_3.find('p', {'id': 'mfs_loja_ancora'}).text
        total_lojas = selection_3.find('p', {'id': 'mfs_total_lojas'}).text
        sala_cinema = selection_3.find('p', {'id': 'mfs_cinema'}).text
        estacionamento = selection_3.find('p', {'id': 'mfs_vagas'}).text
        i = [name_shopping, classe_a, classe_b, classe_c, classe_d, area_total,
                            area_construida, area_bruta_locavel, telefone, site, endereco,
                            qtd_pisos, qtd_lojas_ancora, total_lojas, sala_cinema, estacionamento]
        with open('shoppings.csv', 'a') as _file2:
            _file2.write(f'{i[0]};{i[1]};{i[2]};{i[3]};{i[4]};{i[5]};{i[6]};{i[7]};{i[8]};{i[9]};{i[10]};'
                    f'{i[11]};{i[12]};{i[13]};{i[14]};{i[15]}\n')
        c +=1
        i.clear()
    c = 1
    links.clear()
chrome.quit()
