import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv("datasets/companies_locations.csv")


def fig_update_layout(fig):
    fig.update_layout(
        height=800,
        mapbox=dict(
            style='open-street-map',
            zoom=3,
            center=dict(lon=df['longitude'].mean(), lat=df['latitude'].mean())
        )
    )
    
    return fig


def individual_scattergeo(selected_company):
    fig = go.Figure()

    fig.add_trace(
        go.Scattermapbox(
            mode="markers",
            lat=df.query(f"company == '{selected_company}'")["latitude"],
            lon=df.query(f"company == '{selected_company}'")["longitude"],
            text=df.query(f"company == '{selected_company}'")["text"],
            name=selected_company,
            opacity=0.8,
            marker=dict(
                # symbol="marker",
                size=15,
                color=df.query(f"company == '{selected_company}'")["color"]
            )
        )
    )

    

    return fig_update_layout(fig=fig)


"""
Returns a scattergeo figure of all companies' warehouse locations 
"""
def all_companies_scattergeo():
    fig = go.Figure()

    for company in df.company.unique():
        fig.add_trace(go.Scattermapbox(
            mode="markers",
            lat=df.query(f"company == '{company}'")["latitude"],
            lon=df.query(f"company == '{company}'")["longitude"],
            text=df.query(f"company == '{company}'")["text"],
            name=company,
            opacity=0.8,
            marker=dict(
                # symbol="marker",
                size=15,
                color=df.query(f"company == '{company}'")["color"]
            )
        ))

    # fig.update_mapboxes(accesstoken=free_access_token)

    return fig_update_layout(fig=fig)


def filter_by_company_scattergeo(selected_companies):
    fig = go.Figure()

    for company in selected_companies:
        fig.add_trace(go.Scattermapbox(
            mode="markers",
            lat=df.query(f"company == '{company}'")["latitude"],
            lon=df.query(f"company == '{company}'")["longitude"],
            text=df.query(f"company == '{company}'")["text"],
            name=company,
            opacity=0.8,
            marker=dict(
                # symbol="marker",
                size=15,
                color=df.query(f"company == '{company}'")["color"]
            )
        ))

    return fig_update_layout(fig=fig)



def compare_scattergeo(selected_company):
    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lat=df.query(f"company == 'Altor Solutions'")["latitude"],
        lon=df.query(f"company == 'Altor Solutions'")["longitude"],
        text=df.query(f"company == 'Altor Solutions'")["text"],
        name="Altor Solutions",
        opacity=0.8,
        marker=dict(
            # symbol="village",
            size=15,
            color="black"
        )
    )
    )

    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lat=df.query(f"company == '{selected_company}'")["latitude"],
        lon=df.query(f"company == '{selected_company}'")["longitude"],
        text=df.query(f"company == '{selected_company}'")["text"],
        name=selected_company,
        opacity=0.8,
        marker=dict(
            # symbol="marker",
            size=15,
            color=df.query(f"company == '{selected_company}'")["color"]
        )
    )
    )

    return fig_update_layout(fig=fig)
    


    