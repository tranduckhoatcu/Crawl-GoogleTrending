import os
import glob2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


def save_and_plot():
    sns.set_style('darkgrid')
    relatedEntities = []
    relatedQueries = []
    for ext in [["*relatedEntities.csv","*relatedQueries.csv"]]:
        for directory in glob2.glob(r"file_downloaded/*/"):
            relatedEntities += glob2.glob(os.path.join(directory, ext[0]))
            relatedQueries += glob2.glob(os.path.join(directory, ext[1]))


    final_df = []
    for category in [relatedEntities,relatedQueries]:
        data_list = []
        data_name = []
        for table in category:
            data_name.append(os.path.basename(os.path.dirname(table)))
            df = pd.read_csv(table,sep=',', header=None, engine='python').reset_index()
            df.columns = ['Name', 'Numbers']
            temp1 = df.iloc[1:df.index[df['Name'] == 'RISING'].values[0],:].reset_index(drop=True)
            temp2 = df.iloc[df.index[df['Name'] == 'RISING'].values[0]+1:,:].reset_index(drop=True)
            data_list.append(pd.concat([temp1, temp2],keys=["TOP", "RISING"],axis=0))
        table_df = pd.concat(data_list,keys=data_name,axis=0).reset_index().drop('level_2', 1)
        table_df.columns = ['Categories', 'Feature', 'Name', 'Indicator']
        final_df.append(table_df)
    
    writer = pd.ExcelWriter('vn_trend_2020.xls', engine='xlsxwriter')
    final_df[0].to_excel(writer, sheet_name='related Entities')
    final_df[1].to_excel(writer, sheet_name='related Queries')
    writer.save()
    print('vn_trend_2020.xls Saved in:',os.getcwd())

    plot = final_df[0][(final_df[0]['Categories'] == 'Finance') & (final_df[0]['Feature'] == 'TOP')][['Name', 'Indicator']].head(10)

    sns.set(font_scale=2)
    plt.figure(figsize=(30,20))
    splot = sns.barplot(x=plot['Indicator'].astype(int), y=plot['Name'])
    plt.xlabel('Relative scale of popular topics')
    plt.ylabel('Name')
    plt.title('Top 10 Search topics related to Finance in 2020',y=1.015)
    splot.xaxis.set_label_coords(0.5, -0.05)
    splot.yaxis.set_label_coords(-0.13, 0.5)
    splot.margins(x=0)
    for p in splot.patches:
        splot.annotate("%.1f" % p.get_width(), xy=(p.get_width(), p.get_y()+p.get_height()/2),
                xytext=(5, 0), textcoords='offset points', ha="left", va="center") 
    plt.savefig('Top 10 Search topics related to Finance in 2020.png')

    fig =  ff.create_table(final_df[0][(final_df[0]['Categories'] == 'Finance') & (final_df[0]['Feature'] == 'RISING')][['Name', 'Indicator']].head(10))
    fig.update_layout(
        autosize=True,
        width=500,
        height=200,
        title_text="Top 10 Rising Search topics related to Finance in 2020",
        margin={'t':50}
    )
    fig.write_image("10 Rising Search topics related to Finance in 2020.png", scale=2)

    plot = final_df[1][(final_df[1]['Categories'] == 'Finance') & (final_df[1]['Feature'] == 'TOP')][['Name', 'Indicator']].head(10)
    sns.set(font_scale=2)
    plt.figure(figsize=(30,20))
    splot = sns.barplot(x=plot['Indicator'].astype(int), y=plot['Name'])
    plt.xlabel('Relative scale of popular keywords')
    plt.ylabel('Name')
    plt.title('Top 10 Search keywords related to Finance in 2020',y=1.015)
    splot.xaxis.set_label_coords(0.5, -0.05)
    splot.yaxis.set_label_coords(-0.13, 0.5)
    splot.margins(x=0)
    for p in splot.patches:
        splot.annotate("%.1f" % p.get_width(), xy=(p.get_width(), p.get_y()+p.get_height()/2),
                xytext=(5, 0), textcoords='offset points', ha="left", va="center") 
    plt.savefig('Top 10 Search keywords related to Finance in 2020.png')

    fig =  ff.create_table(final_df[1][(final_df[1]['Categories'] == 'Finance') & (final_df[1]['Feature'] == 'RISING')][['Name', 'Indicator']].head(10))
    fig.update_layout(
        autosize=True,
        width=500,
        height=200,
        title_text="Top 10 Rising Search Keywords related to Finance in 2020",
        margin={'t':50}
    )
    fig.write_image("10 Rising Search Keywords related to Finance in 2020.png", scale=2)

    print('Chart Saved in:',os.getcwd())