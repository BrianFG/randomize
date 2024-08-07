import streamlit as st
import pandas as pd

# Título de la aplicación
st.title('Recetas')

# Crear un input para subir un archivo
uploaded_file = st.file_uploader("Excel de recetas", type=["xlsx"])

# Crear un input para ingresar palabras a excluir
selected_exclude_words = st.text_area("Palabras a excluir de los ingredientes (separadas por comas)")
exclude_words = selected_exclude_words.lower().strip().split(",")
exclude_words = [word.strip() for word in exclude_words if len(word.strip()) > 0]

exclude_options = ['lechuga', 'pollo', 'pescado', 'pasta', 'queso', 'aceite', 'ajo', 'limón', 'huevos', 'espinacas']
exclude_ingredients = st.multiselect("Ingredientes a excluir", exclude_options)
exclude_list = exclude_words + exclude_ingredients


if uploaded_file is not None:
    # Leer el archivo Excel
    df = pd.read_excel(uploaded_file)

    if len(exclude_list) > 0:
        
        # Función para verificar si algún ingrediente contiene alguna de las palabras a excluir
        def should_exclude_recipe(ingredients, exclude_list):
            for word in exclude_list:
                if word.lower() in ingredients.lower():
                    return True
            return False

        # Filtrar las recetas que no contienen las palabras a excluir
        filtered_df = df[~df['Ingredientes'].apply(lambda x: should_exclude_recipe(x, exclude_list))]
    else: 
        filtered_df = df
    # Mostrar el DataFrame filtrado
    st.write("Aquí están las recetas filtradas del archivo Excel:")
    st.dataframe(filtered_df)


    if len(filtered_df) >= 3:
        breakfast_recipe = filtered_df.sample(n=1)
        lunch_recipe = filtered_df.sample(n=1)
        dinner_recipe = filtered_df.sample(n=1)
        
        st.markdown("### Desayuno")
        st.markdown(f"**Nombre:** {breakfast_recipe.iloc[0]['Nombre']}")
        st.markdown(f"**Ingredientes:** {breakfast_recipe.iloc[0]['Ingredientes']}")
        st.markdown(f"**Preparación:** {breakfast_recipe.iloc[0]['Preparación']}")

        st.markdown("### Comida")
        st.markdown(f"**Nombre:** {lunch_recipe.iloc[0]['Nombre']}")
        st.markdown(f"**Ingredientes:** {lunch_recipe.iloc[0]['Ingredientes']}")
        st.markdown(f"**Preparación:** {lunch_recipe.iloc[0]['Preparación']}")

        st.markdown("### Cena")
        st.markdown(f"**Nombre:** {dinner_recipe.iloc[0]['Nombre']}")
        st.markdown(f"**Ingredientes:** {dinner_recipe.iloc[0]['Ingredientes']}")
        st.markdown(f"**Preparación:** {dinner_recipe.iloc[0]['Preparación']}")
    else:
        st.write("No hay suficientes recetas disponibles después de aplicar los filtros.")