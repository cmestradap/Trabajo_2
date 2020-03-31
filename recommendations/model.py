import pandas as pd
import pandas.io.sql as psql
import numpy as np

from database import *
from models.printer import *

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

class Model:
  def __init__(self, user):
    self.id_usuario = user.id
    self.tabla_impresoras = pd.read_sql_query("select id as id_impresora,tipo_color,wifi,escaner, precio from impresoras", con=connection)
    self.tabla_impresoras_calificadas = pd.read_sql_query('select user_id as id_user, impresora_id as id_impresora, calificacion as puntuacion from calificaciones',con=connection)

  # la siguiente funcion devuelve un dataframe con una columna 
  # por tipo_colo, columna con valores binarios de wifi y escaner
  def preparando_matriz(self, tabla_impresoras):
    df = pd.get_dummies(tabla_impresoras, columns = ["tipo_color"])
    df = pd.get_dummies(df, columns = ["wifi"])
    columnas1 = df.columns.values
    if "wifi_Yes" not in columnas1:
      df["wifi_Yes"] = 0
    if "wifi_No" in columnas1:
      df = df.drop(["wifi_No"],axis=1)

    df = pd.get_dummies(df, columns = ["escaner"])
    columnas2 = df.columns.values
    if "escaner_Yes" not in columnas2:
      df["escaner_Yes"] = 0
    if "escaner_No" in columnas2:
      df = df.drop(["escaner_No"],axis=1)

    return df

  def matriz_y_puntuacion_user(self):
    df = self.tabla_impresoras_calificadas[self.tabla_impresoras_calificadas['id_user'] == self.id_usuario]
    puntuaciones = df.loc[:, ["id_impresora","puntuacion"]]
    impresoras_calificadas = df.loc[:, "id_impresora"]
    tabla_impresoras_ratings = self.tabla_impresoras[self.tabla_impresoras["id_impresora"].isin(impresoras_calificadas)]

    return tabla_impresoras_ratings, puntuaciones

  def calcular_perfil_usuario(self, matriz, ratings_usuario):
    for i in range(1, len(matriz.columns)):
      columna = matriz.columns[i]
      #multiplicando matriz por puntuaciones
      matriz[columna]= matriz[columna].multiply(ratings_usuario.puntuacion.values)
    
    perfil = matriz.sum()

    #perfil_usuario_normalizado
    suma_puntuacion = ratings_usuario.puntuacion.sum()
    suma_perfil= perfil.iloc[1:].sum()

    wifi = perfil["wifi_Yes"]/suma_puntuacion
    escaner = perfil["escaner_Yes"]/suma_puntuacion
    precio = perfil["precio"]/suma_puntuacion

    tiposColor = perfil.drop(["precio","escaner_Yes", "wifi_Yes", "id_impresora"])
    suma_tipoColor = tiposColor.sum()
    tiposColorNormalizado = tiposColor.iloc[0:]/suma_tipoColor
    columnasTipo = tiposColor.index

    dataPrecio = pd.DataFrame({"precio": [precio]})
    
    data = pd.DataFrame(columns=columnasTipo)
    data.loc[len(data)]=tiposColorNormalizado 
    data["wifi_Yes"] = wifi
    data["escaner_Yes"] = escaner

    perfil_user_normalizado = pd.concat([dataPrecio, data], axis=1)

    return matriz, perfil, perfil_user_normalizado

  def impresoras_no_calificadas(self):
    df = self.tabla_impresoras_calificadas[self.tabla_impresoras_calificadas['id_user'] == self.id_usuario]
    impresoras_calificadas = df.loc[:, "id_impresora"]
    tabla_impresoras_not_ratings = self.tabla_impresoras[~self.tabla_impresoras.id_impresora.isin(impresoras_calificadas)]

    return tabla_impresoras_not_ratings

  def minimos_y_maximos_precio(self, tabla_impresoras_not_ratings):
    maximo = np.nanmax(tabla_impresoras_not_ratings.loc[:, "precio"].values)
    minimo = np.nanmin(tabla_impresoras_not_ratings.loc[:, "precio"].values)

    return maximo, minimo


  def normalizar_matriz_not_ratings(self, tabla_impresoras_not_ratings, maximo, minimo):
    tabla_impresoras_not_ratings['precio'] = tabla_impresoras_not_ratings.apply(lambda row : self.normalize(row['precio'],maximo, minimo), axis = 1) 
    
    return tabla_impresoras_not_ratings

  def normalize(self, x, maximo, minimo): 
      x_new = ((x - minimo)*(1-0) / (maximo - minimo)) + 0   
      return x_new   

  def agregar_columnas_perfilUserNormalizado(self, matrizNormalizada, perfilUsuarioNormalizado):
    if (len(matrizNormalizada.columns) == len(perfilUsuarioNormalizado.columns) + 1):
      perfilUserNew = perfilUsuarioNormalizado.iloc[0].values
      return perfilUserNew
    else:
      columnasMatriz = matrizNormalizada.columns.values
      columnasPerfil = perfilUsuarioNormalizado.columns.values
      perfilUserNew = []
      for i in range(1, len(columnasMatriz)):
        if (columnasMatriz[i] in columnasPerfil):
          perfilUserNew.append(perfilUsuarioNormalizado[columnasMatriz[i]].values[0])
        else: 
          perfilUserNew.append(0)
      
      return perfilUserNew

  def distaciaEuclidiana(self, x,y): 
    return np.sqrt(np.sum((x-y)**2))

  def encontrar_distancia_euclidiana(self, tablaImpresoraNoCalificadas, perfilUserNormalizado):
    listaDistanciaEuclidiana = []
    for indice, fila in tablaImpresoraNoCalificadas.iterrows():
      filaTablaImpresoras = fila.values
      filaTablaImpresoras = np.delete(filaTablaImpresoras, 0)
      dist_a_b = self.distaciaEuclidiana(perfilUserNormalizado,filaTablaImpresoras)
      listaDistanciaEuclidiana.append(dist_a_b)

    tablaImpresoraNoCalificadas["distanciaEuclidiana"] = listaDistanciaEuclidiana
    return tablaImpresoraNoCalificadas

  def mainContenido(self):
    #condicional para saber si el usuario tiene calificaciones
    tabla_impresoras2, ratings_usuario = self.matriz_y_puntuacion_user()
    ratings_usuario = ratings_usuario.sort_values('id_impresora',ascending=True)
    tabla_impresoras2 = tabla_impresoras2.sort_values('id_impresora',ascending=True)
    matriz = self.preparando_matriz(tabla_impresoras2)
  
    #perfil_usuario normalizado
    matriz_x_calificaciones, perfil, perfil_normalizado = self.calcular_perfil_usuario(matriz, ratings_usuario)
    
    columnas = perfil_normalizado.columns.values
    valores = perfil_normalizado.iloc[0].to_list()
    
    matriz_impresoras_not_ratings = self.impresoras_no_calificadas()
    matriz_impresoras_not_ratings= self.preparando_matriz(matriz_impresoras_not_ratings)
    maximo, minimo = self.minimos_y_maximos_precio(matriz_impresoras_not_ratings)
    matriz_normalizada = self.normalizar_matriz_not_ratings(matriz_impresoras_not_ratings, maximo, minimo)
    perfil_usuarioNormalizado = self.normalizar_matriz_not_ratings(perfil_normalizado, maximo, minimo)
    listaPerfil_usuarioNormalizado = self.agregar_columnas_perfilUserNormalizado(matriz_normalizada,perfil_usuarioNormalizado)  
    dataframeFinal = self.encontrar_distancia_euclidiana(matriz_normalizada,listaPerfil_usuarioNormalizado)
    dataframeFinal = dataframeFinal.sort_values('distanciaEuclidiana',ascending=True) 

    return columnas, valores, dataframeFinal

  def eval1(self):
    self.Mean = self.tabla_impresoras_calificadas.groupby(by="id_user",as_index=False)['puntuacion'].mean()
    Rating_avg = pd.merge(self.tabla_impresoras_calificadas, self.Mean, on='id_user')
    Rating_avg['adg_rating']=Rating_avg['puntuacion_x']-Rating_avg['puntuacion_y']
    self.check = pd.pivot_table(Rating_avg,values='puntuacion_x',index='id_user',columns='id_impresora')
    final = pd.pivot_table(Rating_avg,values='adg_rating',index='id_user',columns='id_impresora')
    self.final_impresoras = final.fillna(final.mean(axis=0))

    # Reemplazo de NaN por usuario Promedio
    final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)

    # similitud de usuario al reemplazar NAN por avg de usuario
    b = cosine_similarity(final_user)
    np.fill_diagonal(b, 0 )
    similarity_with_user = pd.DataFrame(b,index=final_user.index)
    similarity_with_user.columns=final_user.index

    cosine = cosine_similarity(self.final_impresoras)
    np.fill_diagonal(cosine, 0 )
    self.similarity_with_impresoras = pd.DataFrame(cosine,index=self.final_impresoras.index)
    self.similarity_with_impresoras.columns=final_user.index
    self.similarity_with_impresoras.head() 

    def find_n_neighbours(df,n):
      order = np.argsort(df.values, axis=1)[:, :n]
      df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
        .iloc[:n].index, 
        index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
      return df

    # Los 3 mejores vecinos para cada usuario
    sim_user_30_u = find_n_neighbours(similarity_with_user,3)

    # Los 3 mejores vecinos para cada usuario
    self.sim_user_30_m = find_n_neighbours(self.similarity_with_impresoras,3)

    Rating_avg = Rating_avg.astype({"id_impresora": str})
    self.Impresora_user = Rating_avg.groupby(by = 'id_user')['id_impresora'].apply(lambda x:','.join(x))

  def User_item_score1(self):
    Impresora_seen_by_user = self.check.columns[self.check[self.check.index==self.id_usuario].notna().any()].tolist()
    a = self.sim_user_30_m[self.sim_user_30_m.index==self.id_usuario].values
    b = a.squeeze().tolist()
    d = self.Impresora_user[self.Impresora_user.index.isin(b)]
    l = ','.join(d.values)
    Impresora_seen_by_similar_users = l.split(',')
    Impresora_under_consideration = list(set(Impresora_seen_by_similar_users)-set(list(map(str, Impresora_seen_by_user))))
    Impresora_under_consideration = list(map(int, Impresora_under_consideration)) # donde esta str es int
    score = []
    for item in Impresora_under_consideration:
      c = self.final_impresoras.loc[:,item]
      d = c[c.index.isin(b)]
      f = d[d.notnull()]
      avg_user = self.Mean.loc[self.Mean['id_user'] == self.id_usuario,'puntuacion'].values[0]
      index = f.index.values.squeeze().tolist()
      corr = self.similarity_with_impresoras.loc[self.id_usuario,index]
      fin = pd.concat([f, corr], axis=1)
      fin.columns = ['adg_score','correlation']
      fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
      nume = fin['score'].sum()
      deno = fin['correlation'].sum()
      final_score = avg_user + (nume/deno)
      score.append(final_score)
    data = pd.DataFrame({'id_impresora':Impresora_under_consideration,'score':score})
    top_5_recommendation = data.sort_values(by='score',ascending=False).head(10)
    Impresoras_Name = top_5_recommendation.merge(self.tabla_impresoras, how='inner', on='id_impresora')
    Impresoras_Names = Impresoras_Name.id_impresora.values.tolist()
    return Impresoras_Names


  def mainHibrido(self, recomendacion_basado_contenido,recomendacion_colaborativo):
    Hibrido = pd.DataFrame()
    impresoras_calificadas = self.tabla_impresoras_calificadas.id_impresora.unique()

    Hibrido["id_impresoras"] = impresoras_calificadas
    Hibrido = Hibrido.sort_values('id_impresoras',ascending=True)

    df2=self.tabla_impresoras_calificadas.groupby("id_impresora").count()[["puntuacion"]]
    Hibrido["puntuacion_count"] = df2["puntuacion"].values

    df3=self.tabla_impresoras_calificadas.groupby("id_impresora").mean()[["puntuacion"]]
    Hibrido["puntuacion_average"] = df3["puntuacion"].values

    v = Hibrido["puntuacion_count"]
    R = Hibrido["puntuacion_average"]
    C = Hibrido["puntuacion_average"].mean()
    m = Hibrido["puntuacion_count"].quantile(0.70)

    Hibrido['weighted_average']=((R*v)+ (C*m))/(v+m)

    BasadoEnContenido  = recomendacion_basado_contenido.to_list()

    Colaborativo = recomendacion_colaborativo

    for id in Colaborativo:
      if id not in BasadoEnContenido:
        BasadoEnContenido.append(id)

    Hibrido = Hibrido[Hibrido.id_impresoras.isin(BasadoEnContenido)]
    Hibrido = Hibrido.sort_values('weighted_average',ascending=False)
    recomendacionFinal = Hibrido["id_impresoras"]
    recomendacionFinal = recomendacionFinal.to_list()
    for id in BasadoEnContenido:
      if id not in recomendacionFinal:
        recomendacionFinal.append(id)

    return recomendacionFinal

  def eval_model(self):
    self.eval1()
    columnaPerfilUser, valorPerfilUser, dataframeFinal = self.mainContenido()
    recomendacion_basado_contenido = dataframeFinal["id_impresora"].head(10)
    recomendacion_colaborativo = self.User_item_score1()
    return columnaPerfilUser, valorPerfilUser, self.mainHibrido(recomendacion_basado_contenido, recomendacion_colaborativo)
