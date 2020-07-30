#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

# %%
#Se crea una serie con las comunas que se deseea explorar

comuna=["Providencia, RM (Metropolitana)","Santiago, RM (Metropolitana)","Ñuñoa, RM (Metropolitana)","La Reina, RM (Metropolitana)","Las Condes, RM (Metropolitana)"]

df_final=[]
for n in comuna:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(3)
    driver.get("https://www.portalinmobiliario.com") #Cargamos la página principal

    #Buscamos el boton para seleccionar, luego seleccionamos "arriendos" o "venta"
    driver.find_element_by_id('operations-dropdown').find_element_by_class_name('searchbox-dropdown__content').click()
    #driver.find_element_by_css_selector('li[data-id="arriendo"]').click()
    driver.find_element_by_css_selector('li[data-id="venta"]').click() #Aca debes cambiar por arriendo o venta

    #Buscamos el cuadro de texto para ingresar la comuna
    where = driver.find_element_by_class_name('searchbox-autocomplete__field')
    where.clear()
    where.send_keys(n) #esto desplega una lista de autocompletado con sugerencias
    driver.find_element_by_css_selector('li.searchbox-autocomplete-list__item').click() #seleccionamos la primera opcion (que será la que escribimos)
    driver.find_element_by_id('search-submit').click() #Buscar

    #Ahora con la busqueda cargada extraemos 100 resultados

    nb=[]


    while len(nb) < 100: #hasta que el DF tenga mínimo 100 elementos.
        elems = driver.find_elements_by_class_name("results-item") # el contenedor de los resultados.
        for e in elems:
            try:
                titulo=e.find_element_by_tag_name("h2.item_subtitle").text
                direccion=e.find_elements_by_tag_name("span")
                info=e.find_element_by_tag_name("div.item__attrs").text
                superficie=info.split("|")[0]
                dormitorios=info.split("|")[1]
                baños=info.split("|")[2]
                link=e.find_element_by_css_selector('a.item__info-link').get_attribute("href")
                precio=e.find_element_by_tag_name("div.price__container").text
                nb.append({"Precio":precio,"Direccion":direccion[2].text,"Superficie":superficie,"Dormitorios":dormitorios,"Baños":baños,"Link":link})

            except:
                print("Error")
                
        driver.find_element_by_css_selector('.andes-pagination__button--next').click() #vamos a la siguiente página.

    driver.close()
    df = pd.DataFrame(nb)
    df = df[:100]
    df.sample(1)
    df["Comuna"] = str(n)
    df["Valor UF"]=0
    df["Valor Pesos"]=0
    #Los valores vienen mixtos por lo que se debe serparar por Pesos y otro por UFs
    for j in range (len(df)):
        l=int(j+1)
        x=int(df["Precio"][j:l].str.find("UF "))
        df["Valor UF"][j]=df["Precio"][j][x:]
        y=int(df["Precio"][j:l].str.find("$ "))
        df["Valor Pesos"][j]=df["Precio"][j][y:]

    if len(df_final)>0:
        df_final=pd.concat([df, df_final], ignore_index=True)
    else: 
        df_final=df.copy()

#Lo puedes ordenar por Valor UF o por Precio en pesos, debes recordar que el que no tenga ese tipo de valor sera igual a 0

df_final=df_final.sort_values(by=["Valor UF"]).reset_index(drop=True)
df_final=df_final.sort_values(by=["Valor Pesos"]).reset_index(drop=True)

archivo="tu_archivo.csv"

df_final.to_csv(archivo,index=False,sep=";")

#Listo consigue el mejor precio
    
