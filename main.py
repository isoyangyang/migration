import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import utils
import seaborn as sns


def main():
    # Import data
    xls = pd.ExcelFile('/Users/isoyang/Downloads/case_study/Migration_Case_Data.xlsx')
    df1 = pd.read_excel(xls, 'Period 1')  # First period
    df2 = pd.read_excel(xls, 'Period 2')  # Second period

    # Rename columns to substitute underscores for spaces and forward slash
    df1 = df1.rename(utils.renamed_columns, axis=1)
    df2 = df2.rename(utils.renamed_columns, axis=1)

    # Change in total risk-weight
    # total_rw_delta = utils.total_rw_change(df1, df2)
    # print(total_rw_delta)

    # Get all rating classes in a sorted list
    ratings = df1.rating.unique().tolist()
    ratings.sort()

    # Plot aggregate changes per column and per rating
    column_of_interest = 'RWA'
    # utils.plot_agg_changes(df1, df2, column_of_interest, ratings)

    # Unrated customers
    # unrated_customers = df2.query('rating.str.contains("PCU")', engine='python').sort_values('RWA', ascending=[False])
    # print(unrated_customers.head(10))

    # Customer ID 3396 causes a big impact due to being unrated in period 1 which leads to high capital_req and EL
    # id3396_p2 = df2.query('ID == 3396')
    # id3396_p1 = df1.query('ID == 3396')
    # print(id3396_p1, id3396_p2)
    #
    # df1_series = df1.groupby('rating')['expected_loss'].sum()
    # df2_series = df2.groupby('rating')['expected_loss'].sum()
    # myexplode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2]
    #
    # plt.pie(df2_series, labels=ratings, explode=myexplode)
    # plt.show()

    # full_join_all_customers = df1.merge(df2, how='outer', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'))
    inner_join_retained_customers = df1.merge(df2, how='inner', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'))
    # inner_join_new_customers = df1.merge(df2, how='right', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'))

    test = pd.merge(df1, df2, how='outer', left_on='ID', right_on='ID', suffixes=('_P1', '_P2'), indicator=True).query('_merge=="right_only"')
    el = list(test['expected_loss_P2'])
    ratingx = list(test['rating_P2'])
    fig = plt.figure(figsize=(10, 5))
    plt.bar(ratingx, el, color='maroon')
    plt.show()
    print(test.head)


    # unrated_customers_P1P2 = inner_join_retained_customers.query(
    #     '~rating_P1.str.contains("PC0") and rating_P2.str.contains("PC0")', engine='python').sort_values(
    #     'expected_loss_P2')
    # print(unrated_customers_P1P2.head(100))
    # unrated_customers_P1P2.plot(kind='line', x='rating_P1', y='expected_loss_P2')
    # plt.show()
    #
    # x = inner_join_retained_customers.query('rating_P1.str.fullmatch("PC5") and rating_P2.str.fullmatch("PC5")').groupby('rating_P1', 'rating_P2').count()
    # y = inner_join_retained_customers.groupby(['rating_P1', 'rating_P2'])['rating_P1'].count()

    # utils.transition_matrix(inner_join_retained_customers)

    # inner_join_retained_customers['delta_el'] = inner_join_retained_customers['expected_loss_P2'] - inner_join_retained_customers['expected_loss_P1']
    # sorted_df = inner_join_retained_customers.sort_values('delta_el', ascending=True)
    # print(sorted_df.head(50))

    # Compute and plot mean and std per rating class of EL and RWA using describe()

    # data = {
    #     'df1_rwa': df1_rwa_per_rating,
    #     'df1_ead': df1_ead_per_rating,
    #     'df1_rw': df1_rw,
    #     'df2_rwa': df2_rwa_per_rating,
    #     'df2_ead': df2_ead_per_rating,
    #     'df2_rw': df2_rw,
    # }
    #
    # combined_rwa_ead = pd.DataFrame(data)
    # print(combined_rwa_ead)

    # combined_rwa_ead.plot(y='df2_rw', kind='line')
    # plt.show()

    # ratings_list = df1.rating.unique().tolist()
    # ratings_list.sort()

    # print(inner_join)

    # data = {}
    # for i in result.index:
    #     x = str(result['rating_P1'][i])+str(result['rating_P2'][i])
    #     # print(x)
    #     if x in data:
    #         data['x'] += 1
    #     else:
    #         data.update({'x': 1})
    #
    # print(data)

    # print(df1.head())
    # print(df2.head())
    #
    # # Check for duplicate IDs
    # if df1.ID.duplicated().sum() > 0 or df2.ID.duplicated().sum() > 0:
    #     print("df1 duplicates:", df1.ID.duplicated().sum(), '\n', "df2 duplicates:", df2.ID.duplicated().sum())
    #
    # print(df1.query('original_exposure > 1000000'))
    #
    # ax = df1.plot(x='rating', y='capital_requirement')
    # df2.plot(ax=ax, x='rating', y='capital_requirement')
    #
    # plt.show()
    #
    # # 3039  3396    PCU  0.02500  0.45000       8.108567e+06  8.108567e+06  1.049936e+07         839948.80305    91221.38111  202714.18026  3.648855e+06
    #


if __name__ == '__main__':
    main()
