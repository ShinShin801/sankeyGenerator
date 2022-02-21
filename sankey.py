import random
import plotly.graph_objects as go
import pandas as pd


def sankey_generation(df):
    num_kind = df['name'].nunique()
    num_times = int(df['nth'].max())

    # Create all the patterns
    all_name = list(df['name'].unique())

    comb_list = []
    for i in list(set(all_name)):
        for j in list(set(all_name)):
            comb_list.append(f'{i}-{j}')

    # Count all the paterns per section
    one = pd.DataFrame({'comb': comb_list})
    for i in range(1, num_times):
        a = df[df.nth == i]
        b = df[df.nth == i+1]
        c = pd.merge(a, b, how='inner', on='id')
        c['comb'] = c['name_x']+'-'+c['name_y']
        d = c.groupby('comb').count().reset_index()[['comb', 'id']]
        d.rename({'id': i}, axis=1, inplace=True)
        one = pd.merge(one, d, how='left', on='comb')

    title_list = []
    beg = list(map(spliting, comb_list))
    for i in range(len(beg)-1):
        if beg[i] != beg[i+1]:
            title_list.append(beg[i])
    title_list.append(beg[i+1])

    titles = []
    for i in range(1, num_times+1):
        for j in title_list:
            titles.append(add_timing(j, i))

    all = []
    for i in range(1, num_times):
        all += list(one[i])

    colors = ["#"+''.join([random.choice('0123456789ABCDEF')
                          for j in range(6)]) for i in range(num_kind)]
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=50,
            line=dict(color="black", width=0.5),
            label=titles,
            color=colors * num_times
        ),
        link=dict(
            source=sum(
                [[i]*num_kind for i in range(num_kind*(num_times-1))], []),

            target=sum([[i for i in range(num_kind*i, num_kind*i+num_kind)]
                        * num_kind for i in range(1, num_times)], []),
            value=all,
            # color = colors *num_kind*(num_times-1)
        ))])

    # fig.update_layout(title_text="First Buy to Fifth Buy Sankey Diagram", font_size=10)
    fig.update_layout(
        title_text="Sankey Diagram",
        font_size=10,
        autosize=True,
        width=300*num_times,
        height=100*num_kind,
        paper_bgcolor="LightSteelBlue",
    )
    fig.write_html("sankey_output.html")
    print('Done')


def spliting(x):
    return x.split('-')[0]


def add_timing(x, num):
    return f'{x}({num})'


def main():
    df = pd.read_csv('test_sankey.csv')
    sankey_generation(df)


main()
