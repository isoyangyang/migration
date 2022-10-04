import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def total_rw_change(df1, df2):
    """Return the total risk-weight change between periods including all customers"""
    risk_weight_p1 = df1['RWA'].sum()/df1['ead_amount'].sum()
    risk_weight_p2 = df2['RWA'].sum()/df2['ead_amount'].sum()

    return (risk_weight_p2 - risk_weight_p1)/risk_weight_p1


def plot_agg_changes(df1, df2, column_name, ratings):
    """Plot changes in aggregate EAD, RWA and risk-weights per rating category"""
    df1_line = df1.groupby('rating')[column_name].sum()

    df2_line = df2.groupby('rating')[column_name].sum()

    plt.plot(ratings, df1_line, label=f'Period 1 {column_name}', linestyle='--', color='red')
    plt.plot(ratings, df2_line, label=f'Period 2 {column_name}', linestyle='-.')
    plt.legend()
    plt.ylabel(f'{column_name} in thousands')
    plt.xlabel('Ratings')
    plt.show()


"""Rename dataframe columns to substitute spaces for underscores"""
renamed_columns = {
            'Rating/Scoring': 'rating',
            'Original Exposure': 'original_exposure',
            'EAD Amount': 'ead_amount',
            'Capital Requirement': 'capital_requirement',
            'Expected Loss': 'expected_loss',
            'EAD x PD': 'ead_x_pd',
            'EAD x LGD': 'ead_x_lgd'}


def transition_matrix(dataframe):
    """Create credit rating transition matrix and heatmap"""
    x = pd.crosstab(dataframe.rating_P1, dataframe.rating_P2,
                    margins=True,
                    margins_name='Total',
                    normalize='index').round(4) * 100
    ax = sns.heatmap(x, annot=True, cmap='crest')
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    plt.ylabel('Period 1')
    plt.xlabel('Period 2')
    plt.title('Transition Matrix: Probabilities of credit rating migration between periods')
    plt.show()


# """Details of PC0 to PC4 migrations"""
# pc0_to_pc4 = inner_join_retained_customers.query(
#     'rating_P1.str.fullmatch("PC0") and rating_P2.str.contains("PC4")', engine='python').sort_values(
#     'expected_loss_P1')
#
# print(pc0_to_pc4.groupby(['rating_P1', 'rating_P2']).sum())
#
#     pc1_to_pc0 = inner_join_retained_customers.query(
#         'rating_P1.str.contains("PC1")').sort_values(
#         'expected_loss_P1')
#
#     print(pc1_to_pc0.groupby(['rating_P1', 'rating_P2']).sum())