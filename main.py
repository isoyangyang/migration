import pandas as pd
from matplotlib import pyplot as plt
import utils
import seaborn as sns


def main():
    """Import data"""
    xls = pd.ExcelFile('/Users/isoyang/Downloads/case_study/Migration_Case_Data.xlsx')
    df1 = pd.read_excel(xls, 'Period 1')  # First period
    df2 = pd.read_excel(xls, 'Period 2')  # Second period

    """Rename columns to substitute underscores for spaces"""
    df1 = df1.rename(utils.renamed_columns, axis=1)
    df2 = df2.rename(utils.renamed_columns, axis=1)

    """Change in total risk-weight, expected loss and probability of default (incl. all counterparties)"""
    # total_rw_delta = utils.total_rw_change(df1, df2)  # -0.144
    # total_el_delta = utils.total_el_change(df1, df2)  # 0.220
    # total_avg_pd = utils.total_pd_change(df1, df2)  # 0.301
    # print(total_rw_delta, total_el_delta, total_avg_pd)

    """Get all rating classes in a sorted list"""
    ratings = df1.rating.unique().tolist()
    ratings.sort()

    """Plot aggregate changes per column and per rating"""
    # column_of_interest = 'capital_requirement'
    # utils.plot_agg_changes(df1, df2, column_of_interest, ratings)

    """One significantly larger exposure which is unrated in P1 and PC6 in P2 skews the results. 
    For accuracy and better consistency, a new dataframe is copied,
    and the counterparty's P1 values are substituted with its P2"""
    # Get the counterparty ID
    # print(df1.sort_values('expected_loss', ascending=False).head(1))
    # # Substitute P2 row values to copied dataframe
    df1_3396_modified = df1.copy()
    df1_3396_modified.iloc[3039] = df2.iloc[3395]
    df1_3396_modified = df1_3396_modified.sort_values('rating')

    """Change in total risk-weight, expected loss and probability of default (counterparty 3396 EXCLUDED)"""
    total_rw_delta = utils.total_rw_change(df1_3396_modified, df2)  # 0.063
    total_el_delta = utils.total_el_change(df1_3396_modified, df2)  # 0.573
    total_avg_pd = utils.total_pd_change(df1_3396_modified, df2)  # 0.301
    total_lgd_delta = utils.total_lgd_change(df1_3396_modified, df2)  # - 0.010

    print(total_rw_delta, total_el_delta, total_avg_pd, total_lgd_delta)

    """Plot aggregate changes per column and per rating. Modify column_of_interest variable"""
    # column_of_interest = 'capital_requirement'
    # utils.plot_agg_changes(df1_3396_modified, df2, column_of_interest, ratings)

    """Investigate large discrepancy in expected losses between P1 and P2 in PC0+ category"""
    total_el_p1 = df1.query('rating.str.contains("PC0+", regex=False)')['expected_loss'].sum()
    total_el_p2 = df2.query('rating.str.contains("PC0+", regex=False)')['expected_loss'].sum()
    total_el_p2_temp = df2.groupby('rating')['expected_loss'].sum()
    # print(total_el_p2_temp)
    # delta_el = total_el_p2 - total_el_p1
    # print(delta_el)  # 279798

    retained_customers = df1.merge(df2, how='inner', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'))
    # big_el = retained_customers.query('~rating_P1.str.contains("PC0") and rating_P2.str.contains("PC0+", regex=False)',
    #                                   engine='python').sort_values('expected_loss_P2', ascending=False)

    # temp = df2.query('rating.str.contains("PC0+")')\
    #     .sort_values('expected_loss', ascending=[False]).head(10)
    # ids = temp['ID'].tolist()
    # temp2 = df1.query('ID == @ids and ~rating.str.contains("PC0")', engine='python').sort_values('expected_loss', ascending=[False])
    # print(temp, "\n", temp2)

    """Join dataframes to explore all customers and customers only existing in both periods"""
    # full_join_all_customers = df1.merge(df2, how='outer', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'))
    # inner_join_new_customers = df1.merge(df2, how='right', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'))

    """New Customers"""
    new_customers = pd.merge(df1, df2, how='outer', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'),
                             indicator=True).query('_merge=="right_only"')

    new_customers['mean_cp_per_rating'] = new_customers['capital_requirement_P2']\
        .groupby(new_customers['rating_P2'])\
        .transform('mean')

    df1_3396_modified['mean_cp_per_rating'] = df1_3396_modified['capital_requirement']\
        .groupby(df1_3396_modified['rating'])\
        .transform('mean')

    fig = plt.figure(figsize=(10, 5))
    # plt.bar(new_customers['rating_P2'], new_customers['mean_el_per_rating'], color='blue')
    # sns.barplot(data=new_customers, x='rating_P2', y='mean_el_per_rating', color='blue')
    sns.barplot(data=df1_3396_modified, x='rating', y='mean_cp_per_rating', color='blue')
    # plt.show()
    # print(new_customers.head)

    """Explore customers that have defaulted"""
    defaulted_customers_P1P2 = retained_customers.query(
        '~rating_P1.str.contains("PC0") and rating_P2.str.contains("PC0")', engine='python').sort_values(
        'expected_loss_P2')
    # print(defaulted_customers_P1P2.head(100))
    # defaulted_customers_P1P2.plot(kind='line', x='rating_P1', y='expected_loss_P2')
    # plt.show()

    # x = inner_join_retained_customers.query('rating_P1.str.fullmatch("PC5") and rating_P2.str.fullmatch("PC5")').groupby('rating_P1', 'rating_P2').count()
    # y = inner_join_retained_customers.groupby(['rating_P1', 'rating_P2'])['rating_P1'].count()

    """Transition Matrix"""
    # utils.transition_matrix(retained_customers)


if __name__ == '__main__':
    main()
