# utils/all_company_graphs.py
import folium
import requests
import base64
from math import radians, sin, cos, sqrt, atan2
from folium import IFrame
import streamlit as st
import pandas as pd

# Cache the GeoJSON data
@st.cache_data
def get_geojson():
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
    return requests.get(url).json()

# Cache the marker icon creation
@st.cache_data
def create_colored_marker_icon(color):
    svg_marker = '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
            <path stroke="#000000" stroke-width="1" fill="{color}" d="M12 0C7.6 0 4 3.6 4 8c0 5.4 8 16 8 16s8-10.6 8-16c0-4.4-3.6-8-8-8zm0 12c-2.2 0-4-1.8-4-4s1.8-4 4-4 4 1.8 4 4-1.8 4-4 4z"/>
        </svg>
    '''
    
    if color.startswith('#'):
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        color = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.7)'
    
    colored_marker = svg_marker.format(color=color)
    base64_marker = base64.b64encode(colored_marker.encode('utf-8')).decode('utf-8')
    return f'data:image/svg+xml;base64,{base64_marker}'

@st.cache_data
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 3956  # Radius of earth in miles
    return c * r

@st.cache_data
def find_proximity_markers(df_json, lat, lon, radius=300):
    df = pd.DataFrame(df_json)
    nearby_markers = []
    for _, row in df.iterrows():
        distance = haversine(lon, lat, row['longitude'], row['latitude'])
        if distance <= radius:
            row_dict = row.to_dict()
            row_dict['distance'] = round(distance, 1)
            nearby_markers.append(row_dict)
    return nearby_markers

@st.cache_resource
def create_proximity_map(lat, lon, nearby_markers):
    popup_map = folium.Map(
        location=[lat, lon],
        zoom_start=5,
        width=400,
        height=300
    )
    
    folium.Circle(
        location=[lat, lon],
        radius=300 * 1609.34,
        color='red',
        fill=True,
        opacity=0.2
    ).add_to(popup_map)
    
    for marker in nearby_markers:
        tooltip_html = f"""
        <h4>{marker['company']}</h4>
        <h5>{marker['city']}, {marker['state']}</h5>
        <h5>Distance: {marker['distance']} miles</h5>
        """
        
        folium.Marker(
            location=[marker['latitude'], marker['longitude']],
            tooltip=tooltip_html,
            icon=folium.CustomIcon(
                icon_image=create_colored_marker_icon(marker['color']),
                icon_size=(20, 20),
                icon_anchor=(10, 20)
            )
        ).add_to(popup_map)
    
    return popup_map

@st.cache_data
def create_scrollable_legend(unique_markers):
    legend_html = '''
        <div style="
            position: fixed; 
            bottom: 50px;
            right: 50px;
            width: 250px;
            height: 300px;
            overflow-y: auto;
            background-color: white;
            border: 2px solid grey;
            z-index: 1000;
            border-radius: 5px;
            padding: 10px;
            font-size: 12px;
        ">
        <h4 style="margin-top: 0;">Company Locations</h4>
    '''
    
    for company, color in unique_markers:
        legend_html += f'''
            <div style="margin-bottom: 5px;">
                <span style="
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    background-color: {color};
                    opacity: 0.7;
                    border: 1px solid black;
                    margin-right: 5px;
                "></span>
                {company}
            </div>
        '''
    
    legend_html += '</div>'
    return legend_html

@st.cache_resource
def create_map(df):
    # Create state-level counts
    state_counts = df['state'].value_counts().to_dict()
    
    # Create the main map
    m = folium.Map(
        location=[df['latitude'].mean(), df['longitude'].mean()],
        zoom_start=4,
        tiles="Cartodb Positron"
    )
    
    # Convert DataFrame to dict for caching
    df_dict = df.to_dict('records')
    
    # Add markers with proximity maps in popups
    for row in df_dict:
        nearby_markers = find_proximity_markers(df_dict, row['latitude'], row['longitude'])
        popup_map = create_proximity_map(row['latitude'], row['longitude'], nearby_markers)
        
        popup_html = f"""
            <div style="width:400px">
                <h4>{row['company']}</h4>
                <p>{row['city']}, {row['state']}</p>
                {popup_map.get_root().render()}
            </div>
        """
        
        tooltip_html = f"""
            <h4>{row['company']}</h4>
            <h5>{row['city']}, {row['state']}</h5>
        """
        
        popup = folium.Popup(
            IFrame(html=popup_html, width=420, height=350),
            max_width=420
        )
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            tooltip=tooltip_html,
            icon=folium.CustomIcon(
                icon_image=create_colored_marker_icon(row['color']),
                icon_size=(30, 30),
                icon_anchor=(15, 30)
            )
        ).add_to(m)
    
    # Add Choropleth layer
    state_geo = get_geojson()
    
    folium.Choropleth(
        geo_data=state_geo,
        name='choropleth',
        data=state_counts,
        columns=['state', 'count'],
        key_on='feature.id',
        fill_color='YlGn',
        nan_fill_color="grey",
        nan_fill_opacity=0.4,
        fill_opacity=0.6,
        line_opacity=0.4,
        legend_name='Number of Warehouses'
    ).add_to(m)
    
    # Add the scrollable legend
    unique_markers = df[['company', 'color']].drop_duplicates().values.tolist()
    legend_html = create_scrollable_legend(unique_markers)
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m
