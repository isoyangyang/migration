import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns


"""Rename dataframe columns to substitute spaces for underscores"""
renamed_columns = {
            'Rating/Scoring': 'rating',
            'Original Exposure': 'original_exposure',
            'EAD Amount': 'ead_amount',
            'Capital Requirement': 'capital_requirement',
            'Expected Loss': 'expected_loss',
            'EAD x PD': 'ead_x_pd',
            'EAD x LGD': 'ead_x_lgd'}


def total_rw_change(df1, df2):
    """Return the total risk-weight change between periods"""
    risk_weight_p1 = df1['RWA'].sum()/df1['ead_amount'].sum()
    risk_weight_p2 = df2['RWA'].sum()/df2['ead_amount'].sum()

    return (risk_weight_p2 - risk_weight_p1)/risk_weight_p1


def total_el_change(df1, df2):
    """Return the total expected loss change between periods"""
    el_p1 = df1['expected_loss'].sum()
    el_p2 = df2['expected_loss'].sum()

    return (el_p2 - el_p1)/el_p1


def total_pd_change(df1, df2):
    """Return the total change in probability of default divided by the number of customers between periods"""
    pd_p1 = df1['PD'].mean()
    pd_p2 = df2['PD'].mean()
    print(pd_p1, pd_p2)

    return (pd_p2 - pd_p1)/pd_p1


def total_lgd_change(df1, df2):
    """Return the total change in probability of default divided by the number of customers between periods"""
    lgd_p1 = df1['LGD'].mean()
    lgd_p2 = df2['LGD'].mean()
    print(lgd_p1, lgd_p2)

    return (lgd_p2 - lgd_p1)/lgd_p1


def plot_agg_changes(df1, df2, column_name, ratings):
    """Plot changes in aggregate EAD, RWA and risk-weights per rating category"""
    df1_grouped = df1.groupby('rating')[column_name].sum()

    df2_grouped = df2.groupby('rating_P2')[column_name].sum()

    ax = np.arange(len(df1_grouped))

    plt.bar(ax - 0.2, df1_grouped, width=0.4, label='Period 1', color='dodgerblue')
    plt.bar(ax + 0.2, df2_grouped, width=0.4, label='Period 2', color='blue')

    plt.xticks(ax, ratings)

    # plt.plot(ratings, df1_grouped, label=f'Period 1 {column_name}', linestyle='solid', color='red')
    # plt.plot(ratings, df2_grouped, label=f'Period 2 {column_name}', linestyle='--')
    plt.legend()
    plt.ylabel(f'{column_name}', fontsize=14)
    plt.xlabel('Ratings', fontsize=14)
    plt.show()


def transition_matrix(dataframe):
    """Create credit rating transition matrix and heatmap"""
    x = pd.crosstab(dataframe.rating_P1, dataframe.rating_P2,
                    margins=True,
                    margins_name='Total',
                    normalize='index').round(4) * 100
    ax = sns.heatmap(x, annot=True, cmap='Blues', fmt='g')
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    plt.ylabel('Period 1')
    plt.xlabel('Period 2')
    plt.title('Transition Matrix: Probabilities of credit rating migration between periods')
    plt.show()

