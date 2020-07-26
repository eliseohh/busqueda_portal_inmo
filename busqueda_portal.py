#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

# %%
comuna=["Providencia, RM (Metropolitana)","Santiago, RM (Metropolitana)","Ñuñoa, RM (Metropolitana)","San Miguel, RM (Metropolitana)","Independencia, RM (Metropolitana)"]
df_final=[]
for n in comuna:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(3)
    driver.get("https://www.portalinmobiliario.com") #Cargamos la página principal

    #Buscamos el boton para seleccionar, luego seleccionamos "arriendos"
    driver.find_element_by_id('operations-dropdown').find_element_by_class_name('searchbox-dropdown__content').click()
    #driver.find_element_by_css_selector('li[data-id="arriendo"]').click()
    driver.find_element_by_css_selector('li[data-id="venta"]').click()

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

df_final=df_final.sort_values(by=["Valor UF"]).reset_index(drop=True)
    

# %%
#df_final=df_final.sort_values(by=["Valor UF"]).reset_index(drop=True)
df_final=df_final.sort_values(by=["Valor UF"]).reset_index(drop=True)
df_final
# %%
#X=int(df_final["Precio"][0:1].str.find("UF "))
#df_final["Precio"][0][6:]
df_final["Valor Pesos"]=0
for j in range (len(df_final)):
        l=int(j+1)
        x=int(df_final["Precio"][j:l].str.find("UF "))
        df_final["Valor UF"][j]=df_final["Precio"][j][x:]
        y=int(df_final["Precio"][j:l].str.find("$ "))
        df_final["Valor Pesos"][j]=df_final["Precio"][j][y:]

df_final=df_final.sort_values(by=["Valor UF"]).reset_index(drop=True)
df_final

# %%
df_final.to_csv("portal_comunas.csv",index=False,sep=";")

# %%
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(3)
driver.get("https://www.portalinmobiliario.com") #Cargamos la página principal

#Buscamos el boton para seleccionar, luego seleccionamos "arriendos"
driver.find_element_by_id('operations-dropdown').find_element_by_class_name('searchbox-dropdown__content').click()
driver.find_element_by_css_selector('li[data-id="arriendo"]').click()

#Buscamos el cuadro de texto para ingresar la comuna
where = driver.find_element_by_class_name('searchbox-autocomplete__field')
where.clear()
where.send_keys("Santiago, RM (Metropolitana)") #esto desplega una lista de autocompletado con sugerencias
driver.find_element_by_css_selector('li.searchbox-autocomplete-list__item').click() #seleccionamos la primera opcion (que será la que escribimos)
driver.find_element_by_id('search-submit').click() #Buscar



#Ahora con la busqueda cargada extraemos 100 resultados

nb=[]


while len(nb) < 2: #hasta que el DF tenga mínimo 100 elementos.
    elems = driver.find_elements_by_class_name("results-item") # el contenedor de los resultados.
    for e in elems:
        try:
            print(e.find_element_by_css_selector('a.item__info-link').get_attribute("href"))
            #print(e.driver.find_element_by_partial_link_text("https://www.portalinmobiliario.com/venta/").text) #MLC522440361 > div.item__info-container > div > div > a.item__info-link
            titulo=e.find_element_by_tag_name("h2.item_subtitle").text
            direccion=e.find_elements_by_tag_name("span")
            info=e.find_element_by_tag_name("div.item__attrs").text
            superficie=info.split("|")[0]
            dormitorios=info.split("|")[1]
            baños=info.split("|")[2]
            precio=e.find_element_by_tag_name("div.price__container").text
            nb.append({"Precio":precio,"Direccion":direccion[2].text,"Superficie":superficie,"Dormitorios":dormitorios,"Baños":baños})
        except:
            print("Error")
            break
            
    driver.find_element_by_css_selector('.andes-pagination__button--next').click() #vamos a la siguiente página.

#df = pd.DataFrame(nb)
#df = df[:100]
driver.close()

# %%
