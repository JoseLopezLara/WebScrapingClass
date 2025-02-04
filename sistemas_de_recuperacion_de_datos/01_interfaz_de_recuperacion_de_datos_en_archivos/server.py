import streamlit as st
import pandas as pd
import shelve


def create_age_slider():
    """Create and return age range slider"""
    st.slider(
        'Seleccionar rango de edades a filtrar',
        min_value=0,    
        max_value=100,  
        value=(25, 55),  
        key='age_slider'
    )
    return st.session_state.age_slider

def find_users_in_range(min_age: int, max_age: int) -> tuple:
    """Filter users by age range and return results"""
    ages = []
    names = []
    
    try:
        with shelve.open('users_db') as db:
            if len(db) == 0:
                st.warning("No hay usuarios en la base de datos")
                return [], []
            
            for username, age in db.items():
                if min_age <= age <= max_age:
                    names.append(username)
                    ages.append(age)
    except Exception as e:
        st.error(f"Error al leer la base de datos: {e}")
    
    return names, ages

def display_results(names: list, ages: list):
    """Display filtered results"""
    if names and ages:
        df = pd.DataFrame({
            'Nombre': names,
            'Edad': ages
        })
        st.dataframe(df)
    else:
        st.info("No se encontraron usuarios en el rango seleccionado")

def main():
    """Main application flow"""
    # Title
    st.title("Práctica #1 Recuperación de datos")
    
    # Age Slider
    slider_session_values = create_age_slider()
    st.write(f'Rango seleccionado: {slider_session_values[0]} a {slider_session_values[1]}')
    
    names, ages = find_users_in_range(slider_session_values[0], slider_session_values[1])
    display_results(names, ages)

if __name__ == "__main__":
    main()